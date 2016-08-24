from celery import Celery

app = Celery('worker', broker='amqp://guest@localhost//')

@app.task
def add(x, y):
    return x + y