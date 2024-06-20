from fastapi import HTTPException, status


class WrongCredentialsAPIException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = 'Неверное имя пользователя или пароль'
        self.headers = {"WWW-Authenticate": "Basic"}
