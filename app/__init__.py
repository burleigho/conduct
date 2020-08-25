from flask import Flask, jsonify
from flask_restx import Api
from marshmallow import ValidationError
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from resources.user import UserRegister, UserLogin, UserLogout, User, TokenRefresh
from resources.confirmation import Confirmation, ConfirmationByUser

from db import db
from ma import ma


app = Flask(__name__)
load_dotenv(".env", verbose=True)
app.config.from_object("default_config")
app.config.from_envvar(
    "APPLICATION_SETTINGS"
)
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


jwt = JWTManager(app)

api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")
api.add_resource(Confirmation, "/user_confirm/<string:confirmation_id>")
api.add_resource(ConfirmationByUser, "/confirmation/user/<int:user_id>")

if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)
