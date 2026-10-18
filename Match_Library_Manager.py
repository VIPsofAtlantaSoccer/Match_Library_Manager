
#---------------------------------------------------------------------------------------------------------------#
# Load Requirements
# python -m pip install --upgrade package_name
# python -m pip freeze > requirements.txt
#---------------------------------------------------------------------------------------------------------------#
from rich import print
from rich.traceback import install

from Core.Config import Config
from Core.Match_Processing import Match_Processing


#---------------------------------------------------------------------------------------------------------------#
# Enable Rich tracebacks for unexpected errors
#---------------------------------------------------------------------------------------------------------------#
install( show_locals = False, width = 140 )


#---------------------------------------------------------------------------------------------------------------#
# Match Library Manager
# Coordinate application configuration and match processing
#---------------------------------------------------------------------------------------------------------------#
class Match_Library_Manager:

    #---------------------------------------------------------------------------------------------------------------#
    # Initialize the application and load its configuration
    #---------------------------------------------------------------------------------------------------------------#
    def __init__( self ):
        self.Configuration = Config()


    #---------------------------------------------------------------------------------------------------------------#
    # Display general configuration and configured teams
    #---------------------------------------------------------------------------------------------------------------#
    def Display_Configuration( self ):
        print( "\n[bold]Match Library Manager[/bold]\n" )
        print( f"Dry Run: {self.Configuration.General['Dry_Run']}" )
        print( f"Log Directory: {self.Configuration.General['Log_Directory']}\n" )

        print( "[bold]Configured Teams:[/bold]" )

        for Team_ID, Team_Data in self.Configuration.Teams.items():
            Status = "Enabled" if ( Team_Data["Enabled"] ) else "Disabled"

            print( f"\n{Team_ID} - {Team_Data['Team_Name']}" )
            print( f"  Status: {Status}" )
            print( f"  Library: {Team_Data['Library_Directory']}" )
            print( f"  Source: {Team_Data['Source_File']}" )

        print( f"\nEnabled Teams: {len( self.Configuration.Get_Enabled_Teams() )}" )


    #---------------------------------------------------------------------------------------------------------------#
    # Display the match processing summary and any warnings for an individual team
    #---------------------------------------------------------------------------------------------------------------#
    def Display_Matches( self, Team_ID, Matches, Warnings ):
        print( f"\n[bold]{Team_ID}[/bold] - {len( Matches )} matches loaded" )

        for Warning in Warnings:
            print( f"  [yellow]Warning: {Warning}[/yellow]" )


    #---------------------------------------------------------------------------------------------------------------#
    # Read and process CSV match records for all enabled teams
    # Continue processing other teams if a source file fails
    #---------------------------------------------------------------------------------------------------------------#
    def Process_Matches( self ):
        print( "\n[bold]Processing Match Files:[/bold]" )

        for Team_ID, Team_Data in self.Configuration.Get_Enabled_Teams().items():
            Processor = Match_Processing( Team_ID, Team_Data )

            try:
                Matches = Processor.Load_Matches()
            except ( ValueError, OSError, UnicodeError ) as Error:
                print( f"\n[bold red]{Team_ID}: {Error}[/bold red]" )
                continue

            self.Display_Matches( Team_ID, Matches, Processor.Get_Warnings() )


    #---------------------------------------------------------------------------------------------------------------#
    # Execute the application
    #---------------------------------------------------------------------------------------------------------------#
    def Main( self ):
        self.Display_Configuration()
        self.Process_Matches()


#---------------------------------------------------------------------------------------------------------------#
# Application Entry Point
#---------------------------------------------------------------------------------------------------------------#
if ( __name__ == "__main__" ):
    try:
        Application = Match_Library_Manager()
        Application.Main()
    except ( ValueError, FileNotFoundError ) as Error:
        print( f"\n[bold red]Configuration Error:[/bold red] {Error}\n" )
