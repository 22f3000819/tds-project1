import json
from .check_path import ensure_local_path

def sort_json_by_keys2(input_file: str, output_file: str, keys: list):
    input_file_path = ensure_local_path(input_file)
    output_file_path = ensure_local_path(output_file) 
    with open(input_file_path, "r") as file:
        data = json.load(file)
    
    sorted_data = sorted(data, key=lambda x: tuple(x[key] for key in keys))
    
    with open(output_file_path, "w") as file:
        json.dump(sorted_data, file)