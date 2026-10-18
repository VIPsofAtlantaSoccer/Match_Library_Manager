
#---------------------------------------------------------------------------------------------------------------#
# Load Requirements
#---------------------------------------------------------------------------------------------------------------#
import re


#---------------------------------------------------------------------------------------------------------------#
# Directory Naming
# Generate match directory names without modifying the filesystem
#---------------------------------------------------------------------------------------------------------------#
class Directory_Naming:

    #---------------------------------------------------------------------------------------------------------------#
    # Initialize the directory naming processor
    # Store the team name used when generating directory names
    #---------------------------------------------------------------------------------------------------------------#
    def __init__( self, Team_Name ):
        self.Team_Name = Team_Name


    #---------------------------------------------------------------------------------------------------------------#
    # Convert an optional score value into a non-negative integer
    # Return None when the value is missing or invalid
    #---------------------------------------------------------------------------------------------------------------#
    def Parse_Goals( self, Value ):
        Value = str( Value or "" ).strip()

        if ( not Value.isdigit() ):
            return None

        return int( Value )


    #---------------------------------------------------------------------------------------------------------------#
    # Remove characters that Windows does not permit in directory names
    #---------------------------------------------------------------------------------------------------------------#
    def Clean_Name( self, Value ):
        Value = re.sub( r'[<>:"/\\|?*\x00-\x1f]', "-", str( Value ) )
        return Value.strip( " .")


    #---------------------------------------------------------------------------------------------------------------#
    # Format the two teams based on the match venue
    # Handle matches where the opponent or venue is unknown
    #---------------------------------------------------------------------------------------------------------------#
    def Format_Teams( self, Match ):
        Opponent = ( Match.get( "Opponent" ) or "" ).strip()
        Venue = ( Match.get( "Venue" ) or "" ).strip().lower()

        if ( not Opponent ):
            return self.Team_Name

        if ( Venue == "home" ):
            return f"{Opponent} at {self.Team_Name}"

        if ( Venue == "away" ):
            return f"{self.Team_Name} at {Opponent}"

        return f"{self.Team_Name} vs {Opponent}"


    #---------------------------------------------------------------------------------------------------------------#
    # Format the match result, goals, and penalty shootout
    # Always place the configured team's score first
    #---------------------------------------------------------------------------------------------------------------#
    def Format_Result( self, Match ):
        Result = ( Match.get( "Result" ) or "" ).strip().upper()
        Goals_For = self.Parse_Goals( Match.get( "Goals For" ) )
        Goals_Against = self.Parse_Goals( Match.get( "Goals Against" ) )

        Parts = []

        if ( Result ):
            Parts.append( Result )

        if ( Goals_For is not None and Goals_Against is not None ):
            Parts.append( f"{Goals_For}-{Goals_Against}" )

        Shootout_Result = ( Match.get( "Shootout Result" ) or "" ).strip().upper()
        Shootout_For = self.Parse_Goals( Match.get( "Shootout Goals For" ) )
        Shootout_Against = self.Parse_Goals( Match.get( "Shootout Goals Against" ) )

        if ( Shootout_For is not None and Shootout_Against is not None ):
            Shootout = f"({Shootout_For}-{Shootout_Against}) pens"

            if ( Shootout_Result ):
                Shootout = f"{Shootout_Result} {Shootout}"

            Parts.append( Shootout )
        elif ( Shootout_Result ):
            Parts.append( f"{Shootout_Result} pens" )

        return " ".join( Parts )


    #---------------------------------------------------------------------------------------------------------------#
    # Format competition and round information
    # Omit the regular season designation to preserve the existing naming convention
    #---------------------------------------------------------------------------------------------------------------#
    def Format_Competition( self, Match ):
        Competition = ( Match.get( "Comp" ) or "" ).strip()
        Round = ( Match.get( "Round" ) or "" ).strip()

        if ( not Round or Round.lower() == "regular season" ):
            return ""

        return " ".join( Part for Part in [ Competition, Round ] if ( Part ) )


    #---------------------------------------------------------------------------------------------------------------#
    # Generate the complete directory name for one match
    # Return the name without creating or renaming directories
    #---------------------------------------------------------------------------------------------------------------#
    def Generate_Name( self, Match ):
        Date = ( Match.get( "Date" ) or "" ).strip()

        if ( not Date ):
            raise ValueError( "Match date is missing" )

        Directory_Name = f"{Date} - {self.Format_Teams( Match )}"

        Result = self.Format_Result( Match )
        Competition = self.Format_Competition( Match )

        if ( Result ):
            Directory_Name += f", {Result}"

        if ( Competition ):
            Directory_Name += f", {Competition}"

        return self.Clean_Name( Directory_Name )
