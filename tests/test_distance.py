from backend.services.distance import haversine_distance_km


def test_same_location_has_zero_distance():
    distance = haversine_distance_km(41.9980, 21.4255, 41.9980, 21.4255)

    assert distance == 0.0


def test_one_degree_of_longitude_near_equator_is_about_111_km():
    distance = haversine_distance_km(0, 0, 0, 1)

    assert 111.0 < distance < 112.0