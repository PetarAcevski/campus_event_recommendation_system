from datetime import datetime, time
from types import SimpleNamespace

from backend.services.recommendation import score_event


def test_perfect_event_receives_100_points():
    student = SimpleNamespace(
        interests="Technology,Career,Workshop",
        available_from=time(9, 0),
        available_to=time(18, 0),
        faculty="Computer Science",
        latitude=41.9980,
        longitude=21.4255,
        max_price=10,
    )

    event = SimpleNamespace(
        category="Technology",
        start_datetime=datetime(2026, 10, 1, 14, 0),
        end_datetime=datetime(2026, 10, 1, 16, 0),
        target_audience="Computer Science",
        is_online=False,
        latitude=41.9980,
        longitude=21.4255,
        price=0,
        capacity=50,
        registered_count=10,
    )

    result = score_event(student, event)

    assert result is not None
    assert result.score == 100
    assert result.distance_km == 0.0
    assert result.available_places == 40


def test_full_event_is_not_recommended():
    student = SimpleNamespace(max_price=10)

    event = SimpleNamespace(
        capacity=20,
        registered_count=20,
    )

    assert score_event(student, event) is None