__author__ = 'Elad'
from google.appengine.ext import ndb


class Shift(ndb.Model):
    employee_number = ndb.StringProperty()
    shift_hour = ndb.IntegerProperty()
    day_of_the_week = ndb.IntegerProperty()
    role = ndb.IntegerProperty()
    week_sunday_date = ndb.DateProperty()
