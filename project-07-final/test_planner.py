from agents.planner_agent import analyze_trip

request = """
I want to travel from Lahore to Murree
for 3 days.

Total budget: 25000 PKR.
Number of travelers: 2.

My interests are:
Nature, Sightseeing, Peaceful places.

Preferred transport:
public transport.
"""

trip = analyze_trip(request)

print(trip)
print(type(trip))