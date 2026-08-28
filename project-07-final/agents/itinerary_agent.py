import re

from langchain_groq import ChatGroq
from config import GROQ_API_KEY

from utils.helpers import TripRequest, ResearchResult


# =========================================================
# LLM
# =========================================================

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.2,
    api_key=GROQ_API_KEY
)


# =========================================================
# CREATE ITINERARY
# =========================================================

def create_itinerary(
    trip: TripRequest,
    research: ResearchResult
):

    # -----------------------------------------------------
    # VERIFIED PLACES ONLY
    # -----------------------------------------------------

    # Keep verified, visitor-oriented places. OSM can use many
    # different tourism types (viewpoint, museum, park, etc.), so
    # do not restrict the itinerary to only three types.
    excluded_types = {
        "hotel", "guest_house", "hostel", "motel", "chalet",
        "apartment", "alpine_hut", "wilderness_hut", "caravan_site"
    }

    verified_places = [
        place for place in research.places
        if place.get("name")
        and str(place.get("type", "place")).lower() not in excluded_types
    ]

    places_text = "\n".join(
        f"- {place['name']} ({place.get('type', 'place')})"
        for place in verified_places
    )

    if not places_text:
        places_text = "- No verified attractions available."

    # -----------------------------------------------------
    # WEATHER
    # -----------------------------------------------------

    weather_text = str(
        research.weather.get(
            "daily",
            {}
        )
    )

    # =====================================================
    # PROMPT
    # =====================================================

    prompt = f"""
You are TripWise AI's itinerary generation agent.

Create ONLY a plain-text/Markdown travel itinerary.

IMPORTANT:
Your response will be displayed directly inside a Streamlit
application.

Therefore:

- NEVER generate HTML.
- NEVER generate CSS.
- NEVER generate XML.
- NEVER generate SVG.
- NEVER generate HTML tags.
- NEVER generate <div>, <h1>, <h2>, <p>, <span>, <style>,
  <script>, or any other HTML element.
- NEVER generate HTML attributes such as class="", style="",
  id="".
- NEVER generate localhost URLs.
- NEVER generate links to localhost.
- NEVER generate dashboard UI code.
- NEVER generate Streamlit code.
- NEVER generate Python code.
- NEVER wrap your answer in ```html, ```markdown, or ```text.
- Return ONLY the actual travel itinerary in normal Markdown.
- The first non-empty line MUST be `Day 1`.
- Do not put any text before `Day 1`.
- Do not put any text after the final day's Evening section.

TRIP DETAILS:

Origin: {trip.origin}
Destination: {trip.destination}
Days: {trip.days}
Budget: PKR {trip.budget}
Travelers: {trip.travelers}
Interests: {", ".join(trip.interests)}
Transport preference: {trip.transport_preference}

VERIFIED PLACES:

{places_text}

WEATHER DATA:

{weather_text}

STRICT RULES:

1. Create exactly {trip.days} days.

2. Prioritize the user's selected interests.

3. ONLY recommend places from VERIFIED PLACES.

4. NEVER invent tourist attractions.

5. NEVER invent hotel prices.

6. NEVER invent transport prices.

7. NEVER invent meal prices.

8. NEVER provide estimated costs unless a verified price
   was explicitly provided.

9. NEVER invent travel duration.

10. Do not claim hotel availability.

11. Do not claim that a hotel is cheap, expensive,
    comfortable, highly rated, or recommended unless
    the verified research explicitly supports it.

12. If a price is unavailable, write exactly:

Price not available — verify before booking.

13. If travel duration is unavailable, write exactly:

Travel time should be verified before departure.

14. Use the provided weather data when planning outdoor
    activities.

15. If rain or bad weather may affect an outdoor activity,
    clearly mention that the user should verify conditions.

16. Respect the user's transport preference.

17. Keep the itinerary practical.

18. Do not overcrowd the itinerary.

19. Do not create a budget table.

20. Do not create a dashboard.

21. Do not include sections such as:

Trip Overview
Budget Overview
Destination
Weather Forecast
Places Found
Your Interests
Your AI Trip Plan Is Ready
Important Notes

22. Do not include HTML or code anywhere in the response.

23. Do not create fake information.

24. Use only information supported by the supplied research.

25. The final response must contain ONLY the itinerary.

FORMAT:

Day 1

Morning:
- ...

Afternoon:
- ...

Evening:
- ...

Day 2

Morning:
- ...

Afternoon:
- ...

Evening:
- ...

Continue until Day {trip.days}.

Remember:

Return ONLY the itinerary.
No HTML.
No CSS.
No code.
No dashboard.
No verification section.
"""

    # =====================================================
    # LLM CALL
    # =====================================================

    try:
        response = llm.invoke(prompt)
        result = response.content
    except Exception:
        result = ""

    # =====================================================
    # BASIC OUTPUT CLEANUP
    # =====================================================

    if result is None:
        result = ""

    result = str(result).strip()

    # Remove accidental Markdown code fences.
    result = result.replace("```markdown", "")
    result = result.replace("```md", "")
    result = result.replace("```text", "")
    result = result.replace("```", "")
    result = result.strip()

    # Never pass obvious UI/code output to the validator or Streamlit UI.
    if "<div" in result.lower() or "<style" in result.lower() or "<script" in result.lower():
        return ""

    if not re.search(r"(?im)^\s*(?:#{1,6}\s*)?(?:\*\*)?Day\s+1\b", result):
        # Reliable non-LLM fallback: never show an empty itinerary
        # when verified places are available.
        if verified_places:
            day_count = max(1, int(trip.days))
            fallback_lines = []
            for day in range(1, day_count + 1):
                place = verified_places[(day - 1) % len(verified_places)]
                name = str(place.get("name", "Verified place"))
                fallback_lines.extend([
                    f"Day {day}",
                    "",
                    "Morning:",
                    f"- Visit {name}.",
                    "",
                    "Afternoon:",
                    "- Explore nearby verified attractions and enjoy the destination.",
                    "",
                    "Evening:",
                    "- Return to your accommodation and review the next day's plan.",
                    ""
                ])
            return "\n".join(fallback_lines).strip()
        return ""

    return result