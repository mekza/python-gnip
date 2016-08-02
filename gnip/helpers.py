class GnipException(Exception):
    """ Base error. """
    code = None

    def __init__(self, message="", result=None):
        super(GnipException, self).__init__(message)
        self.result = result
        self.message = message


class BadRequest(GnipException):
    code = 400
    message = "Bad Request"


class AuthenticationError(GnipException):
    code = 401
    message = "Not Authorized"


class Forbidden(GnipException):
    code = 403
    message = "Forbidden"


class TooManyRequests(GnipException):
    code = 429


class ResourceNotFound(GnipException):
    code = 404
    message = "Not Found"


class MethodNotAllowed(GnipException):
    code = 405
    message = "Not Allowed"


class UnprocessableEntity(GnipException):
    code = 422
    message = "Unprocessable Entity"


class ServerError(GnipException):
    code = 500
    message = "Internal Server Error"


class BadGatewayError(GnipException):
    code = 502
    message = "Bad Gateway"


class ServiceUnavailableError(GnipException):
    code = 503
    message = "Service is unavailable"


class ConnectionTimeout(GnipException):
    code = 522
    message = "Connection timed out"


def get_error(response):
    try:
        json = response.json()
        if "message" in json:
            return json['message']
        if "error" in json:
            return json["error"]
    except ValueError:
        pass

    return ''


def raise_errors_on_failure(response):
    print(response.text)
    if response.status_code >= 400:
        msg = get_error(response)
        search_for_exception(response.status_code, msg)

    return response

# The code that follows is stolen from werkzeug:
# https://github.com/mitsuhiko/werkzeug/blob/d4e8b3f46c51e7374388791282e66323f64b3068/werkzeug/exceptions.py

_exceptions = {}
__all__ = ['GnipException',
           'raise_errors_on_failure']


def _find_exceptions():
    for name, obj in globals().items():
        try:
            is_http_exception = issubclass(obj, GnipException)
        except TypeError:
            is_http_exception = False
        if not is_http_exception or obj.code is None:
            continue
        __all__.append(obj.__name__)
        old_obj = _exceptions.get(obj.code, None)
        if old_obj is not None and issubclass(obj, old_obj):
            continue
        _exceptions[obj.code] = obj

_find_exceptions()
del _find_exceptions


def search_for_exception(code, msg):
        if code not in _exceptions:
            raise LookupError('no exception for %r' % code)
        raise _exceptions[code](msg)
