import subprocess

# Format the file using npx (without global installation)
def format_file(prettier_version = '3.4.2'):
    print(f"Formatting /data/format.md using Prettier {prettier_version}...")
    subprocess.run(["npx", f"prettier@{prettier_version}", "--write", "C:\data\\format.md"], check=True)
