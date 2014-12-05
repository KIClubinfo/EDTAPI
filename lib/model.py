__author__ = 'mickael'
from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy.sql.sqltypes import Integer, Text, Date, Time

db = SQLAlchemy()


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
            'time_begin': self.time_begin.isoformat(),
            'time_end': self.time_end.isoformat(),
            'link': self.link,
        }

    def __repr__(self):
        return "<Course %s for %s at %s (%s %s)>" % \
               (self.name, self.department, self.place, self.time_begin, self.date)
