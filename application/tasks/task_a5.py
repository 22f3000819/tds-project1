import glob
import os
from .check_path import ensure_local_path

def write_first_line_of_recent_logs(logs_dir: str, output_file: str, num_logs: int = 10):
    # Get all .log files in the directory
    logs_dir_path = ensure_local_path(logs_dir)
    output_file_path = ensure_local_path(output_file) 
    log_files = glob.glob(os.path.join(logs_dir_path, "*.log"))
    
    # Sort files by modification time, most recent first
    log_files.sort(key=os.path.getmtime, reverse=True)
    
    # Take the top `num_logs` files
    recent_logs = log_files[:num_logs]
    
    # Write the first line of each file to the output file
    with open(output_file_path, "w") as outfile:
        for log_file in recent_logs:
            with open(log_file, "r") as infile:
                first_line = infile.readline()
                outfile.write(first_line)