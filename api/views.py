import openrouteservice
import pandas as pd
from django.conf import settings
from django.http import JsonResponse

# Load fuel prices from the CSV file
fuel_prices = pd.read_csv("fuel-prices-for-be-assessment.csv")


ors_client = openrouteservice.Client(key=settings.ORS_API_KEY)

def get_route_with_stops(request):
    start = request.GET.get("start")  # "-122.4194,37.7749"
    end = request.GET.get("end")      # "-118.2437,34.0522"

    if not start or not end:
        return JsonResponse({"error": "Please provide start and end locations."}, status=400)

    try:
        start_coords = tuple(map(float, start.split(',')))
        end_coords = tuple(map(float, end.split(',')))

        # Fetch the route
        route = ors_client.directions(
            coordinates=[start_coords, end_coords],
            profile="driving-car",
            format="geojson"
        )

        # Analyze the route and find fuel stops
        route_data = route['features'][0]['properties']['segments'][0]
        total_distance = route_data['distance'] / 1609.34  # meters to miles
        total_time = route_data['duration'] / 3600  # seconds to hours

        # Calculate fuel stops
        fuel_efficiency = 10  # miles per gallon
        max_range = 500  # miles
        stops = []
        remaining_distance = total_distance
        total_cost = 0

        while remaining_distance > 0:
            # Find the next stop within max range
            stop_distance = min(max_range, remaining_distance)
            fuel_needed = stop_distance / fuel_efficiency

            # Find the cheapest fuel station (demo logic)
            cheapest_station = fuel_prices.iloc[fuel_prices['Retail Price'].idxmin()]
            cost = fuel_needed * cheapest_station['Retail Price']
            total_cost += cost

            stops.append({
                "station": cheapest_station['Truckstop Name'],
                "address": cheapest_station['Address'],
                "city": cheapest_station['City'],
                "state": cheapest_station['State'],
                "fuel_price": cheapest_station['Retail Price'],
                "cost": round(cost, 2)
            })

            remaining_distance -= stop_distance

        return JsonResponse({
            "total_distance": round(total_distance, 2),
            "total_time": round(total_time, 2),
            "fuel_stops": stops,
            "total_fuel_cost": round(total_cost, 2),
            "route": route  # Optional: Return the raw route for visualization
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
