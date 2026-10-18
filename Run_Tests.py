
#---------------------------------------------------------------------------------------------------------------#
# Load Requirements
#---------------------------------------------------------------------------------------------------------------#
import sys
import unittest

from pathlib import Path
from rich.console import Console
from rich.text import Text


#---------------------------------------------------------------------------------------------------------------#
# Rich Test Result
# Display tests grouped by category, with readable results and failure details
#---------------------------------------------------------------------------------------------------------------#
class Rich_Test_Result( unittest.TestResult ):

    #---------------------------------------------------------------------------------------------------------------#
    # Initialize the test result formatter
    # Track the current group and configure Rich console output
    #---------------------------------------------------------------------------------------------------------------#
    def __init__( self ):
        super().__init__()

        self.Console = Console()
        self.Current_Group = None


    #---------------------------------------------------------------------------------------------------------------#
    # Display the test category when beginning a new group
    #---------------------------------------------------------------------------------------------------------------#
    def startTest( self, Test ):
        super().startTest( Test )

        Group = Test.__class__.__name__.removeprefix( "Test_" ).replace( "_", " " )

        if ( Group != self.Current_Group ):
            self.Current_Group = Group
            self.Console.print( f"\n[bold cyan]{Group}[/bold cyan]" )


    #---------------------------------------------------------------------------------------------------------------#
    # Return the readable test description, falling back to the method name
    #---------------------------------------------------------------------------------------------------------------#
    def Get_Description( self, Test ):
        Description = Test.shortDescription()

        if ( Description ):
            return Description

        return Test._testMethodName.removeprefix( "test_" ).replace( "_", " " )


    #---------------------------------------------------------------------------------------------------------------#
    # Display a green checkmark for a successful test
    #---------------------------------------------------------------------------------------------------------------#
    def addSuccess( self, Test ):
        super().addSuccess( Test )
        self.Console.print( f"  [green]✔[/green] {self.Get_Description( Test )}" )


    #---------------------------------------------------------------------------------------------------------------#
    # Display a failed test and its assertion details
    #---------------------------------------------------------------------------------------------------------------#
    def addFailure( self, Test, Error ):
        super().addFailure( Test, Error )
        self.Console.print( f"  [red]✘[/red] {self.Get_Description( Test )}" )
        self.Display_Error( Test, Error )


    #---------------------------------------------------------------------------------------------------------------#
    # Display a test that failed because of an unexpected exception
    #---------------------------------------------------------------------------------------------------------------#
    def addError( self, Test, Error ):
        super().addError( Test, Error )
        self.Console.print( f"  [red]✘[/red] {self.Get_Description( Test )} [red](Error)[/red]" )
        self.Display_Error( Test, Error )


    #---------------------------------------------------------------------------------------------------------------#
    # Display a skipped test and its reason
    #---------------------------------------------------------------------------------------------------------------#
    def addSkip( self, Test, Reason ):
        super().addSkip( Test, Reason )
        self.Console.print( f"  [yellow]○[/yellow] {self.Get_Description( Test )} [dim](Skipped: {Reason})[/dim]" )


    #---------------------------------------------------------------------------------------------------------------#
    # Display the relevant exception message without printing a full traceback
    #---------------------------------------------------------------------------------------------------------------#
    def Display_Error( self, Test, Error ):
        Error_Type, Error_Value, Error_Traceback = Error
        Error_Message = str( Error_Value ).strip()

        if ( not Error_Message ):
            Error_Message = Error_Type.__name__

        for Line in Error_Message.splitlines():
            self.Console.print( Text( f"      {Line}", style = "red" ) )


#---------------------------------------------------------------------------------------------------------------#
# Run Tests
# Discover and execute all automated tests, then display a summary
# Return a nonzero exit code when tests fail
#---------------------------------------------------------------------------------------------------------------#
def Run_Tests():
    Project_Directory = Path( __file__ ).resolve().parent
    Tests_Directory = Project_Directory / "Tests"

    Console_Output = Console()
    Console_Output.print( "\n[bold]Match Library Manager - Tests[/bold]" )

    Test_Loader = unittest.TestLoader()
    Test_Suite = Test_Loader.discover( start_dir = str( Tests_Directory ), pattern = "test_*.py", top_level_dir = str( Project_Directory ) )

    Result = Rich_Test_Result()
    Test_Suite.run( Result )

    Passed = Result.testsRun - len( Result.failures ) - len( Result.errors ) - len( Result.skipped ) - len( Result.expectedFailures ) - len( Result.unexpectedSuccesses )

    Console_Output.print( "\n[bold]Test Summary[/bold]" )
    Console_Output.print( f"  [green]✔ {Passed} Passed[/green]" )
    Console_Output.print( f"  [red]✘ {len( Result.failures )} Failed[/red]" )
    Console_Output.print( f"  [red]✘ {len( Result.errors )} Errors[/red]" )

    if ( Result.skipped ):
        Console_Output.print( f"  [yellow]○ {len( Result.skipped )} Skipped[/yellow]" )

    if ( Result.expectedFailures or Result.unexpectedSuccesses ):
        Console_Output.print( f"  Expected failures: {len( Result.expectedFailures )}" )
        Console_Output.print( f"  Unexpected successes: {len( Result.unexpectedSuccesses )}" )

    Console_Output.print()

    if ( Result.wasSuccessful() and Result.testsRun > 0 ):
        Console_Output.print( "[bold green]All tests passed.[/bold green]" )
        return 0

    Console_Output.print( "[bold red]Tests did not all pass.[/bold red]" )
    return 1


#---------------------------------------------------------------------------------------------------------------#
# Application Entry Point
#---------------------------------------------------------------------------------------------------------------#
if ( __name__ == "__main__" ):
    sys.exit( Run_Tests() )
