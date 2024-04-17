from databaseManager import Student,Course, User
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime


# Excelファイルからデータを読み込む
excel_file = 'sutudentData.xlsx'
df = pd.read_excel(excel_file,sheet_name='student',
                dtype= {'last_name':'str',
                        'first_name':'str',
                        'last_name_katakana':'str',
                        'first_name_katakana':'str',
                        'birthday':'object',
                        'gender':'int',
                        'email':'str',
                        'phone':'str',
                        'mobile_phone':'str',
                        'postal_code':'str',
                        'address':'str',
                        'course_id':'int',
                        'status':'int',
                        }
                )

# データベース接続の設定
engine = create_engine('sqlite:///db/school.db')
Session = sessionmaker(bind=engine)
session = Session()


# ExcelデータをSQLiteデータベースに書き込む
for index, row in df.iterrows():
    student = Student(
        last_name=row['last_name'],
        first_name=row['first_name'],
        last_name_katakana=row['last_name_katakana'],
        first_name_katakana=row['first_name_katakana'],
        birthday=row['birthday'],
        gender=row['gender'],
        email=row['email'],
        phone=row['phone'],
        mobile_phone=row['mobile_phone'],
        postal_code=row['postal_code'],
        address=row['address'],
        course_id=row['course_id'],
        status=row['status']
    )
    session.add(student)

session.commit()
session.close()


excel_file = 'sutudentData.xlsx'
df = pd.read_excel(excel_file,sheet_name='course',
                dtype= {'number':'str',
                        'name':'str',
                        'classroom_id':'str',
                        })


engine = create_engine('sqlite:///db/school.db')
Session = sessionmaker(bind=engine)
session = Session()


for index, row in df.iterrows():
    courses = Course(
        number=row['number'],
        name=row['name'],
        classroom_id=row['classroom_id'],
    )
    session.add(courses)

session.commit()
session.close()

engine = create_engine('sqlite:///db/school.db')
Session = sessionmaker(bind=engine)
session = Session()

new_user = User(username='user')
new_user.set_password('pass')  # パスワードをハッシュ化して設定
session.add(new_user)  # 新しいユーザーをセッションに追加
session.commit()  # 変更をデータベースにコミット
session.close()