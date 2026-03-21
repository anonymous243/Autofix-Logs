import re
from typing import List, Optional, Dict

class ErrorExtractor:
    """
    Logic to identify and extract relevant error segments from logs.
    """
    
    # Common error patterns
    PATTERNS = {
        "python": r"Traceback \(most recent call last\):",
        "node": r"Error:.*?\n\s+at ",
        "java": r"(?i)Exception in thread \".*\"|[\w\.]+(Exception|Error):",
        "web_error": r"HTTP/\d\.\d\" (4\d{2}|5\d{2})| (4\d{2}|5\d{2}) \d+ ",
        "generic_error": r"(?i)error|exception|fatal|failed",
        "system": r"systemd\[\d+\]:.*?(?i)failed"
    }

    def __init__(self):
        self.current_traceback = []
        self.in_traceback = False

    def extract_errors(self, lines: List[str]) -> List[Dict[str, str]]:
        """
        Processes a list of lines and returns structured error segments.
        """
        errors = []
        temp_error = []
        collecting = False
        
        for line in lines:
            # Detect start of a Python traceback
            if re.search(self.PATTERNS["python"], line):
                if temp_error:
                    errors.append({"type": "log_segment", "content": "\n".join(temp_error)})
                temp_error = [line]
                collecting = True
                continue
            
            # Detect Java or Node.js error start
            if (re.search(self.PATTERNS["java"], line) or re.search(r"Error:", line)) and not collecting:
                if temp_error:
                    errors.append({"type": "log_segment", "content": "\n".join(temp_error)})
                temp_error = [line]
                collecting = True
                continue

            # Detect web errors (4xx, 5xx)
            if not collecting and re.search(self.PATTERNS["web_error"], line):
                errors.append({"type": "web_error", "content": line})
                continue

            # Detect generic errors if not already collecting a traceback
            if not collecting and re.search(self.PATTERNS["generic_error"], line):
                errors.append({"type": "single_line", "content": line})
                continue

            if collecting:
                temp_error.append(line)
                # Stop collecting if we see a line that doesn't look like part of a traceback
                # (e.g., a line that doesn't start with whitespace or is a new log timestamp)
                # Java/Node tracebacks usually have "at " or "Caused by:"
                is_traceback_line = line.strip().startswith(("at ", "Caused by:", "...")) or line.startswith((" ", "\t"))
                
                if len(temp_error) > 1 and not is_traceback_line and not re.search(r"^\d{4}-\d{2}-\d{2}", line):
                    # Check if it's just the end of the error message
                    if len(temp_error) > 20: # Safety cap
                        errors.append({"type": "traceback", "content": "\n".join(temp_error)})
                        temp_error = []
                        collecting = False

        if temp_error:
            errors.append({"type": "traceback", "content": "\n".join(temp_error)})
            
        return errors

    def is_critical(self, line: str) -> bool:
        """Heuristic to check if a single line is likely a critical error."""
        return any(re.search(pattern, line) for pattern in self.PATTERNS.values())
