import json
import glob
import os
from .check_path import ensure_local_path

def extract_h1_and_create_index(docs_dir: str, output_file: str):
    """
    Find all Markdown (.md) files in the specified directory, extract the first occurrence of each H1 (line starting with #),
    and create an index file mapping each filename (without the directory prefix) to its title.
    """
    docs_dir_path = ensure_local_path(docs_dir)
    output_file_path = ensure_local_path(output_file)

    md_files = glob.glob(os.path.join(docs_dir_path, "**", "*.md"), recursive=True)
    
    index = {}

    for md_file in md_files:
        title = None
        with open(md_file, "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("# "):
                    title = line.lstrip("# ").strip()
                    break  # Stop reading after first H1

        # Compute relative path
        relative_path = os.path.relpath(md_file, docs_dir_path)

        # Store in index (even if no H1 is found)
        index[relative_path] = title if title else ""

    # Write to JSON file
    with open(output_file_path, "w", encoding="utf-8") as json_file:
        json.dump(index, json_file, indent=2, sort_keys=True)