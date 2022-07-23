from flask_restx import fields, Model

from project.setup.api import api

genre: Model = api.model('Жанр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Комедия'),
})

director: Model = api.model('Режиссеры', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Быков'),
})


movie: Model = api.model('Фильмы', {
    'id': fields.Integer(required=True, example=1),
    'title': fields.String(required=True, max_length=100, example='Майор'),
    'description': fields.String(required=True, max_length=100, example='Бла, бла, бла'),
    'trailer': fields.String(required=True, max_length=100, example='www.youtube.com'),
    'year': fields.Integer(required=True, example=2010),
    'rating': fields.Float(required=True, example=7.9),
    'genre': fields.Nested(genre),
    'director': fields.Nested(director),
})

user: Model = api.model('Пользователm', {
    'id': fields.Integer(required=True, example=1),
    'email': fields.String(required=True, max_length=100, example='qwerty123@mail.ru'),
    'password': fields.String(required=True, max_length=100, example='12345'),
    'name': fields.String(required=True, max_length=100, example='Kolia'),
    'surname': fields.String(required=True, max_length=100, example='Kolov'),
    'favorite_genre': fields.Nested(genre),
})


