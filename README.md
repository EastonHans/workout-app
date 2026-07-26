# Workout Tracker API

Backend API for personal trainers to log workouts and track exercises. Built with Flask and SQLAlchemy.

## Setup

Clone the repo and install dependencies:

```bash
git clone https://github.com/EastonHans/workout-app.git
cd workout-app
pipenv install
```

Set up the database (run from inside `server/`):

```bash
cd server
flask --app app.py db upgrade head
python seed.py
```

## Running

From inside `server/`:

```bash
python app.py
```

Runs on `http://localhost:5555`

## Endpoints

**Exercises**

- `GET /exercises` - list all exercises
- `GET /exercises/<id>` - get one exercise and its workouts
- `POST /exercises` - create an exercise
- `DELETE /exercises/<id>` - delete an exercise

**Workouts**

- `GET /workouts` - list all workouts
- `GET /workouts/<id>` - get one workout with its exercises and performance data
- `POST /workouts` - create a workout
- `DELETE /workouts/<id>` - delete a workout

**WorkoutExercises**

- `POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` - add an exercise to a workout

## Example request bodies

POST `/exercises`:
```json
{
  "name": "Deadlift",
  "category": "strength",
  "equipment_needed": true
}
```

Valid categories: `strength`, `cardio`, `flexibility`, `balance`, `hiit`, `other`

POST `/workouts`:
```json
{
  "date": "2026-07-25",
  "duration_minutes": 60,
  "notes": "leg day"
}
```

POST `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises`:
```json
{
  "sets": 3,
  "reps": 8
}
```

## Validations

Table constraints: `exercises.name` is unique and not null, `workouts.date` is not null, `workouts.duration_minutes` must be > 0, `workout_exercises` has a unique constraint on workout + exercise combo.

Model validations: exercise name can't be blank, category must be valid, workout duration must be positive, sets/reps/duration_seconds must be positive if provided.

Schema validations mirror the model validations and return JSON error messages on bad input.
