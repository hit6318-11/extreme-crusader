import json
from flask import Flask, request, jsonify, session, render_template, request, url_for, redirect
from sqlalchemy import or_
from sqlalchemy.orm import scoped_session, sessionmaker
from databaseManager import Base, Student, User, engine  # エンジンのインポート
import pprint

app = Flask(__name__)

# エンジンをベースクラスのメタデータにバインドします
Base.metadata.bind = engine

# スレッドセーフティを確保するためのスコープ付きセッションファクトリを作成します
db_session = scoped_session(sessionmaker(bind=engine))

# サイトのルーティング
@app.route('/')
def index():
    return render_template("login.html")

@app.route('/login', methods=["POST", "GET"])
def login():
    return render_template("login.html")

@app.route('/search')
def search():
    return render_template("search.html")

@app.route('/result')
def result():
    # セッションストレージから学生データを取得します
    student_data = json.loads(session.get('searchResults', '[]'))

    # 学生データをコンテキスト変数としてテンプレートに渡します
    return render_template("result.html", students_data=student_data)

@app.route('/form')
def form():
    # 仮のクラスオプションデータ
    class_options = [
        {'value': '1', 'text': 'クラス1'},
        {'value': '2', 'text': 'クラス2'},
        {'value': '3', 'text': 'クラス3'}
    ]
    # class_optionsをテンプレートに渡す
    return render_template("form.html", classOptions=class_options)

#@app.route('/form')
#def form():
#    return render_template("form.html")

# 学生エンドポイントの作成
@app.route('/api/students', methods=['POST'])
def create_student():
    data = request.json
    student = Student(**data)
    db_session.add(student)
    db_session.commit()
    return jsonify(student.id), 201

# 学生の取得エンドポイント
#@app.route('/api/students', methods=['GET'])
#def get_students():
#    query_parameters = request.args.to_dict()
#   order_by = query_parameters.pop('order_by', 'id')
#   ascending = query_parameters.pop('ascending', 'true').lower() == 'true'
#    base_query = db_session.query(Student)
#    or_conditions = []
#    for attr, value in query_parameters.items():
#        column = getattr(Student, attr)
#        or_conditions.append(column.ilike(f'%{value}%'))
#    filter_condition = or_(*or_conditions)
#    students = base_query.filter(filter_condition)
#    order_expr = getattr(Student, order_by)
#    if not ascending:
#        order_expr = order_expr.desc()
#    students = students.order_by(order_expr).all()

@app.route('/api/students', methods=['GET'])
def get_students():
    query_parameters = request.args.to_dict()  # クエリパラメータを辞書として取得
    order_by = query_parameters.pop('order_by', 'id')  # ソート基準のパラメータ
    ascending = query_parameters.pop('ascending', 'true').lower() == 'true'  # 昇順か降順か

    if 'all' in query_parameters:  # 'all'パラメータが含まれる場合
        students = db_session.query(Student).all()  # 全ての学生を取得
    else:
        base_query = db_session.query(Student)  # 学生テーブルからクエリを開始
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
    results = [{
        'id': student.id,
        'name': f'{student.first_name} {student.last_name}',
        'class_id': student.class_id
    } for student in students]
    return jsonify(results)


# 学生の更新エンドポイント
@app.route('/api/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.json
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

if __name__ == '__main__':
    app.run(debug=True)
