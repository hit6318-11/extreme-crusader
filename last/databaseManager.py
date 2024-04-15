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
    birthday = Column(Date, nullable=False) # data型へ戻した
    gender = Column(Integer, nullable=False) #intへ変更
    email = Column(String(128), nullable=False)
    phone = Column(String(21), nullable=False) #intからstrへ変更
    mobile_phone = Column(String(15), nullable=False)
    postal_code = Column(String(23), nullable=False)
    address = Column(String(256), nullable=False)
    class_id = Column(Integer, ForeignKey('classes.id'), nullable=False)
    status = Column(Integer, nullable=False) 
    # Relation to Class
    class_ = relationship("Class", back_populates="students")

class Class(Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_number = Column(String(6), nullable=False)
    class_name = Column(String(64), nullable=False)
    classroom_id = Column(String(64), ForeignKey('classrooms.id'), nullable=False)
    # Relations
    students = relationship("Student", back_populates="class_")
    classroom = relationship("Classroom", back_populates="classes")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(256), nullable=False)
    password = Column(String(256), nullable=False)

class Classroom(Base):
    __tablename__ = 'classrooms'
    id = Column(Integer, primary_key=True, autoincrement=True)
    classroom_name = Column(String(256), nullable=False)
    # Relation to Class
    classes = relationship("Class", back_populates="classroom")

engine = create_engine('sqlite:///db/school.db')
Base.metadata.create_all(engine)
