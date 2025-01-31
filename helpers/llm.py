import os
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import SecretStr
from config import cfg

# Constants for model
_MODEL_NAME = "gpt-4o-mini"


def generate_podcast(data: dict, podcast_type: str):
    # Get the appropriate template based on podcast type
    prompt_template = get_prompt_template(podcast_type)

    llm = get_llm(_MODEL_NAME)
    chain = prompt_template | llm
    result = chain.invoke(data)

    return result.content


def get_prompt_template(podcast_type: str):
    # Define the input variables
    input_variables = [
        "time", "leads_received", "fu_completed", "planned_sv", "planned_sv_leads", "planned_f2f",
        "planned_f2f_leads", "planned_fu", "planned_fu_leads", "total_bookings", "bookings_done",
        "bookings_at_l1", "booking_at_l1_leads", "bookings_at_l2", "booking_at_l2_leads"
    ]

    # Define the templates for each podcast type
    templates = {
        "morning": """
          Rise and shine! Welcome to your **Morning Insights** — the perfect way to kickstart your day and crush your goals!

          Here's a quick rundown of what's in store for today:

          🌟 **Leads Received:** You’ve already got {leads_received} fresh leads today — keep that momentum going!
          🌟 **Follow-Ups Completed:** {fu_completed} follow-ups done! Fantastic job staying on top of things!

          🎯 **Site Visits Planned:** {planned_sv} site visits on the agenda, with {planned_sv_leads} leads lined up for action!
          🎯 **Face-to-Face Meetings Planned:** Get ready for {planned_f2f} face-to-face meetings, with {planned_f2f_leads} leads to connect with in person.
          🎯 **Follow-Ups Scheduled:** {planned_fu} follow-ups are in the cards, with {planned_fu_leads} leads to touch base with.

          🔥 **Bookings Progress:** You’ve got this!
          - **Bookings Done Today:** {bookings_done} bookings completed — incredible hustle!
          - **Level 1 Bookings:** {bookings_at_l1} Level 1 bookings secured, with {booking_at_l1_leads} leads pushing you forward.
          - **Level 2 Bookings:** You’ve locked in {bookings_at_l2} Level 2 bookings, with {booking_at_l2_leads} leads taking things to the next level.

          Huge congrats on hitting your targets so early in the day! You’re making it happen!
          """,
        "eod": """
          Good evening, and welcome to your End-of-Day Summary!

          Let’s take a look at the progress you've made today:

          **Leads Received:** {leads_received} new leads received today.
          **Follow-Ups Completed:** {fu_completed} follow-ups completed today.

          **Site Visits Completed:** {planned_sv} site visits completed, with {planned_sv_leads} leads.
          **Face-to-Face Meetings Completed:** {planned_f2f} face-to-face meetings completed, with {planned_f2f_leads} leads.
          **Follow-Ups Completed:** {planned_fu} follow-ups completed, with {planned_fu_leads} leads.

          **Bookings Progress:**
          - **Total Bookings Done:** {bookings_done} bookings done today.
          - **Level 1 Bookings:** {bookings_at_l1} bookings at Level 1, with {booking_at_l1_leads} leads.
          - **Level 2 Bookings:** {bookings_at_l2} bookings at Level 2, with {booking_at_l2_leads} leads.

          Excellent work today! You’re steadily progressing toward your goals. Keep up the momentum for tomorrow!
          """,
        "weekly": """
          Congratulations on completing the week! Here’s your Weekly Wrap-Up:

          **Leads Received:** {leads_received} new leads this week.
          **Follow-Ups Completed:** {fu_completed} follow-ups completed this week.

          **Site Visits Completed:** {planned_sv} site visits completed, with {planned_sv_leads} leads.
          **Face-to-Face Meetings Completed:** {planned_f2f} face-to-face meetings completed, with {planned_f2f_leads} leads.
          **Follow-Ups Completed:** {planned_fu} follow-ups completed, with {planned_fu_leads} leads.

          **Bookings Achieved:**
          - **Total Bookings for the Week:** {bookings_done}
          - **Level 1 Bookings:** {bookings_at_l1}, with {booking_at_l1_leads} leads.
          - **Level 2 Bookings:** {bookings_at_l2}, with {booking_at_l2_leads} leads.

          It’s been a week of great progress! You’ve put in the effort, and it shows. Let’s keep up the good work next week. You’re definitely on the right track!
          """
    }

    # Return the correct template based on the podcast type
    return PromptTemplate(input_variables=input_variables, template=templates.get(podcast_type, templates['weekly']))


def get_llm(model_name: str):
    openai_api_key = cfg.openai_api_key
    openai_organization_id = cfg.openai_organization_id

    if openai_api_key and openai_organization_id:
        openai_api_key_secret = SecretStr(openai_api_key)
        return ChatOpenAI(
            api_key=openai_api_key_secret,
            organization=openai_organization_id,
            model=model_name,
            temperature=0,
            cache=(os.getenv("LANGCHAIN_CACHE") == "true"),
            streaming=(os.getenv("CHATGPT_STREAMING") == "true"),
            verbose=(os.getenv("LLM_VERBOSE") == "true")
        )
    raise Exception("Secrets for OpenAI are required")


if __name__ == "__main__":
    # Example data input
    data = {
        "leads_received": 10,
        "fu_completed": 7,
        "planned_sv": 2,
        "planned_sv_leads": ["Lead A", "Lead B"],
        "planned_f2f": 3,
        "planned_f2f_leads": ["Lead C", "Lead D", "Lead E"],
        "planned_fu": 5,
        "planned_fu_leads": ["Lead F", "Lead G", "Lead H", "Lead I", "Lead J"],
        "total_bookings": 4,
        "bookings_done": 2,
        "bookings_at_l1": 1,
        "booking_at_l1_leads": ["Lead K"],
        "bookings_at_l2": 1,
        "booking_at_l2_leads": ["Lead L"],
        "time": "daily"
    }
