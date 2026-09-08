from dataclasses import dataclass

from backend.services.distance import haversine_distance_km


@dataclass
class ScoreResult:
    score: int
    distance_km: float
    available_places: int
    reason: str


def score_event(student, event) -> ScoreResult | None:
    available_places = event.capacity - event.registered_count

    if available_places <= 0:
        return None

    event_price = float(event.price)
    student_max_price = getattr(student, "max_price", None)

    if student_max_price is not None and event_price > float(student_max_price):
        return None

    score = 0
    reasons = []

    student_interests = {
        interest.strip().lower()
        for interest in student.interests.split(",")
        if interest.strip()
    }

    if event.category.strip().lower() in student_interests:
        score += 30
        reasons.append(f"Matches your {event.category} interest.")

    event_start_time = event.start_datetime.time()
    event_end_time = event.end_datetime.time()

    if (
        event_start_time >= student.available_from
        and event_end_time <= student.available_to
    ):
        score += 20
        reasons.append("Fits your available time.")
    elif (
        student.available_from <= event_start_time <= student.available_to
    ):
        score += 10
        reasons.append("Starts during your available time.")

    target_audience = event.target_audience.strip().lower()
    student_faculty = student.faculty.strip().lower()

    if target_audience == "all students" or target_audience == student_faculty:
        score += 15
        reasons.append("Suitable for your faculty or all students.")

    if event.is_online:
        distance_km = 0.0
        score += 15
        reasons.append("Online event — no travel needed.")
    else:
        distance_km = haversine_distance_km(
            student.latitude,
            student.longitude,
            event.latitude,
            event.longitude,
        )

        if distance_km <= 0.5:
            score += 15
            reasons.append("Very close to your location.")
        elif distance_km <= 1:
            score += 12
            reasons.append("Close to your location.")
        elif distance_km <= 3:
            score += 9
        elif distance_km <= 5:
            score += 6
        else:
            score += 2

    if event_price == 0:
        score += 10
        reasons.append("Free event.")
    else:
        score += 5
        reasons.append("Within your preferred budget.")

    availability_ratio = available_places / event.capacity

    if availability_ratio >= 0.75:
        score += 10
        reasons.append("Many places are still available.")
    elif availability_ratio >= 0.50:
        score += 8
    elif availability_ratio >= 0.25:
        score += 5
    else:
        score += 2

    return ScoreResult(
        score=score,
        distance_km=round(distance_km, 2),
        available_places=available_places,
        reason=" ".join(reasons),
    )

def build_recommendations(student, events):
    recommendations = []

    for event in events:
        result = score_event(student, event)

        if result is None:
            continue

        recommendations.append({
            "event_id": event.id,
            "title": event.title,
            "category": event.category,
            "organizer": event.organizer,
            "location_name": event.location_name,
            "start_datetime": event.start_datetime,
            "end_datetime": event.end_datetime,
            "distance_km": result.distance_km,
            "price": float(event.price),
            "available_places": result.available_places,
            "score": result.score,
            "reason": result.reason,
        })

    return sorted(
        recommendations,
        key=lambda item: (
            -item["score"],
            item["distance_km"],
            item["start_datetime"],
        ),
    )