registered = [
    {
        "redirect_uri": "http://localhost/authorize",
        "client_id": 1
    }
]
def getClientById(client_id):
    for client in registered:
        if client["client_id"] == client_id:
            return client
    return None