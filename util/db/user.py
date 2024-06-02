import datetime
import sqlite3
import bcrypt
import os
import secrets
from util.model.user import User

def getUserByUsername(username) -> User:
    # SQLiteデータベースに接続
    conn = sqlite3.connect('./db/users.db')
    cursor = conn.cursor()
    # ユーザー名を使ってユーザーを検索
    print("searching user by username: ", username)
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    modeledUser = None
    if user[2] is None:
        modeledUser = User(user[0], user[1], None, user[3],
                           None, user[5], user[6])
    elif user[4] is None:
        modeledUser = User(user[0], user[1], datetime.datetime.strptime(user[2], '%Y-%m-%d %H:%M:%S'), user[3],
                           None, user[5], user[6])
    else:
        User(user[0], user[1], datetime.datetime.strptime(user[2], '%Y-%m-%d %H:%M:%S'), user[3],
                           datetime.datetime.strptime(user[4], '%Y-%m-%d %H:%M:%S'), user[5], user[6])
    return modeledUser

def getUserByCode(code: str) -> User:
    # SQLiteデータベースに接続
    conn = sqlite3.connect('./db/users.db')
    cursor = conn.cursor()
    # ユーザー名を使ってユーザーを検索
    print("searching user by code: ", code)
    cursor.execute("SELECT * FROM users WHERE authorization_code = ?", (code,))
    user = cursor.fetchone()
    modeledUser = User(user[0], user[1], datetime.datetime.strptime(user[2], '%Y-%m-%d %H:%M:%S'), user[3],
                       datetime.datetime.strptime(user[4], '%Y-%m-%d %H:%M:%S'), user[5], user[6])
    return modeledUser


def issue_Authorization_Code(username: str):
    code = secrets.token_hex(30)
    # SQLiteデータベースに接続
    conn = sqlite3.connect('./db/users.db')
    cursor = conn.cursor()
    # ユーザー名とパスワードを使ってユーザーを検索
    cursor.execute(
        "UPDATE users SET authorization_code = ?, authorization_code_issued_at = datetime('now') WHERE username = ?", (code, username))
    conn.commit()
    # データベース接続を閉じる
    conn.close()
    return code


def issue_Access_Token(username: str):
    code = secrets.token_hex(30)
    # SQLiteデータベースに接続
    conn = sqlite3.connect('./db/users.db')
    cursor = conn.cursor()
    # ユーザー名とパスワードを使ってユーザーを検索
    cursor.execute(
        "UPDATE users SET access_token = ?, access_token_issued_at = datetime('now') WHERE username = ?", (code, username))
    conn.commit()
    # データベース接続を閉じる
    conn.close()
    return code


def seed_user_data():
    db_path = './db/users.db'
    # ディレクトリが存在しない場合は作成
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    # SQLiteデータベースに接続
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # ユーザーテーブルが存在しない場合は作成
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            authorization_code TEXT,
            authorization_code_issued_at DATETIME,
            access_token TEXT,
            access_token_issued_at DATETIME,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('SELECT * FROM users WHERE username = ?', ('user01',))
    user = cursor.fetchone()
    if not user:
        # ユーザーデータをシード
        username = 'user01'
        password = 'P@ssw0rd'
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())

        cursor.execute(
            'INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        # 変更をコミット
        conn.commit()
    # データベース接続を閉じる
    conn.close()


# シード関数を呼び出す
seed_user_data()
