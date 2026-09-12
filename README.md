# Campus Event Recommendation System

A local web application that recommends relevant campus events to students.

## Overview

The system combines:

- PostgreSQL database for students and events
- FastAPI REST API
- SQLAlchemy ORM
- HTML, JavaScript, and Tailwind CSS frontend
- Haversine formula for distance calculation
- Deterministic recommendation scoring without machine learning

Students receive event recommendations based on their interests, available time, faculty, location, budget, and event capacity.

## Features

- 100 campus events imported from the provided CSV dataset
- 80 generated student profiles with multiple interests
- Event filtering by category, date, and free events
- Student selector with personalized recommendations
- Haversine distance calculation for physical events
- Online events handled with `0 km` distance
- Explainable recommendation score from 0 to 100
- Loading, error, and empty frontend states
- Responsive event cards built with Tailwind CSS
- Automated tests for distance logic, scoring, API endpoints, and filters

## Technology Stack

| Area | Technology |
|---|---|
| Backend | Python, FastAPI |
| Database ORM | SQLAlchemy |
| PostgreSQL driver | psycopg2-binary |
| Environment variables | python-dotenv |
| Database | PostgreSQL |
| Frontend | HTML, JavaScript, Tailwind CSS |
| Python environment | uv |
| Testing | pytest, httpx |

## Project Structure

campus-event-recommendation-system/
├── backend/
│   ├── models/
│   │   ├── event.py
│   │   └── student.py
│   ├── routers/
│   │   ├── events.py
│   │   ├── recommendations.py
│   │   └── students.py
│   ├── schemas/
│   ├── services/
│   │   ├── distance.py
│   │   └── recommendation.py
│   ├── config.py
│   ├── database.py
│   └── main.py
├── data/
│   └── raw/
│       ├── campus_events.csv
│       └── students.csv
├── frontend/
│   └── index.html
├── scripts/
│   ├── create_tables.py
│   ├── generate_students.py
│   └── import_data.py
├── tests/
│   ├── test_api.py
│   ├── test_distance.py
│   └── test_recommendation.py
├── .env.example
├── pyproject.toml
└── README.md
```

## Installation

### 1. Create the Python environment

```powershell
uv sync
```

### 2. Configure the database

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg2://campus_app:campus_dev_password@localhost:5432/campus_events
```

Create the PostgreSQL user and database:

```sql
CREATE USER campus_app WITH PASSWORD 'campus_dev_password';
CREATE DATABASE campus_events OWNER campus_app;
```

### 3. Create database tables

```powershell
uv run python -m scripts.create_tables
```

### 4. Generate and import the student dataset

```powershell
uv run python -m scripts.generate_students
uv run python -m scripts.import_data
```

The project imports:

- 100 campus events from `data/raw/campus_events.csv`
- 80 student profiles from `data/raw/students.csv`

## Running the Application

Start the FastAPI backend:

```powershell
uv run uvicorn backend.main:app --reload
```

Backend API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

Start the frontend in a separate terminal:

```powershell
uv run python -m http.server 5500 --directory frontend
```

Open the application:

```text
http://127.0.0.1:5500/?student_id=1
```

## REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Checks API and database connection |
| GET | `/students` | Returns all students |
| GET | `/students/{student_id}` | Returns one student |
| POST | `/students` | Creates a new student |
| GET | `/events` | Returns events with optional filters |
| GET | `/events/{event_id}` | Returns one event |
| POST | `/events` | Creates a new event |
| GET | `/recommendations/{student_id}` | Returns recommendations for a student |
| GET | `/recommendations?lat=...&lon=...&interests=...` | Returns recommendations for a custom location and interests |

### Event Filtering Examples

```text
GET /events?category=Technology
GET /events?date=2026-09-23
GET /events?free_only=true
GET /events?category=Technology&free_only=true
```

## Recommendation Scoring

The project uses deterministic and explainable scoring.

| Factor | Maximum points | Rule |
|---|---:|---|
| Interest match | 30 | Event category matches one of the student's interests |
| Time availability | 20 | Full match: 20 points; partial match: 10 points |
| Faculty / audience match | 15 | Event is for the student's