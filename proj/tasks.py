from helpers.llm import generate_podcast
from proj.celery_conf import celery_app
from proj.helper import generate_episode

@celery_app.task(queue='default')
def add(x, y):
    return x + y

@celery_app.task(queue='default')
def create_daily_episode():
    data = {
        "leads_received": 30,
        "fu_completed": 12,
        "planned_sv": 5,
        "planned_fu": 9,
        "planned_f2f": 6,
        "total_bookings": 10,
        "bookings_done": 2,
        "bookings_at_l1": 6,
        "bookings_at_l2": 2,
        "planned_sv_leads": ["Avinash", "Poonam", "Rahul", "Sneha", "Vikram"],
        "planned_f2f_leads": ["Anjali", "Karan", "Priya", "Rohit", "Shreya", "Tanmay"],
        "planned_fu_leads": ["Deepak", "Meera", "Nitin", "Pooja", "Rajesh", "Suman", "Vivek", "Yash", "Zoya"],
        "booking_at_l1_leads": ["Arjun", "Bhavna", "Chetan", "Divya", "Esha", "Farhan"],
        "booking_at_l2_leads": ["Gaurav", "Hina"]
    }

    data["time"] = "daily"
    summary = generate_podcast(data)

    # Create episode
    generate_episode(summary, False)

@celery_app.task(queue='default')    
def create_weekly_episode():
    # Logic to fetch daily data for a user
    data = {
        "leads_received": 54,
        "fu_completed": 12,
        "planned_sv": 7,
        "planned_fu": 12,
        "planned_f2f": 3,
        "total_bookings": 13,
        "bookings_done": 3,
        "bookings_at_l1": 5,
        "bookings_at_l2": 5,
        "planned_sv_leads": ["Rohan", "Neha", "Amit", "Kavita", "Suresh", "Anita", "Vijay"],
        "planned_f2f_leads": ["Ritu", "Sanjay", "Pooja"],
        "planned_fu_leads": ["Manoj", "Swati", "Alok", "Preeti", "Rahul", "Divya", "Vikas", "Anjali", "Raj", "Sunita", "Arun", "Kiran"],
        "booking_at_l1_leads": ["Nikhil", "Shweta", "Ravi", "Priya", "Aakash"],
        "booking_at_l2_leads": ["Deepa", "Rajat", "Ananya", "Vivek", "Sonia"]
    }

    data["time"] = "weekly"
    summary = generate_podcast(data)

    # Create episode
    generate_episode(summary, False)