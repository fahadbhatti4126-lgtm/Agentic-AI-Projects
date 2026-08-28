from tools.location_tool import get_coordinates
from tools.places_tool import search_places


destination = "Murree"

location = get_coordinates(destination)

places = search_places(
    location["latitude"],
    location["longitude"]
)

print("\n--- Places Found ---")

for place in places:
    print(
        place["name"],
        "| Type:",
        place["type"],
        "| Lat:",
        place["latitude"],
        "| Lon:",
        place["longitude"]
    )