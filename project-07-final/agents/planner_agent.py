from langchain_groq import ChatGroq

from config import GROQ_API_KEY
from utils.helpers import TripRequest


# ---------------------------------------------------------
# LLM
# ---------------------------------------------------------

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=GROQ_API_KEY
)


# ---------------------------------------------------------
# STRUCTURED OUTPUT
# ---------------------------------------------------------
# JSON mode use kar rahe hain instead of tool/function calling.
# Is se functions.TripRequest wala parser error avoid hota hai.

structured_llm = llm.with_structured_output(
    TripRequest,
    method="json_mode"
)


# ---------------------------------------------------------
# PLANNER AGENT
# ---------------------------------------------------------

def analyze_trip(user_request: str) -> TripRequest:

    prompt = f"""
You are the TripWise AI trip planner.

Extract the user's travel request and return ONLY valid JSON.

The JSON must contain these fields:

- origin
- destination
- days
- budget
- travelers
- interests
- transport_preference

Rules:

1. origin = starting location
2. destination = travel destination
3. days = number of travel days
4. budget = total budget in PKR as a number
5. travelers = number of travelers
6. interests = list of interests
7. transport_preference = preferred transport
8. Do not add extra fields.
9. Return valid JSON only.

User request:

{user_request}
"""

    return structured_llm.invoke(prompt)