
#---------------------------------------------------------------------------------------------------------------#
# Load Requirements
#---------------------------------------------------------------------------------------------------------------#
import json
import re
from pathlib import Path


#---------------------------------------------------------------------------------------------------------------#
# Team Names
# Standardize team names using Name Variations from Player_Dictionary.json
#---------------------------------------------------------------------------------------------------------------#
class Team_Names:

    #---------------------------------------------------------------------------------------------------------------#
    # Initialize the team name lookup
    # Load the dictionary and identify conflicting name variations
    #---------------------------------------------------------------------------------------------------------------#
    def __init__( self, Dictionary_File ):
        self.Dictionary_File = Path( Dictionary_File )
        self.Name_Lookup = {}
        self.Alias_Conflicts = []

        self.Load_Dictionary()


    #---------------------------------------------------------------------------------------------------------------#
    # Normalize a team name for case-insensitive matching
    #---------------------------------------------------------------------------------------------------------------#
    def Normalize_Name_Key( self, Value ):
        Value_Text = str( Value or "" ).strip().lower()
        Value_Text = Value_Text.replace( "’", "'" )
        Value_Text = Value_Text.replace( "\u00a0", " " )
        Value_Text = re.sub( r"\s+", " ", Value_Text )

        return Value_Text


    #---------------------------------------------------------------------------------------------------------------#
    # Load team name variations and their standardized names
    # Report variations assigned to more than one team
    #---------------------------------------------------------------------------------------------------------------#
    def Load_Dictionary( self ):
        if ( not self.Dictionary_File.is_file() ):
            raise FileNotFoundError( f"Team dictionary not found: {self.Dictionary_File}" )

        with self.Dictionary_File.open( "r", encoding = "utf-8-sig" ) as File:
            Dictionary_Data = json.load( File )

        if ( not isinstance( Dictionary_Data, dict ) ):
            raise ValueError( "Team dictionary must contain a JSON object" )

        self.Name_Lookup = {}
        self.Alias_Conflicts = []

        for Section_Value in Dictionary_Data.values():
            if ( not isinstance( Section_Value, list ) ):
                continue

            for Record in Section_Value:
                if ( not isinstance( Record, dict ) ):
                    continue

                if ( str( Record.get( "Type", "" ) ).strip().lower() != "team" ):
                    continue

                Standard_Name = str( Record.get( "Name_Social", "" ) or "" ).strip()
                Name_Variations = Record.get( "Name Variations", [] )

                if ( not Standard_Name or not isinstance( Name_Variations, list ) ):
                    continue

                for Name_Variation in Name_Variations:
                    Alias_Key = self.Normalize_Name_Key( Name_Variation )

                    if ( not Alias_Key ):
                        continue

                    Existing_Name = self.Name_Lookup.get( Alias_Key )

                    if ( Existing_Name and Existing_Name != Standard_Name ):
                        Conflict = ( Name_Variation, Existing_Name, Standard_Name )

                        if ( Conflict not in self.Alias_Conflicts ):
                            self.Alias_Conflicts.append( Conflict )

                        continue

                    self.Name_Lookup[Alias_Key] = Standard_Name


    #---------------------------------------------------------------------------------------------------------------#
    # Return the standardized team name from Name Variations
    # Preserve the original name when no match is found
    #---------------------------------------------------------------------------------------------------------------#
    def Standardize( self, Team_Name ):
        Team_Name_Text = str( Team_Name or "" ).strip()
        Team_Name_Key = self.Normalize_Name_Key( Team_Name_Text )

        return self.Name_Lookup.get( Team_Name_Key, Team_Name_Text )


    #---------------------------------------------------------------------------------------------------------------#
    # Determine whether two names identify the same team
    # Compare their standardized names
    #---------------------------------------------------------------------------------------------------------------#
    def Is_Same_Team( self, First_Team, Second_Team ):
        First_Name = self.Standardize( First_Team )
        Second_Name = self.Standardize( Second_Team )

        return self.Normalize_Name_Key( First_Name ) == self.Normalize_Name_Key( Second_Name )
