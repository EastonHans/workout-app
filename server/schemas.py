from marshmallow import validates, ValidationError, fields, pre_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from models import Exercise, Workout, WorkoutExercise, db

VALID_CATEGORIES = ["strength", "cardio", "flexibility", "balance", "hiit", "other"]


class WorkoutExerciseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = WorkoutExercise
        load_instance = True
        sqla_session = db.session
        include_fk = True

    exercise = fields.Nested(
        lambda: ExerciseSchema(only=("id", "name", "category", "equipment_needed")),
        dump_only=True,
    )

    @validates("sets")
    def validate_sets(self, value):
        if value is not None and value <= 0:
            raise ValidationError("sets must be greater than 0")

    @validates("reps")
    def validate_reps(self, value):
        if value is not None and value <= 0:
            raise ValidationError("reps must be greater than 0")

    @validates("duration_seconds")
    def validate_duration_seconds(self, value):
        if value is not None and value <= 0:
            raise ValidationError("duration_seconds must be greater than 0")


class ExerciseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise
        load_instance = True
        sqla_session = db.session

    workouts = fields.Nested(
        lambda: WorkoutSchema(only=("id", "date", "duration_minutes", "notes")),
        many=True,
        dump_only=True,
    )

    @validates("name")
    def validate_name(self, value):
        if not value or not value.strip():
            raise ValidationError("name can't be empty")

    @validates("category")
    def validate_category(self, value):
        if not value or value.lower() not in VALID_CATEGORIES:
            raise ValidationError(f"category must be one of: {VALID_CATEGORIES}")

    @pre_load
    def normalize(self, data, **kwargs):
        if "category" in data and isinstance(data["category"], str):
            data["category"] = data["category"].lower()
        return data


class WorkoutSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Workout
        load_instance = True
        sqla_session = db.session

    workout_exercises = fields.Nested(
        WorkoutExerciseSchema(only=("id", "exercise_id", "exercise", "reps", "sets", "duration_seconds")),
        many=True,
        dump_only=True,
    )

    @validates("duration_minutes")
    def validate_duration(self, value):
        if value is None or value <= 0:
            raise ValidationError("duration_minutes must be greater than 0")

    @validates("date")
    def validate_date(self, value):
        if value is None:
            raise ValidationError("date is required")


exercise_schema = ExerciseSchema()
workout_schema = WorkoutSchema()
workout_exercise_schema = WorkoutExerciseSchema()

exercises_schema = ExerciseSchema(many=True, exclude=("workouts",))
workouts_schema = WorkoutSchema(many=True, exclude=("workout_exercises",))
