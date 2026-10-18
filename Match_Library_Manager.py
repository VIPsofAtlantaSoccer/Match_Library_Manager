
#---------------------------------------------------------------------------------------------------------------#
# Load Requirements
# python -m pip install --upgrade package_name
# python -m pip freeze > requirements.txt
#---------------------------------------------------------------------------------------------------------------#
from rich import print
from rich.traceback import install
from Core.Config import Config

#---------------------------------------------------------------------------------------------------------------#
# Enable Rich tracebacks for clearer error reporting
#---------------------------------------------------------------------------------------------------------------#
install( show_locals = False, width = 140 )



#---------------------------------------------------------------------------------------------------------------#
# Main application
# Load configuration and display configured teams
#---------------------------------------------------------------------------------------------------------------#
def Main():
    try:
        Configuration = Config()
    except ( ValueError, FileNotFoundError ) as Error:
        print( f"\n[bold red]Configuration Error:[/bold red] {Error}\n" )
        return

    print( "\n[bold]Match Library Manager[/bold]\n" )
    print( f"Dry Run: {Configuration.General['Dry_Run']}" )
    print( f"Log Directory: {Configuration.General['Log_Directory']}\n" )

    print( "[bold]Configured Teams:[/bold]" )

    for Team_ID, Team_Data in Configuration.Teams.items():
        Status = "Enabled" if ( Team_Data["Enabled"] ) else "Disabled"

        print( f"\n{Team_ID} - {Team_Data['Team_Name']}" )
        print( f"  Status: {Status}" )
        print( f"  Library: {Team_Data['Library_Directory']}" )
        print( f"  Source: {Team_Data['Source_File']}" )

    print( f"\nEnabled Teams: {len( Configuration.Get_Enabled_Teams() )}" )

#---------------------------------------------------------------------------------------------------------------#
# Application Entry Point
#---------------------------------------------------------------------------------------------------------------#
if ( __name__ == "__main__" ):
    Main()
