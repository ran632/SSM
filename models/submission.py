from google.appengine.ext.db import StringProperty

__author__ = 'Elad'
from google.appengine.ext import ndb


class Submission(ndb.Model):
    employee_number = ndb.StringProperty()
    dateSent = ndb.DateTimeProperty()
    shift_hour = ndb.IntegerProperty()
    day_of_the_week = ndb.IntegerProperty()
    week_number = ndb.IntegerProperty()