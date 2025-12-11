from flask import Flask, render_template
from sqlalchemy import create_engine
from models import Tasks, Topics
from sqlalchemy.orm import Session
from db_setup import db, migrate

def main():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:fk_kbkEz33@localhost/math"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/problems/')
    def problems_list():
        tasks = Tasks.query.all()
        return render_template('problems.html', tasks=tasks)

    @app.route('/problems/topic/<topic_id>')
    def problems_list_for_topics(topic_id):
        tasks = Tasks.query.filter(Tasks.topic_id == topic_id).all()
        return render_template('problems.html', tasks=tasks)
    
    @app.route('/problems/task/<int:task_id>')
    def show_task(task_id):
        task = Tasks.query.get(task_id)
        return render_template('task.html', task=task)
    
    return app

if __name__ == '__main__':
    app = main()
    app.run(debug=True)