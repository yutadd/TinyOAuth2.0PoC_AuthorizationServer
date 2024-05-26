import sqlite3
import bcrypt
import os
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