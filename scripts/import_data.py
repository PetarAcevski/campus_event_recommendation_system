import csv
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from backend.database import SessionLocal
from backend.models import Event, Student

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EVENTS_CSV = PROJECT_ROOT / "data" / "raw" / "campus_events.csv"
STUDENTS_CSV = PROJECT_ROOT / "data" / "raw" / "students.csv"


def required_text(row, field_name):
    value = row.get(field_name, "").strip()

    if not value:
        raise ValueError(f"Missing required field: {field_name}")

    return value


def parse_boolean(value):
    normalized_value = required_text({"value": value}, "value").lower()

    if normalized_value not in {"true", "false"}:
        raise ValueError(f"Invalid boolean value: {value}")

    return normalized_value == "true"


def import_students(session):
    count = 0

    with STUDENTS_CSV.open(encoding="utf-8") as file:
        for line_number, row in enumerate(csv.DictReader(file), start=2):
            try:
                student = Student(
                    id=int(required_text(row, "student_id")),
                    name=required_text(row, "name"),
                    email=required_text(row, "email"),
                    faculty=required_text(row, "faculty"),
                    year_of_study=int(required_text(row, "year_of_study")),
                    latitude=Decimal(required_text(row, "latitude")),
                    longitude=Decimal(required_text(row, "longitude")),
                    interests=required_text(row, "interests"),
                    available_from=datetime.strptime(
                        required_text(row, "available_from"),
                        "%H:%M",
                    ).time(),
                    available_to=datetime.strptime(
                        required_text(row, "available_to"),
                        "%H:%M",
                    ).time(),
                    max_price=Decimal(required_text(row, "max_price")),
                )

                session.merge(student)
                count += 1
            except (ValueError, TypeError) as error:
                raise ValueError(
                    f"Invalid student data on line {line_number}: {error}"
                ) from error

    return count


def import_events(session):
    count = 0

    with EVENTS_CSV.open(encoding="utf-8") as file:
        for line_number, row in enumerate(csv.DictReader(file), start=2):
            try:
                capacity = int(required_text(row, "capacity"))
                registered_count = int(required_text(row, "registered_count"))

                if capacity < 1:
                    raise ValueError("Capacity must be at least 1.")

                if registered_count < 0 or registered_count > capacity:
                    raise ValueError("Registered count must be between 0 and capacity.")

                event = Event(
                    id=int(required_text(row, "event_id")),
                    title=required_text(row, "title"),
                    description=required_text(row, "description"),
                    category=required_text(row, "category"),
                    organizer=required_text(row, "organizer"),
                    location_name=required_text(row, "location_name"),
                    latitude=Decimal(required_text(row, "latitude")),
                    longitude=Decimal(required_text(row, "longitude")),
                    start_datetime=datetime.strptime(
                        required_text(row, "start_datetime"),
                        "%Y-%m-%d %H:%M",
                    ),
                    end_datetime=datetime.strptime(
                        required_text(row, "end_datetime"),
                        "%Y-%m-%d %H:%M",
                    ),
                    capacity=capacity,
                    registered_count=registered_count,
                    target_audience=required_text(row, "target_audience"),
                    price=Decimal(required_text(row, "price")),
                    is_online=parse_boolean(row.get("is_online", "")),
                )

                session.merge(event)
                count += 1
            except (ValueError, TypeError) as error:
                raise ValueError(
                    f"Invalid event data on line {line_number}: {error}"
                ) from error

    return count


def main():
    session = SessionLocal()

    try:
        student_count = import_students(session)
        event_count = import_events(session)
        session.commit()

        print(f"Imported {student_count} students.")
        print(f"Imported {event_count} events.")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()