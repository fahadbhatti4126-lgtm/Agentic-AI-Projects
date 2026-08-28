from agents.planner_agent import analyze_trip
from agents.research_agent import research_trip


user_request = """
Mujhe Lahore se Murree 3 din ke liye jana hai.
Mera total budget 25000 rupees hai.
Hum 2 log hain.
Humein nature, sightseeing aur peaceful places pasand hain.
Hum public transport prefer karte hain.
"""

# Step 1: Convert user request into structured trip
trip = analyze_trip(user_request)

print("\n--- Trip Request ---")
print(trip.model_dump())


# Step 2: Research destination
research = research_trip(trip)

print("\n--- Location ---")
print(research.location)

print("\n--- Weather ---")
print(research.weather["daily"]["time"])

print("\n--- Places ---")

for place in research.places[:10]:
    print(
        place["name"],
        "|",
        place["type"]
    )