from helpers.llm import generate_podcast
from proj.helper import convert_text_to_speech, generate_episode
from schemas.text_to_speech import TextToSpeechRegisterRequest
from random import randint
from datetime import datetime

data0 = {
    "leads_received": 0,
    "fu_completed": 0,
    "planned_sv": 0,
    "planned_sv_leads": [],
    "planned_f2f": 0,
    "planned_f2f_leads": [],
    # "planned_fu": 5,
    # "planned_fu_leads": ["Lead F", "Lead G", "Lead H", "Lead I", "Lead J"],
    # "total_bookings": 4,
    "bookings_done": 0,
    "bookings_at_l1": 0,
    "booking_at_l1_leads": [],
    "bookings_at_l2": 0,
    "booking_at_l2_leads": [],
    # "time": "daily",
    "total_calls": 0,
    "target_calls": 0,
    "total_sv": 0,
    "target_sv": 0,
}

data1 = data0 | {
    "planned_sv": 2,
    "planned_sv_leads": ["Lead A", "Lead B"],
    "planned_f2f": 3,
    "planned_f2f_leads": ["Lead C", "Lead D", "Lead E"],
}

data2 = data0 | {
    "bookings_at_l1": 1,
    "booking_at_l1_leads": ["Lead K"],
    "bookings_at_l2": 1,
    "booking_at_l2_leads": ["Lead L"],
    "leads_received": 2,
    "fu_completed": 5,
    "planned_sv": 1,
    "planned_sv_leads": ["Lead A"],
}

data3 = data0 | {
    "bookings_done": 2,
    "total_calls": 100,
    "target_calls": 150,
    "total_sv": 8,
    "target_sv": 5,
    "leads_received": 10,
    "fu_completed": 50,
    "planned_sv": 5,
}

data = [data0, data1, data2, data3]





audio_types = 3 * ["morning", "eod"] + ["weekly"]

titles_sets = {
    "morning": ["Start Your Day: Morning Insights"] + 3 * ["Morning Brief"],
    "eod": 2 * ["End of Day Brief"] + ["Recap for the Day"],
    "weekly": ["Weekly Wrap-Up"],
}

time_of_days = {
    "morning": "MORNING",
    "eod": "ENDOFDAY",
    "weekly": "WEEKLY",
}



def pick_random(list):
    return list[randint(0, len(list) - 1)]


for i in range(4):
    for d in data:
        for type in audio_types:
            script = generate_podcast(d, type)
            # print(script)

            output = convert_text_to_speech(TextToSpeechRegisterRequest(text=script))

            title = pick_random(titles_sets[type])
            description = script.replace("*", "")
            duration = d["audio_duration"]
            published_at = datetime.now()
            audio_link = output["s3_url"]
            is_bookmark = False
            is_deleted = False
            time_of_day = time_of_days[type]

            record = (
                title,
                description,
                duration,
                published_at,
                audio_link,
                is_bookmark,
                is_deleted,
                time_of_day,
            )

            print("RECORD:")
            print(record)
