from google.appengine.ext.db import StringProperty

__author__ = 'Elad'
from google.appengine.ext import ndb


class Shift(ndb.Model):
    employee_number = ndb.StringProperty()
    date = ndb.DateTimeProperty()
    shift_hour = StringProperty()
    week_number = ndb.StringProperty()
    shift_id = ndb.StringProperty()