from databaseManager import Student,Class
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
                          'gender':'str',
                          'email':'str',
                          'phone':'str',
                          'mobile_phone':'str',
                          'postal_code':'str',
                          'address':'str',
                          'class_id':'str',
                          'status':'str',
                          }
                  )

# データベース接続の設定
engine = create_engine('sqlite:///school.db')
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
        class_id=row['class_id'],
        status=row['status']
    )
    session.add(student)

session.commit()
session.close()



excel_file = 'sutudentData.xlsx'
df = pd.read_excel(excel_file,sheet_name='class',
                  dtype= {'class_number':'str',
                          'class_name':'str',
                          'classroom_id':'str',
                          })


engine = create_engine('sqlite:///school.db')
Session = sessionmaker(bind=engine)
session = Session()


for index, row in df.iterrows():
    classes = Class(
        class_number=row['class_number'],
        class_name=row['class_name'],
        classroom_id=row['classroom_id'],
    )
    session.add(classes)

session.commit()
session.close()

