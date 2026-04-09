import math
from typing import Tuple


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    distance = R * c
    return distance


def is_within_radius(
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float,
        radius_km: float
) -> bool:
    distance = haversine_distance(lat1, lon1, lat2, lon2)
    return distance <= radius_km

def get_bounding_box(lat: float, lon: float, radius_km: float) -> Tuple[float, float, float, float]:
    lat_delta = radius_km / 111.0
    lon_delta = radius_km / (111.0 * math.cos(math.radians(lat)))

    min_lat = lat - lat_delta
    max_lat = lat + lat_delta
    min_lon = lon - lon_delta
    max_lon = lon + lon_delta

    min_lat = max(min_lat, -90.0)
    max_lat = min(max_lat, 90.0)
    min_lon = max(min_lon, -180.0)
    max_lon = min(max_lon, 180.0)

    return min_lat, max_lat, min_lon, max_lon