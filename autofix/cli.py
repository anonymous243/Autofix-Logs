import typer
from pathlib import Path
from .splash import show_banner
from typing import Optional
from .utils import validate_file_path
from .parser import read_last_lines
from .extractor import ErrorExtractor
from .ai import AIService
from .formatter import Formatter
from .watcher import start_watching
import sys
import os

__version__ = "0.2.0"

# ✅ IMPORTANT: allow running without command
app = typer.Typer(
    help="AutoFix Logs: AI-Powered Log Analyzer",
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True
)


# --------------------------
# VERSION FLAG
# --------------------------
def version_callback(value: bool):
    if value:
        typer.echo(f"AutoFix Logs v{__version__}")
        raise typer.Exit()


# --------------------------
# MAIN CALLBACK (BANNER FIX)
# --------------------------
@app.callback()
def main(
    ctx: typer.Context,
    version_flag: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit.",
        callback=version_callback,
        is_eager=True,
    ),
):
    """
    AutoFix Logs CLI entry point
    """

    # ✅ Show banner ONLY if no command is given
    if ctx.invoked_subcommand is None and not ctx.resilient_parsing:
        show_banner()


# --------------------------
# ANALYZE COMMAND
# --------------------------
@app.command()
def analyze(
    file: str = typer.Argument(..., help="Path to the log file"),
    last: int = typer.Option(100, "--last", "-n", help="Number of last lines to analyze"),
    quick: bool = typer.Option(False, "--quick", "-q", help="Show a quick summary of the error and fix"),
    summary: bool = typer.Option(False, "--summary", "-s", help="Show a summary report of errors found"),
    top: int = typer.Option(1, "--top", "-t", help="Number of top unique errors to analyze"),
):
    """
    Analyze a log file for errors and provide fixes.
    """
    file_path = validate_file_path(file)
    Formatter.print_info(f"Reading last {last} lines of {file}...")

    lines = read_last_lines(file_path, last)
    extractor = ErrorExtractor()
    errors = extractor.extract_errors(lines)

    if not errors:
        Formatter.print_info("No clear errors detected in the specified range.")
        return

    if summary:
        Formatter.print_summary(errors)
        return

    ai_service = AIService()
    
    to_analyze = errors[:top]
    if len(to_analyze) == 1:
        Formatter.print_header(f"Found {len(errors)} unique error blocks. Analyzing the most critical one...")
    else:
        Formatter.print_header(f"Found {len(errors)} unique error blocks. Analyzing the top {len(to_analyze)}...")

    for i, err in enumerate(to_analyze):
        if len(to_analyze) > 1:
            Formatter.print_info(f"--- Analyzing Error {i + 1} ---")
            
        analysis = ai_service.analyze_error(err["content"])

        if quick:
            Formatter.print_quick(analysis)
        else:
            Formatter.print_analysis(analysis)


# --------------------------
# WATCH COMMAND
# --------------------------
@app.command()
def watch(
    file: str = typer.Argument(..., help="Path to the log file to watch")
):
    """
    Continuously monitor a log file for new errors.
    """
    file_path = validate_file_path(file)
    ai_service = AIService()
    extractor = ErrorExtractor()
    start_watching(file_path, ai_service, extractor)


# --------------------------
# DOCTOR COMMAND
# --------------------------
@app.command()
def doctor():
    """
    Check system setup and dependencies.
    """
    Formatter.print_header("System Doctor Check")
    
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    Formatter.print_info(f"Python: {python_version}")
    
    if os.getenv("GEMINI_API_KEY"):
        Formatter.print_info("GEMINI_API_KEY: Set ✅")
    else:
        Formatter.print_error("GEMINI_API_KEY: Not Set ❌")
        
    try:
        import rich
        Formatter.print_info("rich: Installed ✅")
    except ImportError:
        Formatter.print_error("rich: Missing ❌")
        
    try:
        import pyfiglet
        Formatter.print_info("pyfiglet: Installed ✅")
    except ImportError:
        Formatter.print_error("pyfiglet: Missing ❌")


# --------------------------
# VERSION COMMAND
# --------------------------
@app.command()
def version():
    """
    Show AutoFix Logs version.
    """
    typer.echo(f"AutoFix Logs v{__version__}")


# --------------------------
# ENTRY POINT
# --------------------------
def run():
    app()


if __name__ == "__main__":
    run()