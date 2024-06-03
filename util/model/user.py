
import datetime


class User:
    id: str
    authorization_code: str | None
    authorization_code_issued_at: datetime.datetime | None
    access_token: str | None
    access_token_issued_at: datetime.datetime | None
    username: str
    password: str

    def __init__(self, id: str, authorization_code: str, authorization_code_issued_at: datetime, access_token: str, access_token_issued_at: datetime, username: str, password: str):
        self.id = id
        self.authorization_code = authorization_code
        self.authorization_code_issued_at = authorization_code_issued_at
        self.access_token = access_token
        self.access_token_issued_at = access_token_issued_at
        self.username = username
        self.password = password

