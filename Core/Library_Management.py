
#---------------------------------------------------------------------------------------------------------------#
# Load Requirements
#---------------------------------------------------------------------------------------------------------------#
import re
from pathlib import Path


#---------------------------------------------------------------------------------------------------------------#
# Library Management
# Create and rename match directories while protecting existing content
#---------------------------------------------------------------------------------------------------------------#
class Library_Management:

    #---------------------------------------------------------------------------------------------------------------#
    # Initialize the library manager
    # Store the library location and dry-run setting
    #---------------------------------------------------------------------------------------------------------------#
    def __init__( self, Library_Directory, Dry_Run = True ):
        self.Library_Directory = Path( Library_Directory )
        self.Dry_Run = Dry_Run


    #---------------------------------------------------------------------------------------------------------------#
    # Find existing directories beginning with the specified match date
    # Support legacy directory names such as 2017-03-06-TEST
    #---------------------------------------------------------------------------------------------------------------#
    def Find_Match_Directories( self, Match_Date ):
        Year_Directory = self.Library_Directory / Match_Date[:4]

        if ( not Year_Directory.is_dir() ):
            return []

        Date_Pattern = re.compile( rf"^{re.escape( Match_Date )}(?:$|[ -])" )

        return sorted(
            Directory
            for Directory in Year_Directory.iterdir()
            if ( Directory.is_dir() and Date_Pattern.match( Directory.name ) )
        )


    #---------------------------------------------------------------------------------------------------------------#
    # Compare the expected directory name against existing match directories
    # Create, rename, or leave directories unchanged as appropriate
    # Never modify ambiguous matches or overwrite an existing target
    #---------------------------------------------------------------------------------------------------------------#
    def Process_Match( self, Directory_Name ):
        Match_Date = Directory_Name[:10]

        if ( not re.fullmatch( r"\d{4}-\d{2}-\d{2}", Match_Date ) or not Directory_Name.startswith( f"{Match_Date} - " ) ):
            raise ValueError( f"Invalid directory name: {Directory_Name}" )

        Year_Directory = self.Library_Directory / Match_Date[:4]
        Target_Directory = Year_Directory / Directory_Name
        Existing_Directories = self.Find_Match_Directories( Match_Date )

        if ( len( Existing_Directories ) > 1 ):
            return {
                "Status": "CONFLICT",
                "Source": None,
                "Target": Target_Directory,
                "Message": f"Multiple directories found for {Match_Date}",
            }

        if ( not Existing_Directories ):
            if ( not self.Dry_Run ):
                Target_Directory.mkdir( parents = True, exist_ok = False )

            return {
                "Status": "CREATE",
                "Source": None,
                "Target": Target_Directory,
                "Message": "Directory created" if ( not self.Dry_Run ) else "Directory would be created",
            }

        Source_Directory = Existing_Directories[0]

        if ( Source_Directory == Target_Directory ):
            return {
                "Status": "UNCHANGED",
                "Source": Source_Directory,
                "Target": Target_Directory,
                "Message": "Directory already matches",
            }

        if ( Target_Directory.exists() ):
            return {
                "Status": "CONFLICT",
                "Source": Source_Directory,
                "Target": Target_Directory,
                "Message": "Target directory already exists",
            }

        if ( not self.Dry_Run ):
            Source_Directory.rename( Target_Directory )

        return {
            "Status": "RENAME",
            "Source": Source_Directory,
            "Target": Target_Directory,
            "Message": "Directory renamed" if ( not self.Dry_Run ) else "Directory would be renamed",
        }
