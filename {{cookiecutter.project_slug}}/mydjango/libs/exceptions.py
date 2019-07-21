import http

import requests

_HTTP_CODE_TO_EXCEPTION = {}


def _register(cls):
    _HTTP_CODE_TO_EXCEPTION[cls.code] = cls
    return cls


class APIError(Exception):

    def __init__(self, msg, orig_error=None):
        super().__init__(msg)
        self.msg = msg
        self.orig_error = orig_error


class ClientError(APIError):

    ''' Base exception for 4xx responses '''
    pass


@_register
class BadRequest(ClientError):

    ''' 400 bad request exception '''
    code = http.HTTPStatus.BAD_REQUEST


@_register
class Unauthorized(ClientError):

    ''' 401 unauthorized exception '''
    code = http.HTTPStatus.UNAUTHORIZED


@_register
class Forbidden(ClientError):

    ''' 403 forbidden exception '''
    code = http.HTTPStatus.FORBIDDEN


@_register
class NotFound(ClientError):

    ''' 404 not found exception '''
    code = http.HTTPStatus.NOT_FOUND


@_register
class Conflict(ClientError):

    ''' 409 conflict exception '''
    code = http.HTTPStatus.CONFLICT


@_register
class UnprocessableEntity(ClientError):

    ''' 422 unprocessable entity '''
    code = http.HTTPStatus.UNPROCESSABLE_ENTITY


class ServerError(APIError):

    ''' Base exception for 5xx responses '''
    pass


@_register
class InternalServerError(ServerError):

    ''' 500 internal server error '''
    code = http.HTTPStatus.INTERNAL_SERVER_ERROR


@_register
class BadGateway(ServerError):

    ''' 502 bad gateway exception '''
    code = http.HTTPStatus.BAD_GATEWAY


@_register
class GatewayTimeout(ServerError):

    ''' 504 gateway timeout exception '''
    code = http.HTTPStatus.GATEWAY_TIMEOUT


def get_exception_from_response(response: requests.Response):
    try:
        payload = response.json()
    except ValueError:
        payload = response.text

    msg = '{method} {url}\nstatus: {status} {reason}\ndetail: {detail}'.format(
        method=response.request.method,
        url=response.request.url,
        status=response.status_code,
        reason=response.reason,
        detail=payload
    )
    _exception_class = _HTTP_CODE_TO_EXCEPTION.get(
        response.status_code, APIError
    )

    exception = _exception_class(msg)
    if not getattr(exception, 'code', None):
        setattr(exception, 'code', response.status_code)
    return exception
