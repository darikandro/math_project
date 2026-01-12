from flask import Blueprint, redirect, request, session, url_for

from utils.translation_utils import get_translation, translate, get_current_lang


lang_bp = Blueprint('lang', __name__)


@lang_bp.context_processor   #добавляет t, current_lang во все html формы
def inject_translations():
    t, current_lang = get_translation()
    return dict(t=t, current_lang=current_lang)


@lang_bp.route('/set-language', methods=['POST'])  #установка текущего языка
def set_language():
    lang = request.form.get('lang')
    if lang in ('ru', 'by'):
        session['lang'] = lang
    return redirect(request.referrer or url_for('lang.index'))
