from flask import Blueprint, g, render_template, redirect, request, url_for, flash
from datetime import datetime, timezone

from db_setup import db
from modules.auth.models import User
from modules.problems.models import Tasks, Topics, TaskTranslation, TopicTranslation
from utils.translation_utils import get_current_lang, get_translation_db
from utils.tasks_utils import auto_slug
from utils.access_utils import admin_required


admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/tasks/add_task', methods=['GET', 'POST'])
@admin_required
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
        slug = auto_slug(title_ru)
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

        return redirect(url_for('admin.add_task'))
    
    return render_template('admin/add_task.html', topics=topics_tr)


@admin_bp.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_task(task_id):
    task = Tasks.query.get_or_404(task_id)
    task_ru = get_translation_db(task, 'ru')
    task_by = get_translation_db(task, 'by')
    lang = get_current_lang()

    topics_tr = []
    for topic in Topics.query.all():
        tr = get_translation_db(topic, lang)
        topics_tr.append({
            "id": topic.id,
            "title": tr.title if tr else "-"
        })

    task_tr_ru = {'title': task_ru.title, 'description': task_ru.description}
    task_tr_by = {'title': task_by.title, 'description': task_by.description}


    if request.method == 'POST':
        difficulty = request.form['difficulty']
        topic_id = request.form['topic_id']
        answer = request.form['answer']
        new_slug = request.form['slug'].strip()

        title_ru = request.form['title_ru']
        description_ru = request.form['content_ru']

        title_by = request.form['title_by']
        description_by = request.form['content_by']

        existing = Tasks.query.filter(Tasks.title == new_slug, Tasks.id != task.id).first()

        if existing:
            flash(("flash_message", "slug_exists"), "error")

            task.title = new_slug
            task.difficulty = int(difficulty)
            task.topic_id = int(topic_id)
            task.answer = answer

            task_ru.title = title_ru
            task_ru.description = description_ru

            task_by.title = title_by
            task_by.description = description_by

            return render_template('admin/edit_task.html', task=task, topics=topics_tr, task_ru=task_ru, task_by=task_by)
        
        task.title = new_slug
        task.difficulty = int(difficulty)
        task.topic_id = int(topic_id)
        task.answer = answer

        task_ru.title = title_ru
        task_ru.description = description_ru

        task_by.title = title_by
        task_by.description = description_by

        db.session.commit()

        flash(("flash_message", "task_updated"), "success")
        return redirect(url_for('problems.problems_list', edit='admin'))

    return render_template('admin/edit_task.html', task=task, topics=topics_tr, task_ru=task_tr_ru, task_by=task_tr_by)


@admin_bp.route('/tasks/<int:task_id>/delete')
@admin_required
def delete_task(task_id):
    task = Tasks.query.get_or_404(task_id)

    db.session.delete(task)
    db.session.commit()

    flash(("flash_message", "task_deleted"), "success")
    return redirect(url_for('problems.problems_list', edit='admin'))


@admin_bp.route('/topics')
@admin_required
def topics_list():
    topics = Topics.query.all()

    topics_list = []
    for topic in topics:
        topic_ru = get_translation_db(topic, 'ru')
        topic_by = get_translation_db(topic, 'by')

        topics_list.append({
            "id": topic.id,
            "slug": topic.name,
            "ru": topic_ru.title,
            "by": topic_by.title
        })

    return render_template('admin/topics_list.html', topics=topics_list)


@admin_bp.route('/topics/<int:topic_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_topic(topic_id):
    topic = Topics.query.get_or_404(topic_id)
    topic_ru = get_translation_db(topic, 'ru')
    topic_by = get_translation_db(topic, 'by')

    title_ru = topic_ru.title
    title_by = topic_by.title

    if request.method == 'POST':

        new_slug = request.form['slug'].strip()
        new_ru = request.form['title_ru']
        new_by = request.form['title_by']

        exixts = Topics.query.filter(Topics.name == new_slug, Topics.id != topic.id).first()

        if exixts:
            flash(("flash_message", "slug_exists"), "error")

            topic.name = new_slug
            title_ru = new_ru
            title_by = new_by

            return render_template('admin/edit_topic.html', topic=topic, title_ru=title_ru, title_by=title_by)
        
        topic.name = new_slug
        topic_ru.title = new_ru
        topic_by.title = new_by

        db.session.commit()

        flash(("flash_message", "topic_updated"), "success")
        return redirect(url_for('admin.topics_list'))

    return render_template('admin/edit_topic.html', topic=topic, title_ru=title_ru, title_by=title_by)


@admin_bp.route('/topics/<int:topic_id>/delete')
@admin_required
def delete_topic(topic_id):
    topic = Topics.query.get_or_404(topic_id)

    db.session.delete(topic)
    db.session.commit()

    flash(("flash_message", "topic_deleted"), "success")
    return redirect(url_for('admin.topics_list'))


@admin_bp.route('/topics/add', methods=['GET', 'POST'])
@admin_required
def add_topic():
    if request.method == 'POST':
        title_ru = request.form.get('title_ru')
        title_by = request.form.get('title_by')

        if not all([title_ru, title_by]):
            flash(('flash_message', 'add_error'), 'error')
            return render_template('admin/add_topic.html')
    
        topic = Topics(name = auto_slug(title_ru))

        db.session.add(topic)
        db.session.flush()

        ru_translation = TopicTranslation(topic_id = topic.id,
                                        lang = 'ru',
                                        title = title_ru)
        
        by_translation = TopicTranslation(topic_id = topic.id,
                                        lang = 'by',
                                        title = title_by)

        db.session.add_all([ru_translation, by_translation])
        db.session.commit()

        flash(('flash_message', 'topic_added'), 'success')

        return redirect(url_for('admin.topics_list'))
    
    return render_template('admin/add_topic.html')


@admin_bp.route('/users')
@admin_required
def users():
    users = User.query.order_by(User.id).all()
    return render_template('admin/users.html', users=users)


@admin_bp.route('/users/<int:user_id>/change_status')
@admin_required
def change_user_status(user_id):
    user = User.query.get_or_404(user_id)

    if user.id == g.user.id:
        flash (("admin_users", "cannot_change_status"), "error")
        return redirect(url_for('admin.users'))

    if user.status == 'admin':
        user.status = 'user'
    else:
        user.status = 'admin'
    db.session.commit()
    flash(("admin_users", "status_updated"), "success")

    return redirect(url_for('admin.users'))


@admin_bp.route('/users/<int:user_id>/delete')
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    if user.status == 'admin':
        flash(("admin_users", "cannot_delete"), "error")
        return redirect(url_for('admin.users'))

    db.session.delete(user)
    db.session.commit()
    flash(("admin_users", "user_deleted"), "success")

    return redirect(url_for('admin.users'))
