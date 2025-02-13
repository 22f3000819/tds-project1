import json

task_definitions = {
    "A1": "Install uv (if required) and run datagen.py with ${user.email} as the argument.",
    "A2": "Format /data/format.md using prettier@3.4.2.",
    "A3": "Count the number of Wednesdays in /data/dates.txt and write it to /data/dates-wednesdays.txt.",
    "A4": "Sort contacts in /data/contacts.json by last_name, first_name, and save as /data/contacts-sorted.json.",
    "A5": "Write the first line of the 10 most recent .log files in /data/logs/ to /data/logs-recent.txt.",
    "A6": "Extract H1 titles from Markdown files in /data/docs/ and create /data/docs/index.json.",
    "A7": "Extract sender's email address from /data/email.txt using LLM and save to /data/email-sender.txt.",
    "A8": "Extract credit card number from /data/credit-card.png using LLM and save to /data/credit-card.txt.",
    "A9": "Find the most similar pair of comments in /data/comments.txt using embeddings and save to /data/comments-similar.txt.",
    "A10": "Compute total sales for 'Gold' tickets from /data/ticket-sales.db and save to /data/ticket-sales-gold.txt.",
    "B1": "Ensure no data outside /data is accessed or exfiltrated.",
    "B2": "Ensure no data is deleted anywhere on the file system.",
    "B3": "Fetch data from an API and save it.",
    "B4": "Clone a Git repo and make a commit.",
    "B5": "Run a SQL query on SQLite or DuckDB.",
    "B6": "Extract data from a website (scraping).",
    "B7": "Compress or resize an image.",
    "B8": "Transcribe audio from an MP3 file.",
    "B9": "Convert Markdown to HTML.",
    "B10": "Write an API endpoint that filters a CSV file and returns JSON data."
}

prompt = f"""
You are an AI assistant that classifies task descriptions and extracts structured details.

### **Step 1: Classify the Task**
Match the given task description (in any language) to the most relevant predefined task from the list:

{json.dumps(task_definitions, indent=2)}

If no match is found, return `"task_id": "unknown"`.

---

### **Step 2: Extract Additional Information**
If the task matches one of the following, extract the requested values:

#### **A2: Formatting using Prettier**
- `"prettier_version"`: Extract the version of Prettier mentioned. If no version is specified, return `"3.4.2"`.

#### **A3: Counting Days in a File**
- `"input_file"`: Extract the input file path. If only a filename is given (without `/data/`), assume it's inside `/data/`.
- `"output_file"`: Extract the output file path. If only a filename is given (without `/data/`), assume it's inside `/data/`.
- `"day_of_week"`: Extract the day of the week and return it in **Ubuntu Linux format** (`Monday`, `Tuesday`, etc.).

#### **A4: Sorting Contacts**
- `"input_file"`: Extract the input file path. Default to `/data/filename` if `/data/` is missing.
- `"output_file"`: Extract the output file path. Default to `/data/filename` if `/data/` is missing.

#### **A5: Extracting Log Entries**
- `"input_file"`: Extract the input file path (should be inside `/data/logs/`). If not specified, default to `/data/filename`.
- `"output_file"`: Extract the output file path. Default to `/data/filename` if `/data/` is missing.

#### **A6: Extracting H1 Titles**
- `"output_file"`: Extract the output file path (should be inside `/data/docs/`). If not specified, default to `/data/docs/filename`.

---

### **Output Format**
Return only a JSON object like this:
{{
    "task_id": "A3",
    "confidence": 0.92,
    "input_file": "/data/dates.txt",
    "output_file": "/data/dates-wednesdays.txt",
    "day_of_week": "Wednesday"
}}
"""