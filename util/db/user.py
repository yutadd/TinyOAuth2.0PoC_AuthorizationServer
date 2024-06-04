import datetime
import sqlite3
import bcrypt
import os
import secrets
from util.model.user import User

def getUserBySessionId(session_id) -> User:
    # SQLiteデータベースに接続
    conn = sqlite3.connect('./db/users.db')
    cursor = conn.cursor()
    # ユーザー名を使ってユーザーを検索
    print("searching user by session_id: ", session_id)
    cursor.execute("SELECT * FROM users WHERE session_id = ?", (session_id,))
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

def check_loggedin_by_sessionid(sessionid: str) -> bool:
    # SQLiteデータベースに接続
    conn = sqlite3.connect('./db/users.db')
    cursor = conn.cursor()
    # セッションIDを使ってユーザーを検索
    print("searching user by sessionid: ", sessionid)
    cursor.execute("SELECT * FROM users WHERE session_id = ?", (sessionid,))
    user = cursor.fetchone()
    # データベース接続を閉じる
    conn.close()
    # ユーザーが見つかった場合はTrueを返す
    return user is not None
def do_login(username: str, password: str) -> str:
    # SQLiteデータベースに接続
    conn = sqlite3.connect('./db/users.db')
    cursor = conn.cursor()
    
    # ユーザー名を使ってユーザーを検索
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    print(user,username,password)
    if user and bcrypt.checkpw(password.encode('utf-8'), user[6]):
        print("login success")
        # ログイン成功、セッションIDを生成
        session_id = secrets.token_hex(16)
        cursor.execute("UPDATE users SET session_id = ? WHERE username = ?", (session_id, username))
        conn.commit()
        conn.close()
        return session_id
    else:
        # ログイン失敗
        print("login failed")
        conn.close()
        return None

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
            password TEXT NOT NULL,
            session_id TEXT
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
