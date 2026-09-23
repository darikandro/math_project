from datetime import datetime, timezone

from db_setup import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20))
    solved_tasks = db.relationship('SolvedTasks',
                                    backref='user',
                                    lazy='dynamic',
                                    cascade='all, delete-orphan')


class SolvedTasks(db.Model):
    __tablename__ = 'solved_tasks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    solved_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    __tableargs__ = (db.UniqueConstraint('user_id', 'task_id', name='unique_user_task'),)
    