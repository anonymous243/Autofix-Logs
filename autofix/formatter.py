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
        console.print("\n🚨 [bold red]Error Detected[/bold red]")
        console.print("────────────────────────")
        console.print(f"[bold]Type:[/bold] {analysis.get('error_type', 'Unknown')}")
        
        conf = analysis.get("confidence", 0)
        if conf >= 80:
            console.print(f"[bold]Confidence:[/bold] [bold green]High ({conf}%)[/bold green]\n")
        elif conf >= 50:
            console.print(f"[bold]Confidence:[/bold] [bold yellow]Medium ({conf}%)[/bold yellow]\n")
        else:
            console.print(f"[bold]Confidence:[/bold] [bold red]Low ({conf}%)[/bold red]\n")
        
        console.print("💡 [bold yellow]Cause:[/bold yellow]")
        console.print(f"{analysis.get('root_cause', 'Unknown')}\n")
        
        console.print("📖 [bold cyan]Explanation:[/bold cyan]")
        console.print(f"{analysis.get('explanation', 'No explanation provided.')}\n")
        
        if analysis.get('fix_command'):
            console.print("⚡ [bold magenta]Fix Command:[/bold magenta]")
            console.print(f"{analysis.get('fix_command')}")
        console.print()

    @staticmethod
    def print_quick(analysis: dict):
        conf = analysis.get("confidence", 0)
        c_str = "🟢" if conf >= 80 else "🟡" if conf >= 50 else "🔴"
        console.print(f"Error: {analysis.get('error_type', 'Unknown')} {c_str}")
        if analysis.get('fix_command'):
            console.print(f"Fix: {analysis.get('fix_command')}")

    @staticmethod
    def print_summary(errors: list):
        console.print(f"\n[bold]Total Errors Found:[/bold] {len(errors)}")
        types_count = {}
        for error in errors:
            etype = error.get('type', 'unknown')
            types_count[etype] = types_count.get(etype, 0) + 1
        console.print("[bold]Breakdown by Type:[/bold]")
        for etype, count in types_count.items():
            console.print(f"  - {etype}: {count}")
        console.print()

    @staticmethod
    def print_info(text: str):
        console.print(f"[dim]INFO: {text}[/dim]")

    @staticmethod
    def print_error(text: str):
        console.print(f"[bold red]ERROR: {text}[/bold red]")
