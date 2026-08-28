import requests


OVERPASS_SERVERS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]


def search_places(latitude: float, longitude: float):

    query = f"""
    [out:json][timeout:15];

    (
      node["tourism"](around:10000,{latitude},{longitude});
      way["tourism"](around:10000,{latitude},{longitude});
      relation["tourism"](around:10000,{latitude},{longitude});
    );

    out center;
    """

    # Try each Overpass server
    for server in OVERPASS_SERVERS:

        try:

            response = requests.get(
                server,
                params={"data": query},
                headers={
                    "User-Agent": "TripWiseAI/1.0"
                },
                timeout=25
            )

            response.raise_for_status()

            data = response.json()

            places = []

            for item in data.get("elements", []):

                tags = item.get("tags", {})

                name = tags.get("name")

                if not name:
                    continue

                latitude_value = item.get("lat")
                longitude_value = item.get("lon")

                # Ways/relations use center coordinates
                if (
                    latitude_value is None
                    or longitude_value is None
                ):

                    center = item.get(
                        "center",
                        {}
                    )

                    latitude_value = center.get(
                        "lat"
                    )

                    longitude_value = center.get(
                        "lon"
                    )

                if (
                    latitude_value is None
                    or longitude_value is None
                ):
                    continue

                places.append({
                    "name": name,
                    "latitude": latitude_value,
                    "longitude": longitude_value,
                    "type": tags.get(
                        "tourism",
                        "place"
                    )
                })

            return places

        except (
            requests.RequestException,
            ValueError
        ):
            # Try next server
            continue

    # ---------------------------------------------------------
    # IMPORTANT:
    # If all Overpass servers fail, DO NOT CRASH THE PROJECT.
    # Return an empty list so weather, budget and itinerary
    # workflow can continue.
    # ---------------------------------------------------------

    return []