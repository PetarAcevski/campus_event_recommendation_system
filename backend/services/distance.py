from math import asin, cos, radians, sin, sqrt

EARTH_RADIUS_KM = 6371.0088


def haversine_distance_km(
    latitude_1: float,
    longitude_1: float,
    latitude_2: float,
    longitude_2: float,
) -> float:
    latitude_1_rad = radians(float(latitude_1))
    longitude_1_rad = radians(float(longitude_1))
    latitude_2_rad = radians(float(latitude_2))
    longitude_2_rad = radians(float(longitude_2))

    latitude_difference = latitude_2_rad - latitude_1_rad
    longitude_difference = longitude_2_rad - longitude_1_rad

    haversine_value = (
        sin(latitude_difference / 2) ** 2
        + cos(latitude_1_rad)
        * cos(latitude_2_rad)
        * sin(longitude_difference / 2) ** 2
    )

    central_angle = 2 * asin(sqrt(haversine_value))

    return EARTH_RADIUS_KM * central_angle