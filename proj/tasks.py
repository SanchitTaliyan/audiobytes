from proj.celery_conf import celery_app
from proj.helper import generate_episode

@celery_app.task(queue='default')
def add(x, y):
    return x + y

@celery_app.task(queue='default')
def create_daily_episode():
    # @todo Abhishek
    # Logic to fetch data for a user

    # generate a summary of the data
    summary = "This is a summary of the data."

    # create episode
    generate_episode(summary, False)

@celery_app.task(queue='default')
def create_weekly_episode():
    # @todo Abhishek
    # Logic to fetch weekly data of a user

    # generate a summary of the data
    summary = "This is a summary of the data."

    # create episode
    generate_episode(summary, True)