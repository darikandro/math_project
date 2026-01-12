from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from modules.problems.models import Tasks, Topics, TaskTranslation, TopicTranslation
from utils.tasks_utils import difficulty_key
from utils.translation_utils import get_current_lang, get_translation_db
from utils.access_utils import login_required


problems_bp = Blueprint('problems', __name__)


@problems_bp.route('/problems/')
def problems_list():
    lang = get_current_lang()

    sort = request.args.get("sort", "id")
    order = request.args.get("order", "asc")
    topic_filter = request.args.get("topic")

    tasks = Tasks.query.all()

    result = []
    for task in tasks:
        task_tr = get_translation_db(task, lang)
        topic_tr = get_translation_db(task.topic, lang)
        result.append({
            "id": task.id,
            "name": task.title,
            "title": task_tr.title if task_tr else "-",
            "difficulty": task.difficulty,
            "difficulty_key": difficulty_key(task.difficulty),
            "topic": topic_tr.title,
            "topic_name": task.topic.name,
            "created_at": task.created_at 
            })
        
    topics = []
    for topic in Topics.query.all():
        tr = get_translation_db(topic, lang)
        topics.append({
            "name": topic.name,
            "title": tr.title if tr else "-"
        })
        
    
    if topic_filter:
        result = [task for task in result if task["topic_name"] == topic_filter]    
        
    sort_map = {
        "id": lambda x: x["id"],
        "difficulty": lambda x: x["difficulty"],
        "topic": lambda x: x["topic"],
        "created_at": lambda x: x["created_at"]
    }

    if sort in sort_map:
        result.sort(key=sort_map[sort], reverse=(order == "desc"))

    return render_template('problems/list.html', tasks=result, topics=topics, current_sort=sort, current_order=order, current_topic=topic_filter)


#@problems_bp.route('/problems/topic/<topic_id>')
#def problems_list_for_topics(topic_id):
#    tasks = Tasks.query.filter(Tasks.topic_id == topic_id).all()
#    return render_template('problems.html', tasks=tasks)


@problems_bp.route('/problems/<title>')
def show_task(title):
    lang = get_current_lang()
    task = Tasks.query.filter_by(title=title).first_or_404()
    task_tr = get_translation_db(task, lang)
    return render_template('problems/task.html', task=task, task_tr=task_tr)


@problems_bp.route('/problems/<title>/give-answer', methods=['POST'])
@login_required
def give_answer(title):
    given_answer = request.form.get('answer')
    task = Tasks.query.filter_by(title=title).first()
    correct_answer = task.answer

    if given_answer == correct_answer:
        flash(("flash_message", "correct"), "success")
    else:
        flash(("flash_message", "wrong") ,"error")

    return redirect(url_for('problems.show_task', title=title))
