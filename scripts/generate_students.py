import csv
import random
from pathlib import Path

random.seed(42)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "students.csv"

categories = [
    "Technology", "Career", "Business", "Art", "Music",
    "Sport", "Volunteering", "Culture", "Science", "Networking",
    "Workshop", "Competition", "Health", "Student Club", "Language",
]

faculties = [
    "Computer Science",
    "Economics",
    "Design",
    "Engineering",
    "Law",
    "Medicine",
]

first_names = [
    "Ana", "Marko", "Elena", "Stefan", "Mila", "Nikola", "Sara",
    "David", "Ivana", "Filip", "Marija", "Aleksandar", "Katerina",
    "Petar", "Teodora", "Bojan", "Jovana", "Martin", "Angela", "Viktor",
]

last_names = [
    "Petrova", "Ivanov", "Stojanova", "Trajkovski",
    "Nikolovska", "Dimitrov", "Ristovska", "Kostov",
]

students = []

for student_id in range(1, 81):
    first_name = first_names[(student_id - 1) % len(first_names)]
    last_name = last_names[(student_id - 1) % len(last_names)]

    students.append({
        "student_id": student_id,
        "name": f"{first_name} {last_name}",
        "email": f"{first_name.lower()}.{last_name.lower()}{student_id}@example.com",
        "faculty": random.choice(faculties),
        "year_of_study": random.randint(1, 4),
        "latitude": round(41.9980 + random.uniform(-0.004, 0.004), 6),
        "longitude": round(21.4255 + random.uniform(-0.004, 0.004), 6),
        "interests": ",".join(random.sample(categories, k=3)),
        "available_from": random.choice(["09:00", "10:00", "12:00", "13:00", "14:00"]),
        "available_to": random.choice(["16:00", "17:00", "18:00", "19:00", "20:00"]),
        "max_price": random.choice([0, 5, 10, 15, 20]),
    })

with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=students[0].keys())
    writer.writeheader()
    writer.writerows(students)

print(f"Created {len(students)} students: {OUTPUT_PATH}")