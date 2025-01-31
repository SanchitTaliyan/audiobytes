import os

from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import SecretStr

from config import cfg

# _MODEL_NAME = "gpt-4o-2024-08-06"
_MODEL_NAME = "gpt-4o-mini"

def generate_podcast(data: dict):
    # Define the template
    prompt_template = PromptTemplate(
        input_variables=[
            "time", "leads_received", "fu_completed", "planned_sv", "planned_sv_leads", "planned_f2f",
            "planned_f2f_leads", "planned_fu", "planned_fu_leads", "total_bookings", "bookings_done",
            "bookings_at_l1", "booking_at_l1_leads", "bookings_at_l2", "booking_at_l2_leads"
        ],
        template="""
        Summarize the given {time} sales performance data into a short, engaging message that is crisp yet motivating.
        If the performance is below expectations, add a motivational touch to encourage the agent.
        Ensure the text remains concise, avoiding unnecessary names, emojis.
        
        **Daily Performance Report**
        - Leads Received: {leads_received}
        - Follow-Ups Completed: {fu_completed}
        
        **Planned Activities:**
        - Site Visits: {planned_sv} ({planned_sv_leads})
        - Face-to-Face Meetings: {planned_f2f} ({planned_f2f_leads})
        - Follow-Ups: {planned_fu} ({planned_fu_leads})
        
        **Booking Progress:**
        - Total Bookings: {total_bookings}
        - Bookings Completed: {bookings_done}
        - Bookings at Level 1: {bookings_at_l1} ({booking_at_l1_leads})
        - Bookings at Level 2: {bookings_at_l2} ({booking_at_l2_leads})
        """
    )

    llm = get_llm(_MODEL_NAME)

    chain = prompt_template | llm

    result = chain.invoke(data)

    return result.content

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
    raise Exception("Secrets for openai are required")


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

    print(generate_podcast(data))
