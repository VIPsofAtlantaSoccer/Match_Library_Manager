
#---------------------------------------------------------------------------------------------------------------#
# Load Requirements
#---------------------------------------------------------------------------------------------------------------#
from pathlib import Path
import tomllib


#---------------------------------------------------------------------------------------------------------------#
# Configuration Manager
#---------------------------------------------------------------------------------------------------------------#
class Config:

    #---------------------------------------------------------------------------------------------------------------#
    # Initialize the configuration manager
    # Load and validate the TOML configuration file
    #---------------------------------------------------------------------------------------------------------------#
    def __init__( self, Config_Path = None ):
        if ( Config_Path is None ):
            Config_Path = Path( __file__ ).resolve().parent.parent / "Config.toml"

        self.Config_Path = Path( Config_Path )
        self.General = {}
        self.Teams = {}

        self.Load_Config()


    #---------------------------------------------------------------------------------------------------------------#
    # Load the TOML configuration file
    # Validate the general settings and team definitions
    #---------------------------------------------------------------------------------------------------------------#
    def Load_Config( self ):
        if ( not self.Config_Path.is_file() ):
            raise FileNotFoundError( f"Configuration file not found: {self.Config_Path}" )

        try:
            with self.Config_Path.open( "rb" ) as File:
                Data = tomllib.load( File )
        except tomllib.TOMLDecodeError as Error:
            raise ValueError( f"Invalid TOML configuration: {Error}" ) from Error

        self.General = Data.get( "General", {} )
        self.Teams = Data.get( "Teams", {} )

        if ( not isinstance( self.General, dict ) ):
            raise ValueError( "Invalid [General] configuration" )

        if ( not isinstance( self.Teams, dict ) or not self.Teams ):
            raise ValueError( "No teams defined in Config.toml" )

        if ( not isinstance( self.General.get( "Dry_Run" ), bool ) ):
            raise ValueError( "General.Dry_Run must be true or false" )

        for Team_ID, Team_Data in self.Teams.items():
            if ( not isinstance( Team_Data, dict ) ):
                raise ValueError( f"Invalid configuration for team: {Team_ID}" )

            for Field in [ "Team_Name", "Library_Directory", "Source_File" ]:
                if ( not isinstance( Team_Data.get( Field ), str ) or not Team_Data[Field].strip() ):
                    raise ValueError( f"{Team_ID}: Missing or invalid {Field}" )

            if ( not isinstance( Team_Data.get( "Enabled" ), bool ) ):
                raise ValueError( f"{Team_ID}: Enabled must be true or false" )


    #---------------------------------------------------------------------------------------------------------------#
    # Return general application configuration
    #---------------------------------------------------------------------------------------------------------------#
    def Get_General( self ):
        return self.General.copy()


    #---------------------------------------------------------------------------------------------------------------#
    # Return the configuration for a specific team
    # Raise an error if the team does not exist
    #---------------------------------------------------------------------------------------------------------------#
    def Get_Team( self, Team_ID ):
        if ( Team_ID not in self.Teams ):
            raise ValueError( f"Unknown team: {Team_ID}" )

        return self.Teams[Team_ID].copy()


    #---------------------------------------------------------------------------------------------------------------#
    # Return configurations for all enabled teams
    #---------------------------------------------------------------------------------------------------------------#
    def Get_Enabled_Teams( self ):
        return {
            Team_ID: Team_Data.copy()
            for Team_ID, Team_Data in self.Teams.items()
            if ( Team_Data["Enabled"] )
        }
