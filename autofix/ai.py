from google import genai
from .config import GEMINI_API_KEY
from dotenv import load_dotenv
import json
import typer

load_dotenv()

class AIService:
    def __init__(self):
        if not GEMINI_API_KEY:
            typer.echo("Error: GEMINI_API_KEY not found in environment variables.", err=True)
            raise typer.Exit(code=1)
        
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def analyze_error(self, error_content: str) -> dict:
        prompt = f"""
You are a senior DevOps engineer.

Return ONLY valid JSON. No markdown, no explanation outside JSON.

Format:
{{
  "error_type": "string",
  "root_cause": "string",
  "explanation": "string",
  "fix_steps": ["step1", "step2"],
  "commands": ["command1", "command2"]
}}

Rules:
- No formatting like ** or backticks
- Commands must be plain strings
- No headings
- No extra text

Log:
{error_content}
"""

        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )

            text = response.text.strip()

            # Clean markdown if present
            if text.startswith("```"):
                text = text.strip("```json").strip("```").strip()

            return json.loads(text)

        except Exception as e:
            return {
                "error_type": "Analysis Failed",
                "root_cause": "AI Service Error",
                "explanation": str(e),
                "fix_steps": ["Check API key", "Check internet"],
                "commands": []
            }