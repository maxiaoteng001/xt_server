from flask import Blueprint
from flask_restful import Api, Resource
from src.api.password import PasswordItem


api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)

api.add_resource(PasswordItem, '/random_string')