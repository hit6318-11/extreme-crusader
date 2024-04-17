from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash


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

class User(Base):
    """ユーザーテーブルのORMクラス"""
    __tablename__ = 'users'  # テーブル名を指定
    id = Column(Integer, primary_key=True)  # IDは主キーとして自動インクリメントされる
    username = Column(String, unique=True, nullable=False)  # ユーザー名は一意である必要があり、nullは不可
    password_hash = Column(String, nullable=False)  # パスワードハッシュ、nullは不可
    
    # パスワードを設定するメソッド。パスワードをハッシュ化して保存
    def set_password(self, password):
        """パスワードをハッシュ化して設定するメソッド"""
        self.password_hash = generate_password_hash(password)
    
    # 提供されたパスワードが正しいかどうかを検証するメソッド
    def check_password(self, password):
        """提供されたパスワードが正しいかどうかを検証するメソッド"""
        return check_password_hash(self.password_hash, password)

# データベースエンジンの初期化
engine = create_engine('sqlite:///db/school.db')

# データベーススキーマの作成
Base.metadata.create_all(engine)
