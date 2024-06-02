from typing import List



class Client:
    client_id:int
    client_secret:str
    redirect_prefix:str
    allowed_scope:List[str]
    def __init__(self,client_id:str,client_secret:str,redirect_prefix:str,allowed_scope:List[str]) -> None:
        self.client_id=client_id
        self.client_secret=client_secret
        self.redirect_prefix=redirect_prefix
        self.allowed_scope=allowed_scope
