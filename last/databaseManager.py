from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String(64), nullable=False)
    first_name = Column(String(64), nullable=False)
    last_name_katakana = Column(String(64), nullable=False)
    first_name_katakana = Column(String(64), nullable=False)
    birthday = Column(Date, nullable=False)
    gender = Column(Integer, nullable=False)
    email = Column(String(128), nullable=False)
    phone = Column(String(21), nullable=False)
    mobile_phone = Column(String(15), nullable=False)
    postal_code = Column(String(23), nullable=False)
    address = Column(String(256), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    status = Column(Integer, nullable=False)
    course_ = relationship("Course", back_populates="students")

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String(6), nullable=False)
    name = Column(String(64), nullable=False)
    classroom_id = Column(String(64), ForeignKey('classrooms.id'), nullable=False)
    students = relationship("Student", back_populates="course_")
    classroom = relationship("Classroom", back_populates="courses")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(256), nullable=False)
    password = Column(String(256), nullable=False)

class Classroom(Base):
    __tablename__ = 'classrooms'
    id = Column(Integer, primary_key=True, autoincrement=True)
    classroom_name = Column(String(256), nullable=False)
    courses = relationship("Course", back_populates="classroom")

# Initialize the database engine
engine = create_engine('sqlite:///db/school.db')

# Create the database schema
Base.metadata.create_all(engine)
