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

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db, directory="../migrations")
db.init_app(app)


@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(exercises_schema.dump(exercises), 200)


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)
    return make_response(exercise_schema.dump(exercise), 200)


@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "no data provided"}), 400)
    try:
        exercise = exercise_schema.load(data)
        db.session.add(exercise)
        db.session.commit()
        return make_response(exercise_schema.dump(exercise), 201)
    except ValidationError as e:
        return make_response(jsonify({"error": e.messages}), 400)
    except (IntegrityError, ValueError) as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e.orig if hasattr(e, "orig") else e)}), 400)


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)
    db.session.delete(exercise)
    db.session.commit()
    return make_response({}, 204)


@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(workouts_schema.dump(workouts), 200)


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)
    return make_response(workout_schema.dump(workout), 200)


@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "no data provided"}), 400)
    try:
        workout = workout_schema.load(data)
        db.session.add(workout)
        db.session.commit()
        return make_response(workout_schema.dump(workout), 201)
    except ValidationError as e:
        return make_response(jsonify({"error": e.messages}), 400)
    except (IntegrityError, ValueError) as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e.orig if hasattr(e, "orig") else e)}), 400)


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)
    db.session.delete(workout)
    db.session.commit()
    return make_response({}, 204)


@app.route("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises", methods=["POST"])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)

    exercise = db.session.get(Exercise, exercise_id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)

    data = request.get_json() or {}
    data["workout_id"] = workout_id
    data["exercise_id"] = exercise_id

    try:
        we = workout_exercise_schema.load(data)
        db.session.add(we)
        db.session.commit()
        return make_response(workout_exercise_schema.dump(we), 201)
    except ValidationError as e:
        return make_response(jsonify({"error": e.messages}), 400)
    except (IntegrityError, ValueError) as e:
        db.session.rollback()
        return make_response(jsonify({"error": str(e.orig if hasattr(e, "orig") else e)}), 400)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
