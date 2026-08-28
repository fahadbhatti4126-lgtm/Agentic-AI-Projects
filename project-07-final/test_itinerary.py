from agents.planner_agent import analyze_trip
from agents.research_agent import research_trip
from agents.itinerary_agent import create_itinerary


user_request = """
Mujhe Lahore se Murree 3 din ke liye jana hai.
Mera total budget 25000 rupees hai.
Hum 2 log hain.
Humein nature, sightseeing aur peaceful places pasand hain.
Hum public transport prefer karte hain.
"""


# Step 1: Understand the trip
trip = analyze_trip(user_request)

print("\n--- Trip Request ---")
print(trip.model_dump())


# Step 2: Research destination
research = research_trip(trip)

print("\n--- Research Complete ---")
print("Places found:", len(research.places))


# Step 3: Create itinerary
itinerary = create_itinerary(
    trip,
    research
)

print("\n--- AI ITINERARY ---")
print(itinerary)