from fastapi.security import HTTPBasicCredentials

USERS = [
    {"id": 1, "username": "user1", "password": "password1"},
    {"id": 2, "username": "user2", "password": "password2"},
]


def authenticate_user(credentials: HTTPBasicCredentials):
    for user in USERS:
        if (
            user["username"] == credentials.username
            and user["password"] == credentials.password
        ):
            return user
    return None
