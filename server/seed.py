from datetime import date
from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():

    # clear out old data
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    # exercises
    squat = Exercise(name="Barbell Back Squat", category="strength", equipment_needed=True)
    deadlift = Exercise(name="Deadlift", category="strength", equipment_needed=True)
    push_up = Exercise(name="Push-Up", category="strength", equipment_needed=False)
    run = Exercise(name="Treadmill Run", category="cardio", equipment_needed=True)
    plank = Exercise(name="Plank", category="flexibility", equipment_needed=False)
    burpee = Exercise(name="Burpee", category="hiit", equipment_needed=False)

    db.session.add_all([squat, deadlift, push_up, run, plank, burpee])
    db.session.commit()

    # workouts
    leg_day = Workout(date=date(2026, 7, 21), duration_minutes=60, notes="heavy leg day, focus on form")
    cardio_session = Workout(date=date(2026, 7, 22), duration_minutes=45, notes="steady state cardio and core")
    full_body = Workout(date=date(2026, 7, 24), duration_minutes=75, notes="full body circuit, 3 rounds")

    db.session.add_all([leg_day, cardio_session, full_body])
    db.session.commit()

    # link exercises to workouts
    db.session.add_all([
        WorkoutExercise(workout_id=leg_day.id, exercise_id=squat.id, sets=4, reps=8),
        WorkoutExercise(workout_id=leg_day.id, exercise_id=deadlift.id, sets=3, reps=5),
        WorkoutExercise(workout_id=cardio_session.id, exercise_id=run.id, duration_seconds=1800),
        WorkoutExercise(workout_id=cardio_session.id, exercise_id=plank.id, sets=3, duration_seconds=60),
        WorkoutExercise(workout_id=full_body.id, exercise_id=push_up.id, sets=3, reps=15),
        WorkoutExercise(workout_id=full_body.id, exercise_id=burpee.id, sets=3, reps=10),
        WorkoutExercise(workout_id=full_body.id, exercise_id=squat.id, sets=3, reps=12),
    ])
    db.session.commit()

    print("done seeding")
