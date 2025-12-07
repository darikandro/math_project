from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Topics(Base):
    __tablename__ = 'topics'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))

    def __str__(self):
        return self.name

class Tasks(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200))
    description = Column(String(1000))
    difficulty_label = Column(String(20))
    difficulty_score = Column(Integer)
    topic_id = Column(Integer, ForeignKey('topics.id'))
    created_at = Column(DateTime)
    answer_type = Column(String(20))
    answer = Column(String(50))

    topic = relationship(Topics)

