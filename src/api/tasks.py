import json
import os
from dataclasses import asdict

import requests
from dotenv import load_dotenv

from models.task import PriorityType, Task

load_dotenv()

BASE_URL = os.getenv("BACKEND_BASE_URL")


def get_tasks() -> list[Task]:
    headers = {"Content-Type": "application/json"}

    response = requests.get(f"{BASE_URL}/tasks", headers=headers)

    response.raise_for_status()

    tasks = [Task(**items) for items in response.json()]

    return tasks


def add_task(title: str, desc: str):
    task = Task(title=title, description=desc, priority=PriorityType.LOW)

    headers = {"Content-Type": "application/json"}

    resp = requests.post(
        f"{BASE_URL}/tasks", data=json.dumps(asdict(task)), headers=headers
    )

    resp.raise_for_status()

    return resp.status_code == 201
