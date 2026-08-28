import re

from langchain_groq import ChatGroq

from config import GROQ_API_KEY
from utils.helpers import TripRequest, ResearchResult


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=GROQ_API_KEY
)


def validate_itinerary(
    trip: TripRequest,
    research: ResearchResult,
    itinerary: str
):
    # ---------------------------------------------------------
    # SAFETY CHECK
    # ---------------------------------------------------------

    if not itinerary or not str(itinerary).strip():
        return ""

    itinerary = str(itinerary).strip()

    # ---------------------------------------------------------
    # VERIFIED PLACES
    # ---------------------------------------------------------

    verified_places = {
        str(place["name"]).strip()
        for place in research.places
        if place.get("name")
    }

    places_text = "\n".join(
        f"- {place}"
        for place in sorted(verified_places)
    )

    # ---------------------------------------------------------
    # VALIDATION PROMPT
    # ---------------------------------------------------------

    prompt = f"""
You are a strict travel itinerary validator.

Your job is ONLY to check and minimally correct the
already-generated itinerary.

TRIP:
Origin: {trip.origin}
Destination: {trip.destination}
Days: {trip.days}
Budget: PKR {trip.budget}
Travelers: {trip.travelers}
Interests: {", ".join(trip.interests)}
Transport: {trip.transport_preference}

VERIFIED PLACES:
{places_text}

ORIGINAL ITINERARY:
{itinerary}

RULES:

1. Return exactly {trip.days} days.
2. Keep the original itinerary structure.
3. Do NOT create a new itinerary.
4. Do NOT remove a day.
5. Tourist places must come from VERIFIED PLACES.
6. Do not invent prices.
7. Do not invent travel times.
8. Do not claim hotel availability.
9. Do not invent opening hours.
10. Do not invent ticket prices.
11. Do not add new attractions.
12. Keep supported weather warnings.
13. Make only necessary corrections.
14. Return the COMPLETE itinerary.
15. Never return an empty response.
16. Never return "No itinerary was returned."
17. Never explain your corrections.

IMPORTANT:

If the original itinerary is already valid,
return it unchanged.

OUTPUT FORMAT:

Day 1:
Morning:
...
Afternoon:
...
Evening:
...

Day 2:
Morning:
...
Afternoon:
...
Evening:
...

Continue until Day {trip.days}.

Return ONLY the complete itinerary.
"""

    try:

        response = llm.invoke(prompt)

        result = str(
            response.content
        ).strip()

    except Exception:

        # If validator fails, keep original itinerary
        return itinerary

    # ---------------------------------------------------------
    # STRONG FALLBACK
    # ---------------------------------------------------------

    invalid_phrases = [
        "no itinerary was returned",
        "no itinerary",
        "unable to generate",
        "cannot generate",
        "i cannot",
        "i'm unable",
        "unable to validate",
    ]

    result_lower = result.lower()

    if not result:
        return itinerary

    # Validator must never replace a valid itinerary with UI/code output.
    if (
        "<div" in result_lower
        or "<style" in result_lower
        or "<script" in result_lower
        or "```" in result
    ):
        return itinerary

    if any(
        phrase in result_lower
        for phrase in invalid_phrases
    ):
        return itinerary

    # ---------------------------------------------------------
    # CHECK THAT DAYS EXIST
    # ---------------------------------------------------------

    day_count = 0

    for day_number in range(1, trip.days + 1):

        if re.search(
            rf"(?im)^\s*(?:#{1,6}\s*)?(?:\*\*)?Day\s+{day_number}\b",
            result,
        ):
            day_count += 1

    # Validator must contain the expected days.
    # Otherwise use the original itinerary.
    if day_count < trip.days:
        return itinerary

    # ---------------------------------------------------------
    # CHECK MINIMUM CONTENT
    # ---------------------------------------------------------

    if len(result) < 200:
        return itinerary

    return result