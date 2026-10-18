
#---------------------------------------------------------------------------------------------------------------#
# Load Requirements
# python -m pip install --upgrade package_name
# python -m pip freeze > requirements.txt
#---------------------------------------------------------------------------------------------------------------#
from rich import print
from rich.traceback import install
from pathlib import Path


from Core.Config import Config
from Core.Match_Processing import Match_Processing
from Core.Directory_Naming import Directory_Naming
from Core.Library_Management import Library_Management

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
    # Process match directories and display the results for one team
    # Report changes, conflicts, and warnings without listing unchanged directories
    #---------------------------------------------------------------------------------------------------------------#
    def Display_Matches( self, Team_ID, Matches, Warnings ):
        Team_Data = self.Configuration.Get_Team( Team_ID )
        Naming = Directory_Naming( Team_Data["Team_Name"] )

        Project_Directory = Path( __file__ ).resolve().parent
        Library_Directory = Path( Team_Data["Library_Directory"] )

        if ( not Library_Directory.is_absolute() ):
            Library_Directory = Project_Directory / Library_Directory

        Dry_Run = self.Configuration.General["Dry_Run"]
        Library = Library_Management( Library_Directory, Dry_Run )

        Counts = { "CREATE": 0, "RENAME": 0, "UNCHANGED": 0, "CONFLICT": 0, "ERROR": 0 }

        print( f"\n[bold]{Team_ID}[/bold] - {len( Matches )} matches loaded" )
        print( f"  Mode: {'DRY RUN' if ( Dry_Run ) else 'LIVE'}" )

        for Match in Matches:
            try:
                Directory_Name = Naming.Generate_Name( Match )
                Result = Library.Process_Match( Directory_Name )
                Status = Result["Status"]

                Counts[Status] += 1

                if ( Status == "CREATE" ):
                    Action = "Would create" if ( Dry_Run ) else "Created"
                    Relative_Target = Result["Target"].relative_to( Library_Directory )
                    print( f"  [bold green]✓[/bold green]  {Action}: {Team_Data['Library_Directory']}\\{Relative_Target}" )

                elif ( Status == "RENAME" ):
                    Action = "Would rename" if ( Dry_Run ) else "Renamed"
                    Relative_Source = Result["Source"].relative_to( Library_Directory )
                    Relative_Target = Result["Target"].relative_to( Library_Directory )

                    print( f"  [cyan]➜[/cyan]  {Action}:" )
                    print( f"      From: {Team_Data['Library_Directory']}\\{Relative_Source}" )
                    print( f"      To:   {Team_Data['Library_Directory']}\\{Relative_Target}" )

                elif ( Status == "CONFLICT" ):
                    print( f"  [red]✘  Conflict:[/red] {Result['Message']}" )

            except ( ValueError, OSError ) as Error:
                Counts["ERROR"] += 1
                Warnings.append( f"{Match.get( 'Date', '' )}: {Error}" )

        for Warning in Warnings:
            print( f"  [yellow]⚠  Warning: {Warning}[/yellow]" )

        print( "\n[bold]  Summary[/bold]" )
        print( f"  {'Would create' if ( Dry_Run ) else 'Created'}: {Counts['CREATE']}" )
        print( f"  {'Would rename' if ( Dry_Run ) else 'Renamed'}: {Counts['RENAME']}" )
        print( f"  Unchanged: {Counts['UNCHANGED']}" )
        print( f"  Conflicts: {Counts['CONFLICT']}" )
        print( f"  Errors: {Counts['ERROR']}" )


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
