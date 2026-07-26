from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Exercise(db.Model):
    # Reusable exercise that can be added to any workout
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan",
    )
    workouts = db.relationship(
        "Workout",
        secondary="workout_exercises",
        back_populates="exercises",
        viewonly=True,
    )

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Exercise name cannot be blank.")
        return value.strip()

    @validates("category")
    def validate_category(self, key, value):
        allowed = {"strength", "cardio", "flexibility", "balance", "hiit", "other"}
        if not value or value.lower() not in allowed:
            raise ValueError(
                f"Category must be one of: {', '.join(sorted(allowed))}."
            )
        return value.lower()

    def __repr__(self):
        return f"<Exercise id={self.id} name={self.name!r} category={self.category}>"


class Workout(db.Model):
    # A single training session on a given date
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    __table_args__ = (
        db.CheckConstraint("duration_minutes > 0", name="ck_workout_duration_positive"),
    )

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan",
    )
    exercises = db.relationship(
        "Exercise",
        secondary="workout_exercises",
        back_populates="workouts",
        viewonly=True,
    )

    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if value is None or int(value) <= 0:
            raise ValueError("duration_minutes must be a positive integer.")
        return int(value)

    @validates("date")
    def validate_date(self, key, value):
        if value is None:
            raise ValueError("Workout date cannot be null.")
        return value

    def __repr__(self):
        return f"<Workout id={self.id} date={self.date} duration={self.duration_minutes}min>"


class WorkoutExercise(db.Model):
    # Join table linking a workout to an exercise, with sets/reps/duration data
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    # Prevent the same exercise from being added to the same workout twice
    __table_args__ = (
        db.UniqueConstraint("workout_id", "exercise_id", name="uq_workout_exercise"),
    )

    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    @validates("sets")
    def validate_sets(self, key, value):
        if value is not None and int(value) <= 0:
            raise ValueError("sets must be a positive integer.")
        return value

    @validates("reps")
    def validate_reps(self, key, value):
        if value is not None and int(value) <= 0:
            raise ValueError("reps must be a positive integer.")
        return value

    @validates("duration_seconds")
    def validate_duration_seconds(self, key, value):
        if value is not None and int(value) <= 0:
            raise ValueError("duration_seconds must be a positive integer.")
        return value

    def __repr__(self):
        return (
            f"<WorkoutExercise workout={self.workout_id} "
            f"exercise={self.exercise_id} sets={self.sets} reps={self.reps}>"
        )
