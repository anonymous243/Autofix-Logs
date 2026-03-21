import typer
from pathlib import Path
from typing import Optional
from .utils import validate_file_path
from .parser import read_last_lines
from .extractor import ErrorExtractor
from .ai import AIService
from .formatter import Formatter
from .watcher import start_watching

app = typer.Typer(help="AutoFix Logs: AI-Powered Log Analyzer")

@app.command()
def analyze(
    file: str = typer.Argument(..., help="Path to the log file"),
    last: int = typer.Option(100, "--last", "-n", help="Number of last lines to analyze")
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

    ai_service = AIService()
    Formatter.print_header(f"Found {len(errors)} potential error segments. Analyzing...")
    
    # To avoid spamming API, we analyze the most recent error or summarize
    # For this CLI, we'll analyze the last one found as it's usually the most relevant
    latest_error = errors[-1]
    analysis = ai_service.analyze_error(latest_error['content'])
    Formatter.print_analysis(analysis)

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

if __name__ == "__main__":
    app()
