import json
from functools import wraps

from django.http import HttpResponse, JsonResponse

from .exceptions import APIError, UnprocessableEntity


def respond(content=None, status=200, response_class=HttpResponse):
    if content is None:
        content = ''
    return response_class(content, status=status)


def respond_json(content, status=200):
    assert isinstance(content, dict)
    return respond(content, status, JsonResponse)


def missed_key(data, keys):
    for key in keys:
        if key not in data:
            return key


def check_keys(data, keys):
    missed = missed_key(data, keys)
    if missed:
        raise UnprocessableEntity('Required key {} is missed'.format(missed))

    return True


def pick_request_data(*keys):

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            raw = request.body.decode(encoding='utf-8')
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                raise UnprocessableEntity
            check_keys(payload, keys)
            kwargs.update({k: payload.get(k) for k in keys})
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


def handle_api_errors(view_func):

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except APIError as e:
            return respond_json({'error_code': e.code, 'error_msg': e.msg})

    return wrapper
