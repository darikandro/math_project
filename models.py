from db_setup import db

class Topics(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))

    def __str__(self):
        return self.name

class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(1000))
    difficulty_label = db.Column(db.String(20))
    difficulty_score = db.Column(db.Integer)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    created_at = db.Column(db.DateTime)
    answer_type = db.Column(db.String(20))
    answer = db.Column(db.String(50))

    topic = db.relationship(Topics)