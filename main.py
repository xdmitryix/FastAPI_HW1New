# Задание
#
# Необходимо создать API для управления списком задач. Каждая задача должна содержать заголовок и описание.
# Для каждой задачи должна быть возможность указать статус (выполнена/не выполнена).
#
# API должен содержать следующие конечные точки:
# — GET /tasks — возвращает список всех задач.
# — GET /tasks/{id} — возвращает задачу с указанным идентификатором.
# — POST /tasks — добавляет новую задачу.
# — PUT /tasks/{id} — обновляет задачу с указанным идентификатором.
# — DELETE /tasks/{id} — удаляет задачу с указанным идентификатором.
#
# Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа.
# Для этого использовать библиотекуPydantic.

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, List
from pydantic import BaseModel
import pandas as pd

app = FastAPI()
templates = Jinja2Templates(directory="templates")
tasks = []


class Task(BaseModel):
    id: int
    heading: str
    decsription: str
    status: str


@app.get('/')
async def index():
    return 'работает'


@app.post('/addtask/', response_model=Task)
async def add_task(task: Task):
    task_id = len(tasks) + 1
    task.id = task_id
    tasks.append(task)
    return task


@app.get('/tasks/', response_class=HTMLResponse)
async def show_tasks(request: Request):
    task_table = pd.DataFrame([vars(task) for task in tasks]).to_html()
    return templates.TemplateResponse("tasks.html", {"request": request, "task_table": task_table})


@app.get('/tasks/{id_task}/', response_class=HTMLResponse)
async def show_task_to_id(id_task: int):
    for i, task in enumerate(tasks):
        if task.id == id_task:
            return pd.DataFrame([vars(tasks[i])]).to_html()


@app.get('/del/{id_task}/', response_class=HTMLResponse)
async def delete_task_to_id(id_task: int):
    for i, task in enumerate(tasks):
        if task.id == id_task:
            tasks.pop(i)
    task_table = pd.DataFrame([vars(task) for task in tasks]).to_html()
    return task_table


@app.put('/put/{id_task}', response_model=Task)
async def show_task_to_id(id_task: int, task: Task):
    for i, t in enumerate(tasks):
        if t.id == id_task:
            task.id = id_task
            tasks[i] = task
            return task
