from google import genai
from .config import GEMINI_API_KEY
from dotenv import load_dotenv
import json
import typer
import re
from .cache import AICache

load_dotenv()

class AIService:
    def __init__(self):
        if not GEMINI_API_KEY:
            typer.echo("Error: GEMINI_API_KEY not found in environment variables.", err=True)
            raise typer.Exit(code=1)
        
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.cache = AICache()

    def analyze_error(self, error_content: str) -> dict:
        cached = self.cache.get(error_content)
        if cached:
            return cached

        prompt = f"""Analyze this error and return strict JSON format:
{{
  "error_type": "string",
  "root_cause": "string",
  "explanation": "string",
  "fix_command": "string",
  "confidence": integer (0-100)
}}

Error:
{error_content[:2000]}
"""

        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )

            text = response.text.strip()
            if text.startswith("```"):
                text = text.replace("```json", "", 1).replace("```", "")

            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group(0))
                self.cache.set(error_content, result)
                return result
            else:
                raise ValueError("No JSON found in response.")

        except Exception as e:
            # Fallback logic avoids crashing and provides basic heuristics
            keyword = "Unknown Exception"
            if "ModuleNotFoundError" in error_content or "ImportError" in error_content:
                keyword = "Missing Dependency"
                cmd = "pip install <package_name>"
            elif "SyntaxError" in error_content:
                keyword = "Syntax Error"
                cmd = "Check code syntax on the failing line."
            elif "Permission" in error_content:
                keyword = "Permission Denied"
                cmd = "sudo OR check file permissions"
            else:
                cmd = "Review logs manually or search StackOverflow."

            return {
                "error_type": keyword,
                "root_cause": "Failed to parse API response or reach API.",
                "explanation": f"Fallback triggered due to AI error: {e}",
                "fix_command": cmd,
                "confidence": 0
            }