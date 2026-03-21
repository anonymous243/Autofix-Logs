import os
from pathlib import Path
from typing import List, Generator

def read_last_lines(file_path: Path, n: int = 100) -> List[str]:
    """
    Reads the last N lines of a file efficiently without loading the whole file.
    """
    lines = []
    buffer_size = 4096
    file_size = file_path.stat().st_size
    
    with open(file_path, 'rb') as f:
        if file_size == 0:
            return []
            
        f.seek(0, os.SEEK_END)
        pos = f.tell()
        
        while len(lines) <= n and pos > 0:
            read_size = min(pos, buffer_size)
            pos -= read_size
            f.seek(pos)
            chunk = f.read(read_size)
            
            # Count newlines in chunk
            lines = chunk.decode('utf-8', errors='ignore').splitlines() + lines
            
    return lines[-n:]

def stream_new_lines(file_path: Path) -> Generator[str, None, None]:
    """
    Generator that yields new lines added to a file (like tail -f).
    """
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        # Go to end of file
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                yield None
                continue
            yield line
