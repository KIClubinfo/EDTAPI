__author__ = 'mickael'
from flask.ext.restful import Resource
from flask_restful_swagger import swagger
from .model import Course
from utils import parse_args_from_swagger, catch_exceptions


class CourseAPI(Resource):
    """ Courses """

    parameters = [
        {
            "name": "date",
            "description": "The course date (DD/MM/YYYY)",
            "required": False,
            "allowMultiple": False,
            "dataType": "string",
            "paramType": "query"
        },
        {
            "name": "department",
            "description": "The department (IMI, GCC...)",
            "required": False,
            "allowMultiple": False,
            "dataType": "string",
            "paramType": "query"
        },
        {
            "name": "place",
            "description": "The place of the course (number of the room...)",
            "required": False,
            "allowMultiple": False,
            "dataType": "string",
            "paramType": "query"
        },
        {
            "name": "comment",
            "description": "The course comment (may contain the number of the group)",
            "required": False,
            "allowMultiple": False,
            "dataType": "string",
            "paramType": "query"
        },
    ]

    @swagger.operation(
        nickname='course',
        parameters=parameters,
        responseMessages=[
            {
                "code": 200,
                "message": "If there were matching results, here they are"
            },
            {
                "code": 400,
                "message": "Invalid request"
            }
        ]
    )
    @catch_exceptions
    @parse_args_from_swagger(parameters)
    def get(self, args):
        """ Return the courses matching your result """

        # Parameters
        date = args['date']
        department = args['department']
        place = args['place']
        comment = args['comment']

        # Base query
        courses = Course.query

        # Apply filters
        if date:
            courses = courses.filter_by(date=date)
        if place:
            courses = courses.filter_by(place=place)
        if department:
            courses = courses.filter_by(department=department)
        if comment:
            # Can be useful to select a group in a course
            courses = courses.filter_by(department=comment)

        # Do the query
        courses = courses.limit(1000).all()

        # Format it
        course_list = [course.__toJSON__() for course in courses]

        return course_list, 200
