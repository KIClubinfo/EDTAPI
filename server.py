__author__ = 'mickael'
from flask import Flask
from flask import render_template
from flask.ext.restful import Api
from flask_restful_swagger import swagger
from utils import catch_exceptions
import config

# Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URL

from lib.model import db
db.init_app(app)
db.app = app

api = swagger.docs(
    Api(app),
    apiVersion='0.1',
    basePath='http://localhost:5000',
    resourcePath='/',
    produces=["application/json", "text/html"],
    api_spec_url='/doc/courses',
    description='List of courses from emploidutemps.enpc.fr'
)


# The pseudo-REST API
from lib.api import CourseAPI
api.add_resource(CourseAPI, '/courses')


# Get my next course !
@app.route('/my-next-course')
@catch_exceptions
def get_courses():
    raise Exception("Not implemented yet !")


# Home page
@app.route('/')
@catch_exceptions
def homepage():
    return render_template('index.html')


if __name__ == '__main__':
    db.create_all() # Autocreate the DB if it does not exist yet
    app.run(debug=True)
