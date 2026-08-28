from agents.planner_agent import analyze_trip


user_request = """
Mujhe Lahore se Murree 3 din ke liye jana hai.
Mera total budget 25000 rupees hai.
Hum 2 log hain.
Humein nature, sightseeing aur peaceful places pasand hain.
Hum public transport prefer karte hain.
"""

trip = analyze_trip(user_request)

print("\n--- Trip Request ---")
print(trip.model_dump())