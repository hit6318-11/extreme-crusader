import json
from flask import Flask, request, jsonify, session, render_template, request, url_for, redirect
from sqlalchemy import or_
from datetime import datetime
from sqlalchemy.orm import scoped_session, sessionmaker, joinedload
from databaseManager import Base, Student, Course, engine  # データベースエンジンのインポート
from hash import User  # ユーザーハッシュのインポート

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# データベースエンジンをベースクラスのメタデータにバインド
Base.metadata.bind = engine

# スレッドセーフなセッションファクトリを作成
db_session = scoped_session(sessionmaker(bind=engine))

def is_logged_in():
    return 'username' in session

# サイトのルーティング
@app.route('/')
def index():
    if not is_logged_in():
        return redirect(url_for('login'))
    else:
        username = session.get('username')
    return render_template("search.html", username=username)

# ログインルート
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = db_session.query(User).filter(User.username == username).first()
        if user and user.check_password(password):
            session['username'] = user.username
            return redirect(url_for('search'))
        else:
            return render_template("login.html", error="無効な資格情報です。もう一度お試しください。")
    return render_template("login.html")

# ログアウトルート
@app.route('/logout')
def logout():
    if not is_logged_in():
        return redirect(url_for('login'))
    else:
        session.clear()
    return redirect(url_for('login'))

@app.route('/search')
def search():
    if not is_logged_in():
        return redirect(url_for('login'))
    else:
        username = session.get('username')
    return render_template("search.html", username=username)

@app.route('/result')
def result():
    if not is_logged_in():
        return redirect(url_for('login'))
    else:
        username = session.get('username')
    # セッションストレージから学生データを取得
    student_data = json.loads(session.get('searchResults', '[]'))
    # 学生データをテンプレートに渡す
    return render_template("result.html", students_data=student_data, username=username)

@app.route('/form')
def form():
    if not is_logged_in():
        return redirect(url_for('login'))
    else:
        username = session.get('username')
    return render_template("form.html", username=username)

@app.route('/confirm')
def confirm():
    if not is_logged_in():
        return redirect(url_for('login'))
    else:
        username = session.get('username')
    return render_template("confirm.html", username=username)

# 学生エンドポイントの作成
@app.route('/api/students', methods=['POST'])
def create_student():
    data = request.json
    # 誕生日の文字列をPythonの日付オブジェクトに変換
    if 'birthday' in data:
        data['birthday'] = datetime.strptime(data['birthday'], '%Y-%m-%d').date()
    student = Student(**data)
    db_session.add(student)
    db_session.commit()
    return jsonify(student.id), 201

@app.route('/api/students', methods=['GET'])
def get_students():
    query_parameters = request.args.to_dict()  # クエリパラメータを辞書として取得
    order_by = query_parameters.pop('order_by', 'id')  # ソート基準のパラメータ
    ascending = query_parameters.pop('ascending', 'true').lower() == 'true'  # 昇順か降順か

    base_query = db_session.query(Student)  # 学生テーブルからクエリを開始

    if 'id' in query_parameters and query_parameters['id']:
        studentId = int(query_parameters['id'])
        student = base_query.filter(Student.id == studentId).first()
        if student:
            return jsonify([build_student_json(student)])
        else:
            return jsonify([])  # 学生が見つからない場合は空のリストを返す

    or_conditions = []
    for attr, value in query_parameters.items():
        if hasattr(Student, attr):  # 学生クラスに属性が存在するかチェック
            column = getattr(Student, attr)  # 属性に対応するカラムオブジェクトを取得
            or_conditions.append(column.ilike(f'%{value}%'))  # 部分一致検索を設定

    if or_conditions:
        base_query = base_query.filter(or_(*or_conditions))  # 複数条件のORを適用

    # ソート処理
    order_expr = getattr(Student, order_by)
    if not ascending:
        order_expr = order_expr.desc()
    students = base_query.order_by(order_expr).all()  # クエリ実行

    # 結果をJSON形式で整形して返す
    results = [build_student_json(student) for student in students]
    return jsonify(results)

def build_student_json(student):
    return {
        'id': student.id,
        'name': f'{student.last_name} {student.first_name}',
        'lastName': student.last_name,
        'firstName': student.first_name,
        'lastNameKana': student.last_name_katakana,
        'firstNameKana': student.first_name_katakana,
        'birthday': student.birthday,
        'gender': student.gender,
        'email': student.email,
        'phone': student.phone,
        'mobilePhone': student.mobile_phone,
        'postalCode': student.postal_code,
        'address': student.address,
        'classId': student.course_id,
        'course_id': student.course_id,
        'course_number': student.course_.number,
        'course_name': student.course_.name,
        'status': student.status
    }

# 学生の更新エンドポイント
@app.route('/api/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.json
    if 'birthday' in data:
        data['birthday'] = datetime.strptime(data['birthday'], '%Y-%m-%d').date()
    student = db_session.query(Student).filter(Student.id == student_id).first()
    if student:
        for key, value in data.items():
            setattr(student, key, value)
        db_session.commit()
        return jsonify(success=True)
    return jsonify(success=False), 404

# 学生の削除エンドポイント
@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student_int_id = int(student_id)
    student = db_session.query(Student).filter(Student.id == student_int_id).first()
    if student:
        db_session.delete(student)
        db_session.commit()
        return jsonify(success=True)
    return jsonify(success=False), 404

@app.route('/api/courses', methods=['GET'])
def get_courses():
    courses = db_session.query(Course).all()
    results = [{
        'id': course.id,
        'course_number': course.number,
        'course_name': course.name,
        'classroom_id': course.classroom_id
    } for course in courses]
    return jsonify(results)

@app.route('/api/courses', methods=['POST'])
def create_course():
    data = request.json
    new_course = Course(**data)
    db_session.add(new_course)
    db_session.commit()
    return jsonify(new_course.id), 201

@app.route('/api/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    data = request.json
    course = db_session.query(Course).get(course_id)
    if course:
        for key, value in data.items():
            setattr(course, key, value)
        db_session.commit()
        return jsonify(success=True)
    return jsonify(success=False), 404

@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    course = db_session.query(Course).get(course_id)
    if course:
        db_session.delete(course)
        db_session.commit()
        return jsonify(success=True)
    return jsonify(success=False), 404

@app.route('/api/users', methods=['GET'])
def get_user():
    users = db_session.query(User).all()
    results = [{
        'id': user.id,
        'email': user.number,
        'password': user.password,
    } for user in users]
    return jsonify(results)

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(**data)
    db_session.add(new_user)
    db_session.commit()
    return jsonify(new_user.id), 201

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    user = db_session.query(User).get(user_id)
    if user:
        for key, value in data.items():
            setattr(user, key, value)
        db_session.commit()
        return jsonify(success=True)
    return jsonify(success=False), 404

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = db_session.query(User).get(user_id)
    if user:
        db_session.delete(user)
        db_session.commit()
        return jsonify(success=True)
    return jsonify(success=False), 404

if __name__ == '__main__':
    app.run(debug=True)
