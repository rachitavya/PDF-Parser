from celery import Celery
import time

app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

@app.task
def convert(file_content):
    # Simulate processing by sleeping for 4 seconds
    time.sleep(40)
    return f'{file_content} Hello Pello'