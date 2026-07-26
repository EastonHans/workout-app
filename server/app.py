import os
from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    exercise_schema,
    exercises_schema,
    workout_schema,
    workouts_schema,
    workout_exercise_schema,
)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db, directory=os.path.join(BASE_DIR, "..", "migrations"))
db.init_app(app)


def error_response(message, status=400):
    return make_response(jsonify({"error": message}), status)


# Exercises

@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(exercises_schema.dump(exercises), 200)


@app.route("/exercises/<int:exercise_id>", methods=["GET"])
def get_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)
    if not exercise:
        return error_response("Exercise not found.", 404)
    return make_response(exercise_schema.dump(exercise), 200)


@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json()
    if not data:
        return error_response("Request body must be JSON.")
    try:
        new_exercise = exercise_schema.load(data)
        db.session.add(new_exercise)
        db.session.commit()
        return make_response(exercise_schema.dump(new_exercise), 201)
    except ValidationError as e:
        return error_response(e.messages)
    except (IntegrityError, ValueError) as e:
        db.session.rollback()
        return error_response(str(e.orig if hasattr(e, "orig") else e))


@app.route("/exercises/<int:exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id):
    exercise = db.session.get(Exercise, exercise_id)
    if not exercise:
        return error_response("Exercise not found.", 404)
    db.session.delete(exercise)
    db.session.commit()
    return make_response({}, 204)


# Workouts

@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(workouts_schema.dump(workouts), 200)


@app.route("/workouts/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):
    workout = db.session.get(Workout, workout_id)
    if not workout:
        return error_response("Workout not found.", 404)
    return make_response(workout_schema.dump(workout), 200)


@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json()
    if not data:
        return error_response("Request body must be JSON.")
    try:
        new_workout = workout_schema.load(data)
        db.session.add(new_workout)
        db.session.commit()
        return make_response(workout_schema.dump(new_workout), 201)
    except ValidationError as e:
        return error_response(e.messages)
    except (IntegrityError, ValueError) as e:
        db.session.rollback()
        return error_response(str(e.orig if hasattr(e, "orig") else e))


@app.route("/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    workout = db.session.get(Workout, workout_id)
    if not workout:
        return error_response("Workout not found.", 404)
    db.session.delete(workout)
    db.session.commit()
    return make_response({}, 204)


# WorkoutExercises

@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"],
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    if not workout:
        return error_response("Workout not found.", 404)

    exercise = db.session.get(Exercise, exercise_id)
    if not exercise:
        return error_response("Exercise not found.", 404)

    data = request.get_json() or {}
    data["workout_id"] = workout_id
    data["exercise_id"] = exercise_id

    try:
        new_we = workout_exercise_schema.load(data)
        db.session.add(new_we)
        db.session.commit()
        return make_response(workout_exercise_schema.dump(new_we), 201)
    except ValidationError as e:
        return error_response(e.messages)
    except (IntegrityError, ValueError) as e:
        db.session.rollback()
        return error_response(str(e.orig if hasattr(e, "orig") else e))


if __name__ == "__main__":
    app.run(port=5555, debug=True)
