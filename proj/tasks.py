from proj.celery_conf import celery_app

@celery_app.task(queue='default')
def add(x, y):
    return x + y

@celery_app.task(queue='default')
def create_episode():
    # @todo Abhished
    # Logic to fetch data for a user

    # generate a summary of the data
    summary = "This is a summary of the data."

    