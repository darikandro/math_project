from db_setup import db


class Topics(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    translations = db.relationship("TopicTranslation", lazy="dynamic")

    def __str__(self):
        return self.name
    

class TopicTranslation(db.Model):
    __tablename__ = 'topic_translation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)
    lang = db.Column(db.String(2), nullable=False)
    title = db.Column(db.String(100))
    __table_args__ = (db.UniqueConstraint('topic_id', 'lang'), )
    

class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200))
    difficulty = db.Column(db.Integer)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    created_at = db.Column(db.DateTime)
    answer_type = db.Column(db.String(20))
    answer = db.Column(db.String(50))
    topic = db.relationship(Topics)
    translations = db.relationship("TaskTranslation", lazy="dynamic")


class TaskTranslation(db.Model):
    __tablename__ = 'task_translation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    lang = db.Column(db.String(2), nullable=False)
    title = db.Column(db.String(255))
    description = db.Column(db.String(1000))
    __table_args__ = (db.UniqueConstraint('task_id', 'lang'), )
    