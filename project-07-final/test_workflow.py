from workflow import build_workflow


user_request = """
Mujhe Lahore se Murree 3 din ke liye jana hai.
Mera total budget 25000 rupees hai.
Hum 2 log hain.
Humein nature, sightseeing aur peaceful places pasand hain.
Hum public transport prefer karte hain.
"""


app = build_workflow()


result = app.invoke({
    "user_request": user_request
})


print("\n==============================")
print("       TRIPWISE RESULT")
print("==============================")

print("\n--- Trip Request ---")
print(result["trip"].model_dump())


print("\n--- Budget Analysis ---")

for key, value in result["budget"].items():
    print(f"{key}: {value}")


print("\n--- FINAL VALIDATED ITINERARY ---")
print(result["final_itinerary"])
print("\n--- STATE KEYS ---")
print(result.keys())
print("\n--- WEATHER DATA ---")
print(result["weather"])

print("\n--- PLACES DATA ---")
print(result["places"][:5])

print("\n--- LOCATION DATA ---")
print(result["location"])