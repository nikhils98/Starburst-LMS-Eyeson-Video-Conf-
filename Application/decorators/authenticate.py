from functools import wraps
from flask import session, request, redirect, url_for


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('id'):
            return redirect('/')
        return f(*args, **kwargs)

    return decorated_function
