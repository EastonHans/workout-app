from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship("WorkoutExercise", back_populates="exercise", cascade="all, delete-orphan")
    workouts = db.relationship("Workout", secondary="workout_exercises", back_populates="exercises", viewonly=True)

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("name can't be empty")
        return value.strip()

    @validates("category")
    def validate_category(self, key, value):
        valid = ["strength", "cardio", "flexibility", "balance", "hiit", "other"]
        if not value or value.lower() not in valid:
            raise ValueError(f"category must be one of: {valid}")
        return value.lower()

    def __repr__(self):
        return f"<Exercise {self.name}>"


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    __table_args__ = (
        db.CheckConstraint("duration_minutes > 0", name="ck_workout_duration_positive"),
    )

    workout_exercises = db.relationship("WorkoutExercise", back_populates="workout", cascade="all, delete-orphan")
    exercises = db.relationship("Exercise", secondary="workout_exercises", back_populates="workouts", viewonly=True)

    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if not value or int(value) <= 0:
            raise ValueError("duration_minutes must be greater than 0")
        return int(value)

    @validates("date")
    def validate_date(self, key, value):
        if value is None:
            raise ValueError("date is required")
        return value

    def __repr__(self):
        return f"<Workout {self.date}>"


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    __table_args__ = (
        db.UniqueConstraint("workout_id", "exercise_id", name="uq_workout_exercise"),
    )

    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    @validates("sets")
    def validate_sets(self, key, value):
        if value is not None and int(value) <= 0:
            raise ValueError("sets must be greater than 0")
        return value

    @validates("reps")
    def validate_reps(self, key, value):
        if value is not None and int(value) <= 0:
            raise ValueError("reps must be greater than 0")
        return value

    @validates("duration_seconds")
    def validate_duration_seconds(self, key, value):
        if value is not None and int(value) <= 0:
            raise ValueError("duration_seconds must be greater than 0")
        return value

    def __repr__(self):
        return f"<WorkoutExercise workout={self.workout_id} exercise={self.exercise_id}>"
