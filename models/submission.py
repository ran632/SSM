from google.appengine.ext.db import StringProperty

__author__ = 'Elad'
from google.appengine.ext import ndb


class Submission(ndb.Model):
    employee_number = ndb.StringProperty()
    date = ndb.DateTimeProperty()
    shift_hour = ndb.StringProperty()
    week_number = ndb.IntegerProperty()