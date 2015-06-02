from google.appengine.ext.db import StringProperty

__author__ = 'Elad'
from google.appengine.ext import ndb


class Submission(ndb.Model):
    employee_number = ndb.StringProperty()
    dateSent = ndb.DateTimeProperty()
    shift_hour = ndb.IntegerProperty()
    day_of_the_week = ndb.IntegerProperty()
    week_sunday_date = ndb.DateProperty()

class Note(ndb.Model):
    note = ndb.StringProperty()
    week_sunday_date = ndb.DateProperty()
    employee_number = ndb.StringProperty()