
import datetime


class User:
    id: str #0
    authorization_code: str | None #1
    authorization_code_expires_at: datetime.datetime | None #2
    access_token: str | None #3
    access_token_expires_at: datetime.datetime | None #4
    refresh_token: str | None #5
    refresh_token_expires_at: datetime.datetime | None #6
    username: str #7
    password: bytes #8
    session_id: str | None #9
    session_expires_at: datetime.datetime | None #10

    def __init__(self, id: str, authorization_code: str, authorization_code_expires_at: datetime.datetime, access_token: str, access_token_expires_at: datetime.datetime, refresh_token: str, refresh_token_expires_at: datetime.datetime, username: str, password: bytes, session_id: str, session_expires_at: datetime.datetime):
        self.id = id
        self.authorization_code = authorization_code
        self.authorization_code_expires_at = authorization_code_expires_at
        self.access_token = access_token
        self.access_token_expires_at = access_token_expires_at
        self.refresh_token = refresh_token
        self.refresh_token_expires_at = refresh_token_expires_at
        self.username = username
        self.password = password
        self.session_id = session_id
        self.session_expires_at = session_expires_at
