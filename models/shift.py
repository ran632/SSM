__author__ = 'Elad'
from google.appengine.ext import ndb


class Shift(ndb.Model):
    employee_number = ndb.StringProperty()
    start_date = ndb.DateTimeProperty()
    end_date = ndb.DateTimeProperty()
    shift_id = ndb.StringProperty()
