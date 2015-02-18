__author__ = 'mickael'
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

from sqlalchemy.sql.sqltypes import Integer, Text, Date, Time

db = SQLAlchemy()
tz = pytz.timezone('Europe/Paris')


class Course(db.Model):
    __tablename__ = 'course'

    id = db.Column(Integer, primary_key=True)
    name = db.Column(Text)
    comment = db.Column(Text)
    department = db.Column(Text)
    place = db.Column(Text)
    date = db.Column(Date)
    time_begin = db.Column(Time)
    time_end = db.Column(Time)
    link = db.Column(Text)

    def __toJSON__(self):
        return {
            'id': self.id,
            'name': self.name,
            'comment': self.comment,
            'department': self.department,
            'place': self.place,
            'date': self.date.isoformat(),
            'time_begin': self.__combine_iso(self.date, self.time_begin),
            'time_end': self.__combine_iso(self.date, self.time_end),
            'link': self.link,
        }

    @staticmethod
    def __combine_iso(date, time):
        """ Combine a local date and time and make it TZ aware """
        return tz.localize(
            datetime.combine(date, time)
        ).isoformat()

    def __repr__(self):
        return "<Course %s for %s at %s (%s %s)>" % \
               (self.name, self.department, self.place, self.time_begin, self.date)
