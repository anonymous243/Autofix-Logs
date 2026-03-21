import sys
import os
import subprocess

try:
    from google import genai
except ImportError:
    print("Installing required package 'google-genai'...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-genai", "pydantic"])
    subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", "google-generativeai"])
    print("Restarting application...")
    os.execv(sys.executable, [sys.executable, "-m", "autofix.main"] + sys.argv[1:])

from .cli import app

def main():
    app()

if __name__ == "__main__":
    main()
