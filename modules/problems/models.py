from db_setup import db


class Topics(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    translations = db.relationship("TopicTranslation",
                                    backref="topic",
                                    cascade="all, delete-orphan",
                                    passive_deletes=True)

    def __str__(self):
        return self.name
    

class TopicTranslation(db.Model):
    __tablename__ = 'topic_translation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id', ondelete='CASCADE'), nullable=False)
    lang = db.Column(db.String(2), nullable=False)
    title = db.Column(db.String(100))
    __table_args__ = (db.UniqueConstraint('topic_id', 'lang'), )
    

class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), unique=True)
    difficulty = db.Column(db.Integer)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    created_at = db.Column(db.DateTime)
    answer_type = db.Column(db.String(20))
    answer = db.Column(db.String(50))
    topic = db.relationship(Topics)
    translations = db.relationship("TaskTranslation", 
                                   backref="task",
                                   cascade="all, delete-orphan",
                                   passive_deletes=True)
    solved_by = db.relationship('SolvedTasks',
                                backref='task',
                                lazy='dynamic',
                                cascade='all, delete-orphan')


class TaskTranslation(db.Model):
    __tablename__ = 'task_translation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
    lang = db.Column(db.String(2), nullable=False)
    title = db.Column(db.String(255))
    description = db.Column(db.String(1000))
    __table_args__ = (db.UniqueConstraint('task_id', 'lang'), )
    