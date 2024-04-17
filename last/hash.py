# 必要なライブラリのインポート
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

# SQLAlchemyのベースクラスを作成
Base = declarative_base()

# ユーザーモデルの定義
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

# データベース接続の設定。ここではSQLiteを使用している
engine = create_engine('sqlite:///db/school.db')
# 定義された全てのテーブルをデータベースに作成
Base.metadata.create_all(engine)

# セッションファクトリを作成し、データベース操作のためのセッションを開始
Session = sessionmaker(bind=engine)
session = Session()

# 新しいユーザーを追加する例
new_user = User(username='user')
new_user.set_password('pass')  # パスワードをハッシュ化して設定
session.add(new_user)  # 新しいユーザーをセッションに追加
session.commit()  # 変更をデータベースにコミット

# パスワード認証の例
user = session.query(User).filter_by(username='user1').first()  # ユーザー名でユーザーを検索
if user.check_password('mysecurepassword'):  # 提供されたパスワードが正しいか検証
    print("認証成功")
else:
    print("認証失敗")

