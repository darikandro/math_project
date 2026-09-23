from flask import Blueprint, g, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from modules.auth.models import User, SolvedTasks
from modules.problems.models import Tasks
from utils.translation_utils import get_current_lang, translate, get_translation_db
from db_setup import db
from utils.access_utils import login_required


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            return translate("user_exists")
        user = User(
            username = username,
            password_hash = generate_password_hash(password),
            status = "user"
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')  #если метод get - возвращаем форму регистрации


@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password_hash, password):
            return translate("wrong")
        
        session["user_id"] = user.id
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/login.html') 


@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.login'))


@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html')


@auth_bp.route('/profile/stats')
@login_required
def stats():
    lang = get_current_lang()

    solved_tasks = (SolvedTasks.query.filter_by(user_id=g.user.id).join(Tasks).all())

    solved = []
    for s in solved_tasks:
        task = s.task
        topic = task.topic

        task_tr = get_translation_db(task, lang)
        topic_tr = get_translation_db(topic, lang)
        
        solved.append({"id": task.id,
        "title": task_tr.title if task_tr.title else task.title,
        "topic": topic_tr.title if topic_tr.title else topic.name,
        "difficulty": task.difficulty,
        "solved_at": s.solved_at})
    

    return render_template('auth/stats.html', solved=solved, total=len(solved))
