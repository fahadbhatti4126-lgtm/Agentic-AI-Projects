from agents.planner_agent import analyze_trip
from agents.research_agent import research_trip
from agents.itinerary_agent import create_itinerary
from agents.validator_agent import validate_itinerary


user_request = """
Mujhe Lahore se Murree 3 din ke liye jana hai.
Mera total budget 25000 rupees hai.
Hum 2 log hain.
Humein nature, sightseeing aur peaceful places pasand hain.
Hum public transport prefer karte hain.
"""


# Step 1: Planner Agent
trip = analyze_trip(user_request)

print("\n--- Trip Request ---")
print(trip.model_dump())


# Step 2: Research Agent
research = research_trip(trip)

print("\n--- Research Complete ---")
print("Places found:", len(research.places))


# Step 3: Itinerary Agent
itinerary = create_itinerary(
    trip,
    research
)

print("\n--- AI ITINERARY ---")
print(itinerary)


# Step 4: Validator Agent
validated_itinerary = validate_itinerary(
    trip,
    research,
    itinerary
)

print("\n--- VALIDATED ITINERARY ---")
print(validated_itinerary)