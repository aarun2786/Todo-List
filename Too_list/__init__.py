from flask import  Flask
from flask_login import LoginManager
from Mongodb import *
from main import main as main_blueprint
from auth import auth as auth_blueprint
from todo import todo as todo_blueprint
from bson import ObjectId

def create_app():
    app = Flask(__name__)
    app.secret_key = 'akr'
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(todo_blueprint)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        try:
            usr = collection.find_one({"_id":ObjectId(user_id)})
            return User(str(usr['_id']))
        except:
            return None

    return app

if __name__=="__main__":
    create_app().run(debug=True)