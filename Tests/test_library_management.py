
#---------------------------------------------------------------------------------------------------------------#
# Load Requirements
#---------------------------------------------------------------------------------------------------------------#
import tempfile
import unittest
from pathlib import Path

from Core.Library_Management import Library_Management


#---------------------------------------------------------------------------------------------------------------#
# Library Management Tests
# Verify directory creation, renaming, and filesystem safeguards
#---------------------------------------------------------------------------------------------------------------#
class Test_Library_Management( unittest.TestCase ):

    #---------------------------------------------------------------------------------------------------------------#
    # Create an isolated temporary library for each test
    #---------------------------------------------------------------------------------------------------------------#
    def setUp( self ):
        self.Temp_Directory = tempfile.TemporaryDirectory()
        self.Library_Directory = Path( self.Temp_Directory.name )
        self.Year_Directory = self.Library_Directory / "2017"
        self.Manager = Library_Management( self.Library_Directory, Dry_Run = False )
        self.Expected_Name = "2017-03-06 - Orlando City at TEST, W 2-1"


    #---------------------------------------------------------------------------------------------------------------#
    # Remove the temporary library after each test
    #---------------------------------------------------------------------------------------------------------------#
    def tearDown( self ):
        self.Temp_Directory.cleanup()


    #---------------------------------------------------------------------------------------------------------------#
    # Verify that a missing match directory is created
    #---------------------------------------------------------------------------------------------------------------#
    def test_Create_Directory( self ):
        """Creates a missing match directory"""

        Result = self.Manager.Process_Match( self.Expected_Name )

        self.assertEqual( Result["Status"], "CREATE" )
        self.assertTrue( ( self.Year_Directory / self.Expected_Name ).is_dir() )


    #---------------------------------------------------------------------------------------------------------------#
    # Verify that updated match information renames an existing directory
    #---------------------------------------------------------------------------------------------------------------#
    def test_Rename_Directory( self ):
        """Renames a date-only directory when match details become available"""

        Original_Directory = self.Year_Directory / "2017-03-06-TEST"
        Original_Directory.mkdir( parents = True )

        Result = self.Manager.Process_Match( self.Expected_Name )

        self.assertEqual( Result["Status"], "RENAME" )
        self.assertFalse( Original_Directory.exists() )
        self.assertTrue( ( self.Year_Directory / self.Expected_Name ).is_dir() )


    #---------------------------------------------------------------------------------------------------------------#
    # Verify that renaming a directory preserves its existing files
    #---------------------------------------------------------------------------------------------------------------#
    def test_Preserve_Files( self ):
        """Preserves files when renaming a match directory"""

        Original_Directory = self.Year_Directory / "2017-03-06-TEST"
        Original_Directory.mkdir( parents = True )

        Original_File = Original_Directory / "Match_Notes.txt"
        Original_File.write_text( "Original match notes", encoding = "utf-8" )

        Result = self.Manager.Process_Match( self.Expected_Name )
        Updated_File = self.Year_Directory / self.Expected_Name / "Match_Notes.txt"

        self.assertEqual( Result["Status"], "RENAME" )
        self.assertTrue( Updated_File.is_file() )
        self.assertEqual( Updated_File.read_text( encoding = "utf-8" ), "Original match notes" )


    #---------------------------------------------------------------------------------------------------------------#
    # Verify that an already-correct directory remains unchanged
    #---------------------------------------------------------------------------------------------------------------#
    def test_Unchanged_Directory( self ):
        """Leaves an already-correct directory unchanged"""

        Expected_Directory = self.Year_Directory / self.Expected_Name
        Expected_Directory.mkdir( parents = True )

        Result = self.Manager.Process_Match( self.Expected_Name )

        self.assertEqual( Result["Status"], "UNCHANGED" )
        self.assertTrue( Expected_Directory.is_dir() )


    #---------------------------------------------------------------------------------------------------------------#
    # Verify that dry-run mode previews creation without modifying the filesystem
    #---------------------------------------------------------------------------------------------------------------#
    def test_Dry_Run_Create( self ):
        """Previews directory creation without creating it"""

        Manager = Library_Management( self.Library_Directory, Dry_Run = True )
        Result = Manager.Process_Match( self.Expected_Name )

        self.assertEqual( Result["Status"], "CREATE" )
        self.assertFalse( self.Year_Directory.exists() )


    #---------------------------------------------------------------------------------------------------------------#
    # Verify that dry-run mode previews renaming without modifying the filesystem
    #---------------------------------------------------------------------------------------------------------------#
    def test_Dry_Run_Rename( self ):
        """Previews directory renaming without modifying it"""

        Original_Directory = self.Year_Directory / "2017-03-06-TEST"
        Original_Directory.mkdir( parents = True )

        Manager = Library_Management( self.Library_Directory, Dry_Run = True )
        Result = Manager.Process_Match( self.Expected_Name )

        self.assertEqual( Result["Status"], "RENAME" )
        self.assertTrue( Original_Directory.is_dir() )
        self.assertFalse( ( self.Year_Directory / self.Expected_Name ).exists() )


    #---------------------------------------------------------------------------------------------------------------#
    # Verify that multiple directories sharing a date cannot be renamed automatically
    #---------------------------------------------------------------------------------------------------------------#
    def test_Multiple_Directories( self ):
        """Reports a conflict when multiple directories share a date"""

        First_Directory = self.Year_Directory / "2017-03-06-TEST"
        Second_Directory = self.Year_Directory / "2017-03-06 - Another Match"

        First_Directory.mkdir( parents = True )
        Second_Directory.mkdir()

        Result = self.Manager.Process_Match( self.Expected_Name )

        self.assertEqual( Result["Status"], "CONFLICT" )
        self.assertTrue( First_Directory.is_dir() )
        self.assertTrue( Second_Directory.is_dir() )


#---------------------------------------------------------------------------------------------------------------#
# Test Entry Point
#---------------------------------------------------------------------------------------------------------------#
if ( __name__ == "__main__" ):
    unittest.main()
