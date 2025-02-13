from fastapi import FastAPI, status, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import json
import os
import requests
from application.llm_prompt import prompt
from application.tasks.task_a1 import install_uv, run_datagen
from application.tasks.task_a2 import format_file
from application.tasks.task_a3 import count_weekdays
from application.tasks.task_a4 import sort_json_by_keys2
from application.tasks.task_a5 import write_first_line_of_recent_logs
from application.tasks.task_a6 import extract_h1_and_create_index
from application.tasks.task_a7 import extract_email_address
from application.tasks.task_a8 import handle_task_A8
from application.tasks.task_a9 import find_most_similar_comments
from application.tasks.task_a10 import calculate_ticket_sales
from application.tasks.check_path import ensure_local_path

AIPROXY_TOKEN = None

with open(".env") as f:
    try:
        for line in f:
            l=line.split("=")
            key,value = l[0],l[1]
            AIPROXY_TOKEN = value
            # print(AIPROXY_TOKEN)
    except:
        print("Setup the enviroment variables")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/run', status_code=status.HTTP_200_OK)
def tasks(task: str):
    headers = {
        "Authorization": f"Bearer {AIPROXY_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": task}
        ],
        "temperature": 0
    }

    response = requests.post("https://aiproxy.sanand.workers.dev/openai/v1/chat/completions", headers=headers, data=json.dumps(data))
    response_json = response.json()
    try:
        rel = json.loads(response_json['choices'][0]['message']['content'])
    except Exception as e:
        return response_json
    if rel['task_id'] == 'A1':
        install_uv()
        run_datagen(email='22f3000819@ds.study.iitm.ac.in')
        return {
            "message": f'Task A1 completed'
        }
    elif rel['task_id'] == 'A2':
        try:
            format_file(rel['file_path'],rel['prettier_version'])
            return {
                "message": f'Task A2 completed'
            }
        except Exception as e:
            return {
                "message": f'{type(e).__name__}'
            }
    elif rel['task_id'] == 'A3':
        try:
            count_weekdays(input_file=rel['input_file'], output_file=rel['output_file'], weekday=rel['day_of_week'])
            return {
                "message": f'Task A3 completed'
            }
        except Exception as e:
            return {
                "message": f'{type(e).__name__}'
            }
    elif rel['task_id'] == 'A4':
        try:
            sort_json_by_keys2(input_file=rel['input_file'], output_file=rel['output_file'], keys=rel['keys'])
            return {
                "message": f'Task A4 completed'
            }
        except Exception as e:
            return {
                "message": f'{type(e).__name__}'
            }
    elif rel['task_id'] == 'A5':
        try:
            write_first_line_of_recent_logs(logs_dir=rel['logs_dir'], output_file=rel['output_file'], num_logs=rel['num_logs'])
            return {
                "message": f'Task A5 completed'
            }
        except Exception as e:
            return {
                "message": f'{type(e).__name__}'
            }
    elif rel['task_id'] == 'A6':
        try:
            extract_h1_and_create_index(docs_dir=rel['docs_dir'], output_file=rel['output_file'])
            return {
                "message": f'Task A6 completed'
            }
        except Exception as e:
            return {
                "message": f'{type(e).__name__}'
            }
    elif rel['task_id'] == 'A7':
        try:
            email_info, ofp = extract_email_address(email_content=rel['input_file'], output_file=rel['output_file'])
            sender_email = (requests.post(
                "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
                headers=headers,
                data=json.dumps({
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": 'extract the senders email address.YOUR response should be only the email address as string'},
                        {"role": "user", "content": email_info}
                    ],
                    "temperature": 0
                })
            )).json()

            with open(ofp, "w") as file:
                file.write(sender_email['choices'][0]['message']['content'])
            return {
                "message": f'Task A7 completed'
            }
        except Exception as e:
            return {
                "message": f'{type(e).__name__}'
            }
    elif rel['task_id'] == 'A8':
        try:
            handle_task_A8(input_file=rel['input_file'], output_file=rel['output_file'])
            return {
                "message": f'Task A8 completed'
            }
        except Exception as e:
            return {
                "message": f'{type(e).__name__}'
            }
    elif rel['task_id'] == 'A9':
        try:
            find_most_similar_comments(comments_file=rel['input_file'], output_file=rel['output_file'])
            return {
                "message": f'Task A9 completed'
            }
        except Exception as e:
            return {
                "message": f'{type(e).__name__}'
            }
    elif rel['task_id'] == 'A10':
        try:
            calculate_ticket_sales(db_file=rel['db_file'], ticket_type=rel['ticket_type'], output_file=rel['output_file'])
            return {
                "message": f'Task A10 completed'
            }
        except Exception as e:
            return {
                "message": f'{type(e).__name__}'
            }
    return {
        "message": f'POST route working {rel}'
    }

@app.get('/read', status_code=status.HTTP_200_OK, response_class=PlainTextResponse)
def read(path: str = Query(..., description="Path to the file to read")):
    output_file_path = ensure_local_path(path)
    if not os.path.exists(output_file_path):
        raise HTTPException(status_code=404, detail="File not found")
    with open(output_file_path, "r") as file:
        content = file.read()
    return content