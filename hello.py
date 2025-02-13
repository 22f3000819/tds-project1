from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import requests
from application.llm_prompt import prompt
from application.tasks.task_a1 import install_uv, run_datagen

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
    return {
        "message": f'POST route working {rel}'
    }

@app.get('/read', status_code=status.HTTP_200_OK)
def read(path: str):
    return {
        "message": f'GET route working {path}'
    }
