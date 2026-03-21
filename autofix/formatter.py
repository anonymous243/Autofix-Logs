from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()

class Formatter:
    @staticmethod
    def print_header(text: str):
        console.print(f"\n[bold blue]>>> {text}[/bold blue]\n")

    @staticmethod
    def print_analysis(analysis: dict):
        """
        Prints the AI analysis in a beautiful CLI format.
        """
        # Error Type & Root Cause
        console.print(Panel(
            f"[bold red]Type:[/bold red] {analysis.get('error_type', 'Unknown')}\n"
            f"[bold yellow]Root Cause:[/bold yellow] {analysis.get('root_cause', 'Unknown')}",
            title="[bold red]Error Detected[/bold red]",
            border_style="red",
            box=box.ROUNDED
        ))

        # Explanation
        console.print(f"\n[bold cyan]Explanation:[/bold cyan]\n{analysis.get('explanation', 'No explanation provided.')}")

        # Fix Steps
        if analysis.get('fix_steps'):
            console.print("\n[bold green]Fix Steps:[/bold green]")
            for i, step in enumerate(analysis['fix_steps'], 1):
                console.print(f"  {i}. {step}")

        # Commands
        if analysis.get('commands'):
            console.print("\n[bold magenta]Suggested Commands:[/bold magenta]")
            for cmd in analysis['commands']:
                console.print(Panel(f"[white]{cmd}[/white]", box=box.SQUARE, border_style="dim"))

    @staticmethod
    def print_info(text: str):
        console.print(f"[dim]INFO: {text}[/dim]")

    @staticmethod
    def print_error(text: str):
        console.print(f"[bold red]ERROR: {text}[/bold red]")
