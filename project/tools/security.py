import base64
import hashlib

import calendar
import datetime
from os import abort

import jwt

from flask import current_app

from project.services import UsersService


def __generate_password_digest(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )


def generate_password_hash(password: str) -> str:
    return base64.b64encode(__generate_password_digest(password)).decode('utf-8')


def compare_passwords_hash(password_hash, other_password) -> bool:
    """
    Метод возвращает сравнение бинарных последовательностей чисел(из базы данных 'password_hash'
     и сгенерированный 'other_password'), возвращает True or False
     """
    return password_hash == generate_password_hash(other_password)


class AuthsService:
    def __init__(self, user_service: UsersService):
        self.user_service = user_service

    def generate_tokens(self, email, password, is_refresh=False):
        """
        Метод который генерирует access_token и refresh_token, получая email и пароль пользователя
        с проверкой is_refresh (создание новых токенов, а не перегенерация refresh_token)
        """

        user = self.user_service.get_by_email(email)

        if user is None:
            raise abort(404)

        if not is_refresh:
            if not compare_passwords_hash(user.password) == password:
                abort(400)

        data = {
            "email": user.email,
            "password": user.password
        }

        # 15 min for access_token
        min15 = datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config['TOKEN_EXPIRE_MINUTES'])
        data["exp"] = calendar.timegm(min15.timetuple())
        access_token = jwt.encode(data, key=current_app.config['SECRET_KEY'], algorithm=current_app.config['ALGORITHM'])

        # 130 days for refresh_token
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=current_app.config['TOKEN_EXPIRE_DAYS'])
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, key=current_app.config['SECRET_KEY'],
                                   algorithm=current_app.config['ALGORITHM'])

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
