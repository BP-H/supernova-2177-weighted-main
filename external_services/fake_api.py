_DB = {"profiles": {}}

def get_profile(username: str):
    return _DB["profiles"].get(username, {"username": username, "avatar_url": "", "bio": "", "location": "", "website": ""})

def save_profile(data: dict):
    if "username" not in data:
        return False
    _DB["profiles"][data["username"]] = data
    return True
