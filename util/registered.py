registered = [
    {
        "redirect_uri": "http://localhost/callback",
        "client_id": 1,
        "allowed_scopes":["read"]
    }
]
def getClientById(client_id):
    for client in registered:
        if client["client_id"] == int(client_id):
            return client
    return None