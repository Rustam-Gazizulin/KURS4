from flask_restx import Namespace, Resource
from flask import request

from project.container import user_service
from project.setup.api.models import user

api = Namespace('user')


@api.route('/')
class RegisterView(Resource):
    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def patch(self):
        data = request.json
        header = request.headers.environ.get('HTTP_AUTHORIZATION').replace('Bearer ','')

        return user_service.update_user(data=data, refresh_token=header)

    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def get(self):
        data = request.json
        header = request.headers.environ.get('HTTP_AUTHORIZATION').replace('Bearer ','')

        return user_service.get_by_user_token(refresh_token=header)

# @api.route('/password/')
# class LoginView(Resource):
#     @api.response(404, 'Not Found')
#     #@api.marshal_with(user, code=200, description='OK')
#     def put(self):
#         data = request.json
#         if data.get('email') and data.get('password'):
#             return user_service.check(data.get('email'), data.get('password')), 201
#         else:
#             return "email or password not found", 401
