from flask import Flask, request, jsonify, session, render_template, request, url_for, redirect
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import scoped_session, sessionmaker
from databaseManager import Base, Student,User  # 事前に定義したStudentクラスをimport

app = Flask(__name__)
# SQLiteデータベース 'school.db' への接続を設定します。
engine = create_engine('sqlite:///db/school.db')
Base.metadata.bind = engine

# セッションファクトリを作成し、スレッドセーフなセッションを確保します。
db_session = scoped_session(sessionmaker(bind=engine))


# サイトのルーティング
@app.route('/')
def index():
    return render_template(
        "login.html"
    )
@app.route('/login', methods = ["POST", "GET"])
def login():
    # if request.method == "POST":
    #     session.permanent = True 
    #     user = request.form["nm"]
    #     session["user"] = user
    #     return redirect(url_for("search"))
    # else:
    #     if "user" in session:
    #         return redirect(url_for("search"))
        return render_template("login.html")
@app.route('/search')
def search():
    # if "user" in session:
    #     user = session["user"]
        return render_template("search.html")
    # else:
        # return redirect(url_for("login"))
@app.route('/result')
def result():
    # if "user" in session:
    #     user = session["user"]
        return render_template("result.html")
    # else:
        # return redirect(url_for("login"))
@app.route('/form')
def form():
    # if "user" in session:
    #     user = session["user"]
        return render_template("form.html")
    # else:
        # return redirect(url_for("login"))


# 生徒情報の作成を行うエンドポイント
@app.route('/api/students', methods=['POST'])
def create_student():
    data = request.json  # リクエストボディからJSONデータを取得
    student = Student(**data)  # Studentインスタンスを作成
    db_session.add(student)  # セッションに追加
    db_session.commit()  # データベースにコミット
    return jsonify(student.id), 201  # 作成した生徒のIDとHTTPステータスコード201を返す

# 生徒情報の取得を行うエンドポイント
@app.route('/api/students', methods=['GET'])
def get_students():
    # リクエストからクエリパラメータを辞書として取得
    query_parameters = request.args.to_dict()

    # クエリパラメータからオーダリング基準を抽出
    order_by = query_parameters.pop('order_by', 'id')  # 指定されていない場合はIDでデフォルトオーダリング
    ascending = query_parameters.pop('ascending', 'true').lower() == 'true'

    # すべての生徒を取得する基本クエリを初期化
    base_query = db_session.query(Student)

    # OR条件を格納するためのリストを初期化
    or_conditions = []

    # クエリパラメータごとに反復処理し、各属性に対するフィルタリング条件を動的に構築
    for attr, value in query_parameters.items():
        # 各属性に対するフィルタリング条件を動的に構築
        # 簡単のため、すべての属性を文字列型と仮定する
        column = getattr(Student, attr)
        or_conditions.append(column.ilike(f'%{value}%'))

    # OR条件を結合してフィルタリング条件を作成
    filter_condition = or_(*or_conditions)

    # ベースクエリにフィルタリング条件を適用
    students = base_query.filter(filter_condition)

    # クエリパラメータから取得したオーダリング基準に基づいて、オーダリング条件を動的に適用
    order_expr = getattr(Student, order_by)
    if not ascending:
        order_expr = order_expr.desc()

    # データベースからオプションのオーダリングを適用して生徒を取得
    students = students.order_by(order_expr).all()

    # 生徒データをJSON形式でフォーマットして返す
    return jsonify([{
        'id': student.id,
        'first_name': student.first_name,
        'last_name': student.last_name,
        'last_name_katakana': student.last_name_katakana,
        'first_name_katakana': student.first_name_katakana,
        'birthday': student.birthday.isoformat(),  
        'gender': student.gender,
        'email': student.email,
        'phone': student.phone,
        'mobile_phone': student.mobile_phone,
        'postal_code': student.postal_code,
        'address': student.address,
        'class_id': student.class_id,
        'status': student.status
    } for student in students])

# 生徒情報の更新を行うエンドポイント
@app.route('/api/students/<int:student_id>', methods=['PUT'])
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
@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student_int_id = int(student_id)
    student = db_session.query(Student).filter(Student.id == student_int_id).first()  # 削除対象の生徒を検索
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