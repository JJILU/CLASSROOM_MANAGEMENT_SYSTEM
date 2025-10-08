
from datetime import datetime
from extensions import db

# --- Association table for Lecturers & Courses ---
lecturer_course = db.Table(
    "lecturer_course",
    db.Column("lecturer_id", db.Integer, db.ForeignKey("employed_lecturers.id")),
    db.Column("course_id", db.Integer, db.ForeignKey("course.id"))
)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    duration = db.Column(db.Integer)
    present_year = db.Column(db.Integer, default=datetime.now().year)

    students = db.relationship("Student", backref="course")


class RegisteredStudents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    student_id = db.Column(db.String(20), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # one-to-many relation with Course
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))
    course = db.relationship("Course", backref="registered_students")


class EmployedLecturers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    nrc_number = db.Column(db.String(20), unique=True)
    lecturer_id = db.Column(db.String(20), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # many-to-many relation with Course
    courses = db.relationship("Course", secondary=lecturer_course, backref="lecturers")