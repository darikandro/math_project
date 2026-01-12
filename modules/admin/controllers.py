from flask import Blueprint, render_template, redirect, request, url_for, flash
from datetime import datetime, timezone

from db_setup import db
from modules.problems.models import Tasks, Topics, TaskTranslation, TopicTranslation
from utils.translation_utils import get_current_lang, get_translation_db


admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/tasks/add_task', methods=['GET', 'POST'])
def add_task():
    topics = Topics.query.order_by(Topics.name).all()
    lang = get_current_lang()

    topics_tr = []
    for topic in Topics.query.all():
        tr = get_translation_db(topic, lang)
        topics_tr.append({
            "id": topic.id,
            "title": tr.title if tr else "-"
        })

    if request.method == 'POST':
        title_ru = request.form.get('title_ru')
        content_ru = request.form.get('content_ru')
        title_by = request.form.get('title_by')
        content_by = request.form.get('content_by')
        slug = request.form.get('slug')
        answer = request.form.get('answer')
        topic_id = request.form.get('topic_id')
        difficulty = request.form.get('difficulty')

        if not all([title_ru, title_by, content_ru, content_by, answer, slug, topic_id, difficulty]):
            flash(('flash_message', 'add_error'), 'error')
            return render_template('admin/add_task.html', topics=topics_tr)
        
        task = Tasks(title = slug, 
                    difficulty = int(difficulty), 
                    topic_id = int(topic_id), 
                    created_at = datetime.now(timezone.utc), 
                    answer_type = 'number', 
                    answer = answer)
        
        db.session.add(task)
        db.session.flush()  # нужен, чтобы task.id появился до translations

        ru_translation = TaskTranslation(task_id = task.id,
                                        lang = 'ru',
                                        title = title_ru,
                                        description = content_ru)
        
        by_translation = TaskTranslation(task_id = task.id,
                                        lang = 'by',
                                        title = title_by,
                                        description = content_by)

        db.session.add_all([ru_translation, by_translation])
        db.session.commit()

        flash(('flash_message', 'task_added'), 'success')

        return redirect(url_for('admin.edit_problems'))
    
    return render_template('admin/add_task.html', topics=topics_tr)


@admin_bp.route('/tasks')
def edit_problems():
    return render_template('admin/problems.html')


@admin_bp.route('/users')
def users():
    return render_template('admin/users.html')
