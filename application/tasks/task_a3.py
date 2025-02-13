from .check_path import ensure_local_path
from dateutil.parser import parse

def count_weekdays(input_file: str, output_file: str, weekday: str):
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday_index = weekdays.index(weekday)

    # Ensure paths are local
    input_file_path = ensure_local_path(input_file)
    output_file_path = ensure_local_path(output_file)
    count = 0
    with open(input_file_path, "r") as file:
        for line in file:
            date_str = line.strip()
            if not date_str:
                continue  # Skip empty lines
            try:
                parsed_date = parse(date_str)  # Auto-detect format
                if parsed_date.weekday() == weekday_index:
                    count += 1
            except ValueError:
                print(f"Skipping invalid date format: {date_str}")

    # Write the result to the output file
    with open(output_file_path, "w") as file:
        file.write(str(count))