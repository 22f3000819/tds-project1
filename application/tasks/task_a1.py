import subprocess
import sys
import os
import urllib.request

DATA_GEN_URL = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
DATA_GEN_FILE = "datagen.py"

def install_uv():
    """Check if 'uv' is installed and install it if not."""
    try:
        subprocess.run(["uv", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ uv is already installed.")
    except FileNotFoundError:
        print("❌ uv is not installed. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "uv"], check=True)

def run_datagen(email: str):
    url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
    script_path = "datagen.py"

    # Download the script
    print("Downloading datagen.py...")
    urllib.request.urlretrieve(url, script_path)

    # Run using `uv`
    try:
        result = subprocess.run(
            ["sudo","uv", "run", script_path, email],
            capture_output=True,
            text=True,
            check=True
        )
        print("Output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)
    
    # Optional: Clean up the file after execution
    os.remove(script_path)