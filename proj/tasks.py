from helpers.llm import generate_podcast
from proj.celery_conf import celery_app
from proj.helper import generate_episode

@celery_app.task(queue='default')
def add(x, y):
    return x + y

@celery_app.task(queue='default')
def create_morning_episode(params):
    data = params

    data["time"] = "daily"
    summary = generate_podcast(data, "morning")

    # Create episode
    generate_episode(summary, False)

@celery_app.task(queue='default')
def create_eod_episode(params):
    data = params

    data["time"] = "daily"  # Specify the time for EOD
    summary = generate_podcast(data, "eod")

    # Create episode for EOD
    generate_episode(summary, False)

@celery_app.task(queue='default')    
def create_weekly_episode(params):
    # Logic to fetch daily data for a user
    data = params

    data["time"] = "weekly"
    summary = generate_podcast(data, "weekly")

    # Create episode
    generate_episode(summary, False)