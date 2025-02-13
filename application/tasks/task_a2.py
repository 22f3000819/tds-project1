import subprocess
from .check_path import ensure_local_path

# Format the file using npx (without global installation)
def format_file(file_path = '/data/format.md', prettier_version = '3.4.2'):
    ifp = ensure_local_path(file_path)
    subprocess.run(["npx", f"prettier@{prettier_version}", "--write", ifp], check=True)
