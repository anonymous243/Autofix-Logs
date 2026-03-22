from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def show_banner():
    # Big ASCII Title
    try:
        from pyfiglet import figlet_format
        banner = figlet_format("AutoFix Logs", font="slant")
        console.print(f"[bold cyan]{banner}[/bold cyan]")
    except ImportError:
        console.print("\n[bold cyan]=== AutoFix Logs ===[/bold cyan]\n")

    # Info panel
    tips = Text()

    tips.append("🚀 AI-Powered Log Analyzer\n\n", style="bold green")

    tips.append("Core Commands:\n", style="bold white")
    tips.append("  autofix analyze <file>   ", style="cyan")
    tips.append("Analyze logs and fix errors\n", style="dim")
    
    tips.append("  autofix watch <file>     ", style="cyan")
    tips.append("Monitor logs in real-time\n\n", style="dim")

    tips.append("Utility:\n", style="bold white")
    tips.append("  autofix doctor           ", style="cyan")
    tips.append("Check system setup\n", style="dim")
    
    tips.append("  autofix version          ", style="cyan")
    tips.append("Show version\n", style="dim")
    
    tips.append("  autofix --help           ", style="cyan")
    tips.append("Show help\n\n", style="dim")

    tips.append("Fix errors instantly ⚡\n", style="bold yellow")

    console.print(
        Panel(
            tips,
            title="Welcome to AutoFix Logs",
            border_style="green"
        )
    )