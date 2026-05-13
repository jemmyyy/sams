from asgiref.local import Local

_thread_locals = Local()


def set_current_academy_id(academy_id):
    _thread_locals.academy_id = academy_id


def get_current_academy_id():
    return getattr(_thread_locals, "academy_id", None)


def clear_current_academy_id():
    if hasattr(_thread_locals, "academy_id"):
        del _thread_locals.academy_id
