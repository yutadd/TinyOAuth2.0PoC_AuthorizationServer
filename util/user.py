import sqlite3
import bcrypt
import os
import secrets
def authenticate(username: str, password: str) -> bool:
    # SQLiteデータベースに接続
    conn = sqlite3.connect('./db/users.db')
    cursor = conn.cursor()
    print(username)
    # ユーザー名とパスワードを使ってユーザーを検索
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    
    # データベース接続を閉じる
    conn.close()
    
    # ユーザーが見つかった場合はTrueを返す
    # ユーザーが見つかり、パスワードが一致する場合はTrueを返す
    print(user)
    if user and bcrypt.checkpw(password.encode('utf-8'), user[0]):
        return True
    else:
        return False
def issue_Authorization_Code(username:str):
    code=secrets.token_hex(30)
    # SQLiteデータベースに接続
    conn = sqlite3.connect('./db/users.db')
    cursor = conn.cursor()
    # ユーザー名とパスワードを使ってユーザーを検索
    cursor.execute("SELECT password FROM users WHERE id = ?", (username,))
    user = cursor.fetchone()
    cursor.execute("UPDATE users SET authorization_code = ?, authorization_code_issued_at = datetime('now') WHERE username = ?", (code, username))
    conn.commit()
    # データベース接続を閉じる
    conn.close()
    return code
def issue_Access_Token(code:str):
    code=secrets.token_hex(30)
    # SQLiteデータベースに接続
    conn = sqlite3.connect('./db/users.db')
    cursor = conn.cursor()
    # ユーザー名とパスワードを使ってユーザーを検索
    cursor.execute("SELECT password FROM users WHERE authorization_code = ?", (code,))
    user = cursor.fetchone()
    userid=user.id
    cursor.execute("UPDATE users SET access_token = ?, access_token_issued_at = datetime('now') WHERE userid = ?", (code, userid))
    conn.commit()
    # データベース接続を閉じる
    conn.close()
    return code
import datetime

def is_authorization_code_valid(username: str,code:str) -> bool:
    # SQLiteデータベースに接続
    conn = sqlite3.connect('./db/users.db')
    cursor = conn.cursor()
    
    # ユーザー名を使ってユーザーを検索
    cursor.execute("SELECT * FROM users WHERE userid = ?", (username,))
    user = cursor.fetchone()
    
    # データベース接続を閉じる
    conn.close()
    print("checking code is valid ",code,"and",user[1])
    # Authorization Codeが発行されてから5分以内かどうかを確認
    if user and (datetime.datetime.now() - datetime.datetime.strptime(user[0], '%Y-%m-%d %H:%M:%S')).total_seconds() <= 300 and user[1]==code:
        return True
    else:
        return False

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
            access_token_issued_at,
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
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        
        # 変更をコミット
        conn.commit()
    
    # データベース接続を閉じる
    conn.close()

# シード関数を呼び出す
seed_user_data()