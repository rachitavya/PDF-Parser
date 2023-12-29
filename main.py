from fastapi import FastAPI, File, UploadFile,Query
from celery.result import AsyncResult
from celery import Celery
import time
import uuid
from fastapi.responses import JSONResponse

app = FastAPI()
celery_app = Celery('tasks', broker='redis://localhost:6379/0')

def convert(file):
    file_content=file.file.read()
    time.sleep(4)
    return file_content

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):    
    result = celery_app.send_task("tasks.convert", args=[file.file.read()])
    # id=uuid.uuid4()
    id=str(result.id)
    return {'status':'task started','task_id':id,"filename": 'hello'}

@app.get("/task-status/")
async def get_task_status(task_id: str = Query(..., title="Task ID", description="ID of the Celery task")):
    # Check the status of the Celery task using the task_id
    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.state == 'PENDING':
        response_data = {"status": "pending", "message": "Task is still pending."}
    elif task_result.state == 'SUCCESS':
        response_data = {"status": "success", "message": "Task has completed successfully."}
    elif task_result.state == 'FAILURE':
        response_data = {"status": "failure", "message": f"Task has failed: {task_result.result}"}
    else:
        response_data = {"status": "unknown", "message": "Task status is unknown."}

    return JSONResponse(content=response_data)