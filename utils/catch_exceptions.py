"""
    Catch user-defined exceptions instead of raising a HTTP 500 error

    This could be accomplished by Flask itself, but is not supported when using blueprints (argh)
    (or at least I haven't found how)

"""
from functools import wraps
from flask import jsonify


def catch_exceptions(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # We try to execute this function
        try:
            return_value = f(*args, **kwargs)

        except Exception as e:

            # We add the exception name
            response = {
                'message': e.type if hasattr(e, 'type') else 'Server Error',
                'exception_name': e.__class__.__name__,
            }

            # We may have a message with this exception
            if hasattr(e, 'message'):
                response['exception_message'] = e.message

            # We may have a user-defined status code
            response_code = e.return_status_code if hasattr(e, 'return_status_code') else 500

            # We return the custom response message, with a 500 error code
            response = jsonify(response)
            response.status_code = response_code
            return response
        else:
            # If nothing went wrong, we pipe the response
            return return_value
    return decorated_function
