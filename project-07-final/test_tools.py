from tools.location_tool import get_coordinates
from tools.weather_tool import get_weather


destination = "Murree"

location = get_coordinates(destination)

print("\n--- Location ---")
print(location)


weather = get_weather(
    location["latitude"],
    location["longitude"],
    days=3
)

print("\n--- Weather ---")

for i, date in enumerate(weather["daily"]["time"]):
    print(
        date,
        "| Max:",
        weather["daily"]["temperature_2m_max"][i],
        "°C",
        "| Min:",
        weather["daily"]["temperature_2m_min"][i],
        "°C",
        "| Rain:",
        weather["daily"]["precipitation_probability_max"][i],
        "%"
    )