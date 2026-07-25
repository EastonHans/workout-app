# Workout Tracker API

A RESTful backend API for personal trainers to track workouts and their associated exercises. Built with Flask, SQLAlchemy, Flask-Migrate, and Marshmallow.

---

## Features

- Create, view, and delete **Workouts** (date, duration, notes)
- Create, view, and delete reusable **Exercises** (name, category, equipment needed)
- Add an **Exercise to a Workout** with performance data (sets, reps, or duration)
- Model-level and schema-level validations with meaningful error messages
- Database constraints enforcing data integrity

---

## Tech Stack

| Tool | Version |
|------|---------|
| Python | 3.13 |
| Flask | 3.0.3 |
| Flask-SQLAlchemy | 3.1.1 |
| Flask-Migrate | 4.0.7 |
| Marshmallow | 3.21.3 |
| marshmallow-sqlalchemy | 1.1.0 |

---

## Installation

**1. Clone the repository**

```bash
git clone <your-repo-url>
cd workout-app
```

**2. Install dependencies with Pipenv**

```bash
pipenv install
```

**3. Navigate into the server directory**

```bash
cd server
```

**4. Initialize and run the database migrations**

```bash
flask --app app.py db init
flask --app app.py db migrate -m "Initial migration"
flask --app app.py db upgrade head
```

**5. Seed the database with example data**

```bash
python seed.py
```

---

## Running the Server

From inside the `server/` directory:

```bash
python app.py
```

The API will be available at `http://localhost:5555`.

---

## API Endpoints

### Exercises

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/exercises` | List all exercises |
| `GET` | `/exercises/<id>` | Get a single exercise with its associated workouts |
| `POST` | `/exercises` | Create a new exercise |
| `DELETE` | `/exercises/<id>` | Delete an exercise (cascades WorkoutExercise records) |

**POST `/exercises` — Request Body**

```json
{
  "name": "Barbell Back Squat",
  "category": "strength",
  "equipment_needed": true
}
```

Valid categories: `strength`, `cardio`, `flexibility`, `balance`, `hiit`, `other`

---

### Workouts

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/workouts` | List all workouts |
| `GET` | `/workouts/<id>` | Get a single workout with exercises, sets, reps, and duration |
| `POST` | `/workouts` | Create a new workout |
| `DELETE` | `/workouts/<id>` | Delete a workout (cascades WorkoutExercise records) |

**POST `/workouts` — Request Body**

```json
{
  "date": "2026-07-25",
  "duration_minutes": 60,
  "notes": "Optional notes here"
}
```

---

### WorkoutExercises

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout |

**POST body (all fields optional):**

```json
{
  "sets": 4,
  "reps": 8,
  "duration_seconds": null
}
```

---

## Validations

### Table Constraints
- `exercises.name` — `NOT NULL`, `UNIQUE`
- `exercises.category` — `NOT NULL`
- `workouts.date` — `NOT NULL`
- `workouts.duration_minutes` — `NOT NULL`, check constraint `> 0`
- `workout_exercises.workout_id` + `exercise_id` — `UNIQUE` together (prevents duplicate entries)

### Model Validations (SQLAlchemy `@validates`)
- `Exercise.name` — cannot be blank
- `Exercise.category` — must be one of the allowed values
- `Workout.duration_minutes` — must be a positive integer
- `Workout.date` — cannot be null
- `WorkoutExercise.sets/reps/duration_seconds` — must be positive when provided

### Schema Validations (Marshmallow)
- `ExerciseSchema.name` — cannot be blank
- `ExerciseSchema.category` — must be an allowed category
- `WorkoutSchema.duration_minutes` — must be positive
- `WorkoutSchema.date` — required field
- `WorkoutExerciseSchema.sets/reps/duration_seconds` — must be positive when provided
