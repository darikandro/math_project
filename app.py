import os

from flask import Flask, g, render_template, request, redirect, session
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from db_setup import db, migrate
from modules.auth.controllers import auth_bp
from modules.auth.models import User
from modules.lang.controllers import lang_bp, inject_translations
from modules.problems.controllers import problems_bp
from modules.main.controllers import main_bp
from modules.admin.controllers import admin_bp
from utils.greetings import say_hello


load_dotenv()

def main():
    app = Flask(__name__)
    app.secret_key = os.environ.get('FLASK_SECRET_KEY') #ключ для сессии фласка
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp) 
    app.register_blueprint(lang_bp) 
    app.register_blueprint(problems_bp) 
    app.register_blueprint(main_bp) 
    app.register_blueprint(admin_bp) 


    app.context_processor(inject_translations)

    @app.before_request  # срабатывает перед каждым запросом
    def load_user():
        user_id = session.get('user_id')
        g.user = User.query.get(user_id) if user_id else None  # g - сохранение в глобальную переменную проекта


    @app.context_processor
    def inject_greeting():
        return {"random_greeting": say_hello()}
    
    return app


if __name__ == '__main__':
    app = main()
    app.run(debug=True)
    