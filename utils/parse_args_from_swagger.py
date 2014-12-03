"""
    This decorator allow us to make checks on API parameters, based on the `parameters` dict given to Swagger

Reqparse checks the presence / type of the arguments

Decorated methods will receive a dict called `args` as parameter
"""

from flask.ext.restful import reqparse
from functools import wraps


def parse_args_from_swagger(parameters):

    # Convert dataType string from swagger to a real Python type
    python_types = {
        'string': str,
        'int': int,
        'boolean': str,
    }

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            parser = reqparse.RequestParser()
            for parameter in parameters:
                if parameter['paramType'] == 'path':
                    # Path parameter are mandatory
                    pass
                else:
                    parser.add_argument(
                        parameter['name'],
                        required=parameter['required'],
                        type=python_types[parameter['dataType']],
                        default=parameter['defaultValue'] if 'defaultValue' in parameter else None
                    )
            arguments = parser.parse_args()
            kwargs['args'] = arguments
            return f(*args, **kwargs)
        return decorated_function
    return decorator
