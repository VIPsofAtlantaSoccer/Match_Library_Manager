
#---------------------------------------------------------------------------------------------------------------#
# Load Requirements
#---------------------------------------------------------------------------------------------------------------#
import unittest

from Core.Directory_Naming import Directory_Naming


#---------------------------------------------------------------------------------------------------------------#
# Directory Naming Tests
# Verify directory names for complete and incomplete match records
#---------------------------------------------------------------------------------------------------------------#
class Test_Directory_Naming( unittest.TestCase ):

    #---------------------------------------------------------------------------------------------------------------#
    # Initialize the directory naming utility for each test
    #---------------------------------------------------------------------------------------------------------------#
    def setUp( self ):
        self.Naming = Directory_Naming( "Atlanta United" )


    #---------------------------------------------------------------------------------------------------------------#
    # Verify a match with only a date and configured team
    #---------------------------------------------------------------------------------------------------------------#
    def test_Date_Only( self ):
        """Date-only match generates a directory name"""
        Match = { "Date": "2027-03-06" }
        self.assertEqual( self.Naming.Generate_Name( Match ), "2027-03-06 - Atlanta United" )


    #---------------------------------------------------------------------------------------------------------------#
    # Verify a match with an opponent but no known venue
    #---------------------------------------------------------------------------------------------------------------#
    def test_Unknown_Venue( self ):
        """Unknown venue uses vs format"""
        Match = { "Date": "2027-03-06", "Opponent": "Orlando City" }
        self.assertEqual( self.Naming.Generate_Name( Match ), "2027-03-06 - Atlanta United vs Orlando City" )


    #---------------------------------------------------------------------------------------------------------------#
    # Verify a home victory with the configured team's score first
    #---------------------------------------------------------------------------------------------------------------#
    def test_Home_Win( self ):
        """Home victory generates the correct score"""
        Match = { "Date": "2017-03-18", "Opponent": "Chicago Fire", "Venue": "Home",
                  "Result": "W", "Goals For": "4", "Goals Against": "0", "Round": "Regular Season" }

        self.assertEqual( self.Naming.Generate_Name( Match ), "2017-03-18 - Chicago Fire at Atlanta United, W 4-0" )


    #---------------------------------------------------------------------------------------------------------------#
    # Verify an away defeat with the configured team's score first
    #---------------------------------------------------------------------------------------------------------------#
    def test_Away_Loss( self ):
        """Away loss preserves team-first score"""
        Match = { "Date": "2027-03-06", "Opponent": "Orlando City", "Venue": "Away",
                  "Result": "L", "Goals For": "1", "Goals Against": "3" }

        self.assertEqual( self.Naming.Generate_Name( Match ), "2027-03-06 - Atlanta United at Orlando City, L 1-3" )


    #---------------------------------------------------------------------------------------------------------------#
    # Verify competition and playoff round naming
    #---------------------------------------------------------------------------------------------------------------#
    def test_Playoffs( self ):
        """Playoff competition and round are included"""
        Match = { "Date": "2017-10-26", "Opponent": "Columbus Crew", "Venue": "Home",
                  "Comp": "MLS", "Round": "Cup Playoffs" }

        self.assertEqual( self.Naming.Generate_Name( Match ), "2017-10-26 - Columbus Crew at Atlanta United, MLS Cup Playoffs" )


    #---------------------------------------------------------------------------------------------------------------#
    # Verify penalty shootout scoring remains in team-first order
    #---------------------------------------------------------------------------------------------------------------#
    def test_Penalties( self ):
        """Penalty shootout preserves team-first scores"""
        Match = { "Date": "2024-10-22", "Opponent": "CF Montréal", "Venue": "Home",
                  "Result": "D", "Goals For": "2", "Goals Against": "2",
                  "Shootout Result": "W", "Shootout Goals For": "5", "Shootout Goals Against": "4" }

        self.assertEqual( self.Naming.Generate_Name( Match ), "2024-10-22 - CF Montréal at Atlanta United, D 2-2 W (5-4) pens" )


#---------------------------------------------------------------------------------------------------------------#
# Test Entry Point
#---------------------------------------------------------------------------------------------------------------#
if ( __name__ == "__main__" ):
    unittest.main()
