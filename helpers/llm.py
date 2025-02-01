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
        "bookings_at_l1", "booking_at_l1_leads", "bookings_at_l2", "booking_at_l2_leads",
        'total_calls', 'target_calls', 'total_sv', 'target_sv',
    ]

    # Define the templates for each podcast type
    templates = {
        "morning": """
            Morning update:
            - Site visits: {planned_sv} visits planned, {planned_sv_leads} leads.
            - Meetings planned {planned_f2f}, {planned_f2f_leads} leads.

            Please summarize this data in a natural, engaging way, showing excitement and motivation for the day ahead.
            always find new way to motivate and add motivation quotes to the summary.
        """,
        "eod": """
            Evening update:
            - l1 Bookings approved: {bookings_at_l1} bookings at level 1, {booking_at_l1_leads} leads
            - l2 Bookings approved: {bookings_at_l2} bookings at level 2, {booking_at_l2_leads} leads
            - Bookings progress: {bookings_done} bookings done today
            - Targets: {leads_received} new leads, {fu_completed} follow-ups completed.
            - Site visits: {planned_sv} visits completed, {planned_sv_leads} leads.

            Provide a summary of the day’s work in a positive tone, focusing on achievements and motivating for tomorrow.
            always find new way to motivate and add motivation quotes to the summary.
        """,
        "weekly": """
            Weekly progress:
            - Total bookings: {bookings_done}.
            - Total calls: {total_calls} out of target {target_calls}.
            - Total site visits: {total_sv} out of target {target_sv}.
            - Leads received: {leads_received}, follow-ups completed: {fu_completed}.
            - Site visits: {planned_sv} visits.

            Write a wrap-up of the week’s performance, highlighting key achievements and motivating for next week.
            always find new way to motivate and add motivation quotes to the summary.
        """
    }

    prompt_end = """
            remove points with 0 numbers.
            prefer using qualititave words instead of numbers, like: few, many, halfway, almost, midpoint, a little, a lot, etc.
            dont include more than 2 lead names for each point.
            dont include yourself in the summary.
            dont use these words: we, our, i, me, etc.
    """

    template = templates.get(podcast_type, templates['weekly']) + prompt_end

    # Return the correct template based on the podcast type
    return PromptTemplate(input_variables=input_variables, template=template)


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
