from flask import Flask, request, jsonify, session, render_template, request, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from databaseManager import Base, Student  # 事前に定義したStudentクラスをimport

app = Flask(__name__)
# SQLiteデータベース 'school.db' への接続を設定します。
engine = create_engine('sqlite:///school.db')
Base.metadata.bind = engine

# セッションファクトリを作成し、スレッドセーフなセッションを確保します。
db_session = scoped_session(sessionmaker(bind=engine))


# サイトのルーティング
@app.route('/')
def goToIndex():
    return render_template(
        "login.html"
    )
@app.route('/login')
def goToLogin():
    return render_template(
        "login.html"
    )
@app.route('/search')
def goToSearch():
    return render_template(
        "search.html"
    )
@app.route('/result')
def goToResult():
    return render_template(
        "result.html"
    )
@app.route('/form')
def goToForm():
    return render_template(
        "form.html"
    )


# 生徒情報の作成を行うエンドポイント
@app.route('/students', methods=['POST'])
def create_student():
    data = request.json  # リクエストボディからJSONデータを取得
    student = Student(**data)  # Studentインスタンスを作成
    db_session.add(student)  # セッションに追加
    db_session.commit()  # データベースにコミット
    return jsonify(student.id), 201  # 作成した生徒のIDとHTTPステータスコード201を返す

# 生徒情報の取得を行うエンドポイント
@app.route('/students', methods=['GET'])
def get_students():
    students = db_session.query(Student).all()  # すべての生徒情報を取得
    return jsonify([{
        'id': student.id,
        'first_name': student.first_name,
        'last_name': student.last_name,
        'last_name_katakana': student.last_name_katakana,
        'first_name_katakana': student.first_name_katakana,
        'birthday': student.birthday.isoformat(),  # 日付はISOフォーマットに変換
        'gender': student.gender,
        'email': student.email,
        'phone': student.phone,
        'mobile_phone': student.mobile_phone,
        'postal_code': student.postal_code,
        'address': student.address,
        'class_id': student.class_id,
        'status': student.status
    } for student in students])  # 生徒情報をJSON形式で返す

# 生徒情報の更新を行うエンドポイント
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.json  # リクエストボディからJSONデータを取得
    student = db_session.query(Student).filter(Student.id == student_id).first()  # 更新対象の生徒を検索
    if student:
        for key, value in data.items():
            setattr(student, key, value)  # 存在するフィールドの値を更新
        db_session.commit()  # データベースにコミット
        return jsonify(success=True)
    return jsonify(success=False), 404  # 生徒が見つからない場合は404エラー

# 生徒情報の削除を行うエンドポイント
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = db_session.query(Student).filter(Student.id == student_id).first()  # 削除対象の生徒を検索
    if student:
        db_session.delete(student)  # セッションから削除
        db_session.commit()  # データベースにコミット
        return jsonify(success=True)
    return jsonify(success=False), 404  # 生徒が見つからない場合は404エラー

if __name__ == '__main__':
    app.run(debug=True)  # アプリケーションをデバッグモードで起動


#このコードスニペットでは、生徒情報のCRUD操作（作成、読み取り、更新、削除）を行うためのエンドポイントを提供します。
#各エンドポイントでは、クライアントからのリクエストに基づいて適切な操作を実行し、結果をJSON形式で返します。
#また、生徒情報の取得では、isoformat()メソッドを使用して日付をISO 8601形式に変換しています。
#これにより、フロントエンドでの日付の取り扱いが容易になります。