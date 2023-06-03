import uuid


def get_new_token():
    return str(uuid.uuid4()).replace("-", "")
