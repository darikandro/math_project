from functools import wraps
from flask import flash, g, redirect, url_for, abort


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if g.user is None:
            flash(("flash_message", "login_required"), "message")
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)
    return wrapped


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not g.user or g.user.status != 'admin':
            abort(403)
        return view(*args, **kwargs)
    return wrapped
