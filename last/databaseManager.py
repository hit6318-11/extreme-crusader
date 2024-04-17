from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Student(Base):
    """学生テーブルのORMクラス"""
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String(64), nullable=False)  # 姓
    first_name = Column(String(64), nullable=False)  # 名
    last_name_katakana = Column(String(64), nullable=False)  # 姓（カタカナ）
    first_name_katakana = Column(String(64), nullable=False)  # 名（カタカナ）
    birthday = Column(Date, nullable=False)  # 誕生日
    gender = Column(Integer, nullable=False)  # 性別
    email = Column(String(128), nullable=False)  # メール
    phone = Column(String(21), nullable=False)  # 電話番号
    mobile_phone = Column(String(15), nullable=False)  # 携帯電話番号
    postal_code = Column(String(23), nullable=False)  # 郵便番号
    address = Column(String(256), nullable=False)  # 住所
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)  # コースID
    status = Column(Integer, nullable=False)  # ステータス
    course_ = relationship("Course", back_populates="students")  # コースとのリレーションシップ

class Course(Base):
    """コーステーブルのORMクラス"""
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String(6), nullable=False)  # コース番号
    name = Column(String(64), nullable=False)  # コース名
    classroom_id = Column(String(64), ForeignKey('classrooms.id'), nullable=False)  # 教室ID
    students = relationship("Student", back_populates="course_")  # 学生とのリレーションシップ
    classroom = relationship("Classroom", back_populates="courses")  # 教室とのリレーションシップ

class Classroom(Base):
    """教室テーブルのORMクラス"""
    __tablename__ = 'classrooms'
    id = Column(Integer, primary_key=True, autoincrement=True)
    classroom_name = Column(String(256), nullable=False)  # 教室名
    courses = relationship("Course", back_populates="classroom")  # コースとのリレーションシップ

# データベースエンジンの初期化
engine = create_engine('sqlite:///db/school.db')

# データベーススキーマの作成
Base.metadata.create_all(engine)
