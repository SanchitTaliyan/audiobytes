from proj.celery_conf import celery_app
from proj.helper import generate_episode

def format_leads(leads):
    if len(leads) <= 2:
        return "\n".join([f"> {lead}" for lead in leads])
    else:
        return "\n".join([f"> {lead}" for lead in leads[:2]]) + f"\n+ {len(leads) - 2} others"
@celery_app.task(queue='default')
def add(x, y):
    return x + y

@celery_app.task(queue='default')
def create_daily_morning_episode():
    # Logic to fetch daily data for a user
    leads_received = 30
    fu_completed = 12
    planned_sv = 5
    planned_fu = 9
    planned_f2f = 6
    total_bookings = 10
    bookings_done = 2
    bookings_at_l1 = 6
    bookings_at_l2 = 2

    # Sample lead data: [lead_id, lead_name, lead_phone]
    planned_sv_leads = ["Avinash", "Poonam", "Rahul", "Sneha", "Vikram"]
    planned_f2f_leads = ["Anjali", "Karan", "Priya", "Rohit", "Shreya", "Tanmay"]
    planned_fu_leads = ["Deepak", "Meera", "Nitin", "Pooja", "Rajesh", "Suman", "Vivek", "Yash", "Zoya"]
    booking_at_l1_leads = ["Arjun", "Bhavna", "Chetan", "Divya", "Esha", "Farhan"]
    booking_at_l2_leads = ["Gaurav", "Hina"]


    # Generate a summary of the data
    summary = f"""
    Planned Site Visits:  
    {format_leads(planned_sv_leads)}

    Planned Face-to-Face Meetings:  
    {format_leads(planned_f2f_leads)}

    Planned Follow-Ups:  
    {format_leads(planned_fu_leads)}

    Bookings at Level 1:  
    {format_leads(booking_at_l1_leads)}

    Bookings at Level 2:  
    {format_leads(booking_at_l2_leads)}
    
    Today, you've received {leads_received} leads and completed {fu_completed} follow-ups. 
    You have {planned_sv} site visits, {planned_fu} follow-ups, and {planned_f2f} face-to-face meetings planned.
    Your total bookings stand at {total_bookings} ({bookings_done} completed, {bookings_at_l1} at Level 1, and {bookings_at_l2} at Level 2).

    Quote of the Day:  
    "Success is the sum of small efforts, repeated day in and day out."

    Keep pushing forward—every effort counts! 💪
    """

    # Create episode
    generate_episode(summary, False)

@celery_app.task(queue='default')    
def create_daily_eod_episode():
    # Logic to fetch daily data for a user
    leads_received = 54
    fu_completed = 12
    planned_sv = 7
    planned_fu = 12
    planned_f2f = 3
    total_bookings = 13
    bookings_done = 3
    bookings_at_l1 = 5
    bookings_at_l2 = 5

    # Sample lead data: [lead_id, lead_name, lead_phone]
    planned_sv_leads = ["Rohan", "Neha", "Amit", "Kavita", "Suresh", "Anita", "Vijay"]
    planned_f2f_leads = ["Ritu", "Sanjay", "Pooja"]
    planned_fu_leads = ["Manoj", "Swati", "Alok", "Preeti", "Rahul", "Divya", "Vikas", "Anjali", "Raj", "Sunita", "Arun", "Kiran"]
    booking_at_l1_leads = ["Nikhil", "Shweta", "Ravi", "Priya", "Aakash"]
    booking_at_l2_leads = ["Deepa", "Rajat", "Ananya", "Vivek", "Sonia"]

    # Function to format lead lists
    def format_leads(leads):
        if len(leads) <= 2:
            return "\n".join([f"> {lead}" for lead in leads])
        else:
            return "\n".join([f"> {lead}" for lead in leads[:2]]) + f"\n+ {len(leads) - 2} others"

    # Generate a summary of the data
    summary = f"""
    Planned Site Visits:  
    {format_leads(planned_sv_leads)}

    Planned Face-to-Face Meetings:  
    {format_leads(planned_f2f_leads)}

    Planned Follow-Ups:  
    {format_leads(planned_fu_leads)}

    Bookings at Level 1:  
    {format_leads(booking_at_l1_leads)}

    Bookings at Level 2:  
    {format_leads(booking_at_l2_leads)}
    
    Today, you received {leads_received} leads and successfully completed {fu_completed} follow-ups. 
    You planned {planned_sv} site visits, {planned_fu} follow-ups, and {planned_f2f} face-to-face meetings for the day. 
    Out of {total_bookings} total bookings, you completed {bookings_done}, with {bookings_at_l1} at Level 1 and {bookings_at_l2} at Level 2.

    Your consistent effort is paying off—each follow-up, site visit, and booking is a step toward your goals. Keep up the great work!

    Quote of the Day:  
    "The harder you work for something, the greater you'll feel when you achieve it."

    Keep pushing, your success is on the way!
    """

    # Create episode
    generate_episode(summary, False)

@celery_app.task(queue='default')
def create_weekly_episode():
    # Logic to fetch weekly data of a user
    leads_received = 100
    fu_completed = 35
    planned_sv = 23
    planned_fu = 13
    planned_f2f = 8
    total_bookings = 15
    bookings_done = 5
    bookings_at_l1 = 7
    bookings_at_l2 = 3

    # generate a summary of the data
    summary = f"""
      This week, you received {leads_received} leads and successfully completed {fu_completed} follow-ups. 
      You planned {planned_sv} site visits, {planned_fu} follow-ups, and {planned_f2f} face-to-face meetings. 
      Out of {total_bookings} total bookings, you've accomplished {bookings_done}, with {bookings_at_l1} at Level 1 
      and {bookings_at_l2} at Level 2.

      **Your hard work is showing great results, and the path to success is being paved one lead at a time.**

      Quote of the Week:  
      "Don't watch the clock; do what it does. Keep going."

      Stay focused, keep pushing, and let's make the next week even more successful!
    """

    # create episode
    generate_episode(summary, True)