import re
from typing import List, Dict

class ErrorExtractor:
    def __init__(self):
        # ✅ Use IGNORECASE securely
        self.patterns = {
            "python": re.compile(
                r"Traceback \(most recent call last\):|\bException\b|\bError\b",
                re.IGNORECASE,
            ),
            "node": re.compile(r"\bError\b|^\s*at\s+\w+", re.IGNORECASE),
            "system": re.compile(r"\bERROR\b|\bFATAL\b|\bCRITICAL\b", re.IGNORECASE),
        }

        # Recognize when a new log entry begins (timestamps)
        self.boundary_pattern = re.compile(
            r"^\d{4}-\d{2}-\d{2}"               # 2023-11-12
            r"|^\w{3} \d{2} \d{2}:\d{2}:\d{2}"  # Oct 12 10:00:00
            r"|^\[\d{4}-"                       # [2023-
            r"|^\d{2}/\w{3}/\d{4}"              # 12/Oct/2023
        )

    def is_error_line(self, line: str) -> bool:
        return any(pattern.search(line) for pattern in self.patterns.values())

    def is_boundary(self, line: str) -> bool:
        # Ignore wrapped/indented stack traces, ensuring we don't prematurely stop capturing
        if line.startswith(" ") or line.startswith("\t"):
            return False
        return bool(self.boundary_pattern.search(line))

    def _deduplicate_and_extract_root(self, errors: List[Dict]) -> List[Dict]:
        unique = {}
        for err in errors:
            content = err["content"]
            lines = content.split("\n")
            
            # Focus on ROOT ERROR (Skip intermediate cascading noise)
            # Especially for huge tracebacks, last ~10 lines have the actual failing logic
            if len(lines) > 20:
                content = "\n".join(lines[:5] + ["...[truncated intermediate noise]..."] + lines[-10:])
            
            # Dict key-based deduplication ensures only strictly unique blocks remain
            unique[content] = {
                "type": "error", # Explicit fallback for legacy CLI code
                "content": content,
                "start_line": err["start_line"],
                "end_line": err["end_line"]
            }
            
        return list(unique.values())

    def extract_errors(self, lines: List[str]) -> List[Dict]:
        errors = []
        current_block = []
        capturing = False
        start_index = 0

        for i, line in enumerate(lines, 1):
            line_clean = line.rstrip()
            is_empty = (line_clean.strip() == "")
            is_new_section = self.is_boundary(line_clean)

            if capturing:
                # 🛑 Stop capturing when blank line or actual new log entry (that ISN'T an error) occurs
                if is_empty or (is_new_section and not self.is_error_line(line_clean)):
                    errors.append(
                        {
                            "content": "\n".join(current_block),
                            "start_line": start_index,
                            "end_line": i - 1,
                        }
                    )
                    capturing = False
                    current_block = []
                else:
                    current_block.append(line_clean)
                    continue

            # 🚨 Start capturing
            if not capturing and not is_empty and self.is_error_line(line_clean):
                capturing = True
                current_block = [line_clean]
                start_index = i

        # 🔚 Close off EOF blocks
        if capturing and current_block:
            errors.append(
                {
                    "content": "\n".join(current_block),
                    "start_line": start_index,
                    "end_line": len(lines),
                }
            )

        return self._deduplicate_and_extract_root(errors)