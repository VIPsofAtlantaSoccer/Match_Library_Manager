
#---------------------------------------------------------------------------------------------------------------#
# Load Requirements
#---------------------------------------------------------------------------------------------------------------#
import re
from pathlib import Path

from Core.Team_Names import Team_Names

#---------------------------------------------------------------------------------------------------------------#
# Library Management
# Create and rename match directories while protecting existing content
#---------------------------------------------------------------------------------------------------------------#
class Library_Management:

    #---------------------------------------------------------------------------------------------------------------#
    # Initialize the library manager
    # Store the library path, configured team, dictionary lookup, and dry-run setting
    #---------------------------------------------------------------------------------------------------------------#
    def __init__( self, Library_Directory, Team_Name, Team_Names, Dry_Run = True ):
        self.Library_Directory = Path( Library_Directory )
        self.Team_Name = Team_Name
        self.Team_Names = Team_Names
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
    # Create or rename a match directory using the date and opponent
    # Preserve existing files and report ambiguous matches without changing them
    #---------------------------------------------------------------------------------------------------------------#
    def Process_Match( self, Directory_Name ):
        Match_Date = Directory_Name[:10]

        if ( not re.fullmatch( r"\d{4}-\d{2}-\d{2}", Match_Date ) or not Directory_Name.startswith( f"{Match_Date} - " ) ):
            raise ValueError( f"Invalid directory name: {Directory_Name}" )

        Year_Directory = self.Library_Directory / Match_Date[:4]
        Target_Directory = Year_Directory / Directory_Name
        Opponent = self.Get_Directory_Opponent( Directory_Name )

        Source_Directory, Conflict = self.Find_Existing_Match( Match_Date, Opponent )

        if ( Conflict ):
            return {
                "Status": "CONFLICT",
                "Source": None,
                "Target": Target_Directory,
                "Message": Conflict,
            }

        if ( Source_Directory is None ):
            if ( Target_Directory.exists() ):
                return {
                    "Status": "CONFLICT",
                    "Source": None,
                    "Target": Target_Directory,
                    "Message": "Target directory already exists",
                }

            if ( not self.Dry_Run ):
                Target_Directory.mkdir( parents = True, exist_ok = False )

            return {
                "Status": "CREATE",
                "Source": None,
                "Target": Target_Directory,
                "Message": "Directory created" if ( not self.Dry_Run ) else "Directory would be created",
            }

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



    #---------------------------------------------------------------------------------------------------------------#
    # Extract the opponent from an existing match directory name
    # Identify the configured team using standardized dictionary names
    # Return None when the directory does not identify an opponent
    #---------------------------------------------------------------------------------------------------------------#
    def Get_Directory_Opponent( self, Directory_Name ):
        Match_Details = Directory_Name[10:].strip()

        if ( Match_Details.startswith( "-" ) ):
            Match_Details = Match_Details[1:].strip()

        Match_Details = Match_Details.split( ",", 1 )[0].strip()

        if ( self.Team_Names.Is_Same_Team( Match_Details, self.Team_Name ) ):
            return None

        for Separator in [ " at ", " vs " ]:
            if ( Separator in Match_Details ):
                Team_1, Team_2 = Match_Details.split( Separator, 1 )

                if ( self.Team_Names.Is_Same_Team( Team_1, self.Team_Name ) ):
                    return self.Team_Names.Standardize( Team_2 )

                if ( self.Team_Names.Is_Same_Team( Team_2, self.Team_Name ) ):
                    return self.Team_Names.Standardize( Team_1 )

        return None



    #---------------------------------------------------------------------------------------------------------------#
    # Identify the existing directory for a match using its date and opponent
    # Match either team order and preserve support for incomplete directory names
    #---------------------------------------------------------------------------------------------------------------#
    def Find_Existing_Match( self, Match_Date, Opponent ):
        Existing_Directories = self.Find_Match_Directories( Match_Date )

        Identified_Matches = []
        Unidentified_Matches = []

        for Directory in Existing_Directories:
            Existing_Opponent = self.Get_Directory_Opponent( Directory.name )

            if ( Existing_Opponent is None ):
                Unidentified_Matches.append( Directory )
            elif ( Opponent and self.Team_Names.Is_Same_Team( Existing_Opponent, Opponent ) ):
                Identified_Matches.append( Directory )

        if ( len( Identified_Matches ) == 1 ):
            return Identified_Matches[0], None

        if ( len( Identified_Matches ) > 1 ):
            return None, f"Multiple directories match {Match_Date} against {Opponent}"

        if ( len( Unidentified_Matches ) == 1 ):
            return Unidentified_Matches[0], None

        if ( len( Unidentified_Matches ) > 1 ):
            return None, f"Multiple unidentified directories exist for {Match_Date}"

        if ( not Opponent and Existing_Directories ):
            return None, f"Cannot identify the opponent for {Match_Date}"

        return None, None

