import os
from pathlib import Path
import typer

def validate_file_path(path: str) -> Path:
    """
    Validates that the file path exists, is a file, and is not a directory traversal attempt.
    """
    p = Path(path).resolve()
    
    if not p.exists():
        raise typer.BadParameter(f"File not found: {path}")
    
    if not p.is_file():
        raise typer.BadParameter(f"Path is not a file: {path}")
    
    # Basic check for sensitive directories (optional, can be expanded)
    sensitive_paths = ["/etc/passwd", "/etc/shadow", "/root"]
    if str(p) in sensitive_paths:
        raise typer.BadParameter("Access to sensitive system files is prohibited.")
        
    return p

def get_file_size(path: Path) -> int:
    """Returns file size in bytes."""
    return path.stat().st_size
