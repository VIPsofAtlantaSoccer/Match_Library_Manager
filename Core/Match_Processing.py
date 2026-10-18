
#---------------------------------------------------------------------------------------------------------------#
# Load Requirements
#---------------------------------------------------------------------------------------------------------------#
import csv
from datetime import datetime
from pathlib import Path


#---------------------------------------------------------------------------------------------------------------#
# Match Processing
# Read and validate match records from a team's CSV file
#---------------------------------------------------------------------------------------------------------------#
class Match_Processing:

    #---------------------------------------------------------------------------------------------------------------#
    # Initialize the match processor
    # Store the team identifier and resolve the CSV path relative to the project root
    #---------------------------------------------------------------------------------------------------------------#
    def __init__( self, Team_ID, Team_Data ):
        self.Team_ID = Team_ID
        self.Team_Name = Team_Data["Team_Name"]
        self.Source_File = Path( Team_Data["Source_File"] )

        if ( not self.Source_File.is_absolute() ):
            Project_Directory = Path( __file__ ).resolve().parent.parent
            self.Source_File = Project_Directory / self.Source_File

        self.Matches = []
        self.Warnings = []


    #---------------------------------------------------------------------------------------------------------------#
    # Read the entire CSV and validate each match record
    # Return all valid matches while retaining every original CSV field
    #---------------------------------------------------------------------------------------------------------------#
    def Load_Matches( self ):
        self.Matches = []
        self.Warnings = []

        with self.Source_File.open( "r", encoding = "utf-8-sig", newline = "" ) as File:
            Reader = csv.DictReader( File )

            if ( not Reader.fieldnames or "Date" not in Reader.fieldnames ):
                raise ValueError( f"{self.Team_ID}: CSV is missing the Date column" )

            for Line_Number, Row in enumerate( Reader, start = 2 ):
                if ( None in Row ):
                    self.Warnings.append( f"Line {Line_Number}: Too many CSV values" )
                    continue

                if ( not any( Value and Value.strip() for Value in Row.values() ) ):
                    continue

                Date_Str = ( Row.get( "Date" ) or "" ).strip()

                try:
                    Match_Date = datetime.strptime( Date_Str, "%Y-%m-%d" ).date()
                except ValueError:
                    self.Warnings.append( f"Line {Line_Number}: Invalid date '{Date_Str}'" )
                    continue

                Match = Row.copy()
                Match["Date"] = Match_Date.isoformat()

                self.Matches.append( Match )

        return self.Matches


    #---------------------------------------------------------------------------------------------------------------#
    # Return the number of successfully loaded match records
    #---------------------------------------------------------------------------------------------------------------#
    def Get_Match_Count( self ):
        return len( self.Matches )


    #---------------------------------------------------------------------------------------------------------------#
    # Return warnings generated while processing the CSV
    #---------------------------------------------------------------------------------------------------------------#
    def Get_Warnings( self ):
        return self.Warnings.copy()
