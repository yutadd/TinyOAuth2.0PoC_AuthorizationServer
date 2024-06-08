import datetime
import sqlite3
from typing import List
import bcrypt
import os
import secrets
from util.model.user import User

def issue_Authorization_Code(username: str):
    code = secrets.token_hex(30)
    users=SearchUserByAnyColumn('username',username)
    if len(users)>0:
        user=users[0]
        user.authorization_code=str(code)
        authorization_code_expires_at = datetime.datetime.now() + datetime.timedelta(hours=1)
        user.access_token_expires_at = authorization_code_expires_at
        updateUserByUserObject(user)
        return code
    else:
        raise Exception('ユーザーが見つかりません')

def check_loggedin_by_sessionid(sessionid: str) -> bool:
    users=SearchUserByAnyColumn("session_id",sessionid)
    if len(users)>0:
        user=users[0]
        return user.session_id is not None
    else:
        False

def is_token_valid(token: str) -> bool:
    users=SearchUserByAnyColumn("access_token",token)
    if len(users)>0:
        user=users[0]
        return user.access_token is not None
    else:
        return False
def is_code_valid(code: str) -> bool:
    users=SearchUserByAnyColumn("authorization_code",code)
    if len(users)>0:
        user=users[0]
        return user.authorization_code is not None
    else:
        return False
# user name is unique by definition
def do_login(username: str, password: str) -> str:
    users=SearchUserByAnyColumn('username',username)
    if len(users)>0:
        user=users[0]
        print(user,username,password)
        print(user.password)
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
            print("login success")
            # ログイン成功、セッションIDを生成
            session_id = secrets.token_hex(16)
            user.session_id=session_id
            user.session_expires_at=datetime.datetime.now()+datetime.timedelta(hours=1)
            updateUserByUserObject(user)
            return session_id
        else:
            # ログイン失敗
            print("login failed")
            return None
    else:
        return None
def issue_Access_Token(username: str)->str:
    code = secrets.token_hex(30)
    users=SearchUserByAnyColumn('username',username)
    if len(users)>0:
        user=users[0]
        user.access_token=str(code)
        access_token_expires_at = datetime.datetime.now() + datetime.timedelta(hours=1)
        user.access_token_expires_at = access_token_expires_at
        updateUserByUserObject(user)
        return code
    else:
        raise Exception("ユーザーが見つかりません")
def updateUserByUserObject(user:User):
    # SQLiteデータベースに接続
    try:
        conn = sqlite3.connect('./db/users.db')
        cursor = conn.cursor()
        print("updating users database:")
        print(user.session_id)
        # ユーザー情報を更新
        cursor.execute('''
            UPDATE users
            SET authorization_code = ?,
                authorization_code_expires_at = ?,
                access_token = ?,
                access_token_expires_at = ?,
                refresh_token = ?,
                refresh_token_expires_at = ?,
                username = ?,
                password = ?,
                session_id = ?,
                session_expires_at = ?
            WHERE id = ?
        ''', (
            user.authorization_code,
            user.authorization_code_expires_at,
            user.access_token,
            user.access_token_expires_at,
            user.refresh_token,
            user.refresh_token_expires_at,
            user.username,
            user.password,
            user.session_id,
            user.session_expires_at,
            user.id
        ))
        
        # 変更をコミット
        conn.commit()
        # データベース接続を閉じる
        print("commited to database")
        conn.close()
    except Exception as e:
        print(e)
def replaceExpiredValueToNone(user: User) -> User:
    current_time = datetime.datetime.now()
    if user.authorization_code_expires_at and user.authorization_code_expires_at < current_time:
        user.authorization_code = None
        user.authorization_code_expires_at = None
    if user.access_token_expires_at and user.access_token_expires_at < current_time:
        user.access_token = None
        user.access_token_expires_at = None
    if user.refresh_token_expires_at and user.refresh_token_expires_at < current_time:
        user.refresh_token = None
        user.refresh_token_expires_at = None
    if user.session_expires_at and user.session_expires_at < current_time:
        user.session_id = None
        user.session_expires_at = None
    return user

def SearchUserByAnyColumn(column,value)->List[User]:
    # TODO: セキュリティ診断を行う
    conn = sqlite3.connect('./db/users.db')
    cursor = conn.cursor()
    allowed_columns = [
        'id', 'authorization_code', 'authorization_code_expires_at', 
        'access_token', 'access_token_expires_at', 'refresh_token', 
        'refresh_token_expires_at', 'username', 'password', 
        'session_id', 'session_expires_at'
    ]
    print(column,value)
    if column in allowed_columns:
        cursor.execute(f'SELECT * from users where {column}= ?',(value,))
        users=cursor.fetchall()
        result=[]
        print(type(users))
        print(users)
        print(len(users))
        for index in range(len(users)):
            user = User(
                id=users[index][0],
                authorization_code=str(users[index][1]) if users[index][1] is not None else None,
                authorization_code_expires_at=datetime.datetime.strptime(users[index][2], '%Y-%m-%d %H:%M:%S.%f') if users[index][2] is not None else None,
                access_token=str(users[index][3]) if users[index][3] is not None else None,
                access_token_expires_at=datetime.datetime.strptime(users[index][4], '%Y-%m-%d %H:%M:%S.%f') if users[index][4] is not None else None,
                refresh_token=str(users[index][5]) if users[index][5] is not None else None,
                refresh_token_expires_at=datetime.datetime.strptime(users[index][6], '%Y-%m-%d %H:%M:%S.%f') if users[index][6] is not None else None,
                username=str(users[index][7]),
                password=users[index][8],
                session_id=str(users[index][9]) if users[index][9] is not None else None,
                session_expires_at=datetime.datetime.strptime(users[index][10], '%Y-%m-%d %H:%M:%S.%f') if users[index][10] is not None else None
            )
            user = replaceExpiredValueToNone(user)
            updateUserByUserObject(user)
            result.append(user)
        return result
    else:
        raise Exception("[dev]searching error this column name is not able to use.")
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
            authorization_code_expires_at DATETIME,
            access_token TEXT,
            access_token_expires_at DATETIME,
            refresh_token TEXT,
            refresh_token_expires_at DATETIME,
            username TEXT NOT NULL UNIQUE,
            password BLOB NOT NULL,
            session_id TEXT,
            session_expires_at DATETIME
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
