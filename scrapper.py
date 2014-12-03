__author__ = 'mickael'
import datetime
import requests
import re
import sqlalchemy
from bs4 import BeautifulSoup
from lib.model import Course


class EdtScraper(object):

    def __init__(self, base_url):
        self.base_url = base_url

    def run(self):
        response = requests.get(self.base_url)

        if not response or response.status_code != 200\
                or 'Une erreur est survenue, merci de nous contacter ' in response.text:
            raise Exception("Unable to fetch the page !")

        root_html = BeautifulSoup(response.text)
        courses = root_html.find(id='content').find('ul', recursive=False)

        course_list = []

        for course in courses:
            course_data = self.__process_course_tag(course)

            print("Found course : %s" % course_data)
            course_list.append(course_data)

        return course_list

    def __process_course_tag(self, course_tag):
        """ Parse a span tag """
        course = Course()

        course.link = course_tag.find('a')['href']

        # Detect course ID
        expr = re.search('index_mobile\.php\?id=(\d+)&code_departement=.*&mydate=([0-9/]+)', course.link)
        course.id = expr.group(1)
        course.date = datetime.datetime.strptime(expr.group(2), '%d/%m/%Y').date()

        for span_tag in course_tag.find_all('span'):

            assert(len(span_tag['class']) == 1)
            type = span_tag['class'][0]

            if type == 'image':
                # First field : time of beginning / end of the courses
                # <br><b>08:30<br>11:45</br>
                expr = re.search('<br><b>([0-9]{2}:[0-9]{2})<br>([0-9]{2}:[0-9]{2})</b', str(span_tag))
                time_format = '%H:%M'
                course.time_begin = datetime.datetime.strptime(expr.group(1), time_format).time()
                course.time_end = datetime.datetime.strptime(expr.group(2), time_format).time()
            elif type == 'comment':
                # Second field : department and place
                expr = re.search('(.*) : (.*)', span_tag.text)
                course.department = expr.group(1)
                course.place = expr.group(2)
            elif type == 'name':
                # Third field : name
                course.name = span_tag.text
            elif type == 'starcomment':
                # Fourth field : comment
                course.comment = span_tag.text
            elif type == 'arrow':
                # Nothing to do
                pass
            else:
                print("Unrecognized type : %s !" % type)

        return course


if __name__ == '__main__':
    # Lancement en ligne de commande
    scrapper = EdtScraper('http://emploidutemps.enpc.fr/index_mobile.php')
    course_list = scrapper.run()
    print("Found %d courses !" % len(course_list))

    # Registering them
    from sqlalchemy.orm import scoped_session, sessionmaker
    engine = sqlalchemy.create_engine("sqlite:///test.db")
    session = scoped_session(sessionmaker(bind=engine))

    for course in course_list:
        session.merge(course)

    session.commit()
