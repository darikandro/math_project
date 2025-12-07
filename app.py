from flask import Flask, render_template
from sqlalchemy import create_engine
from models import Tasks, Topics
from sqlalchemy.orm import Session, sessionmaker

engine = create_engine("mysql+pymysql://root:fk_kbkEz33@localhost/math")
engine.connect()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/problems/')
def problems_list():

    session = Session(bind=engine)
    tasks = session.query(Tasks).all()

    return render_template('problems.html', tasks=tasks)

@app.route('/problems/topic/<topic_id>')
def problems_list_for_topics(topic_id):
    
    session = Session(bind=engine)
    tasks = session.query(Tasks).filter(Tasks.topic_id == topic_id).all()

    return render_template('problems.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)