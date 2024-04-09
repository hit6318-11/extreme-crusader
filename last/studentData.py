from databaseManager import Student
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Excelファイルからデータを読み込む
excel_file = 'sutudentData.xlsx'
df = pd.read_excel(excel_file)

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




