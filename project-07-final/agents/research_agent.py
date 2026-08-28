from tools.location_tool import get_coordinates
from tools.weather_tool import get_weather
from tools.places_tool import search_places

from utils.helpers import TripRequest, ResearchResult


def research_trip(trip: TripRequest) -> ResearchResult:
    # Step 1: Find destination coordinates
    location = get_coordinates(trip.destination)

    # Step 2: Get weather forecast
    weather = get_weather(
        location["latitude"],
        location["longitude"],
        days=trip.days
    )

    # Step 3: Find nearby places
    places = search_places(
        location["latitude"],
        location["longitude"]
    )

    # Step 4: Return structured research result
    return ResearchResult(
        location=location,
        weather=weather,
        places=places
    )