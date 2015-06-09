__author__ = 'Elad'
from google.appengine.ext import ndb
from staticfunctions import Staticfunctions

class Shift(ndb.Model):
    employee_number = ndb.StringProperty()
    shift_hour = ndb.IntegerProperty()
    day_of_the_week = ndb.IntegerProperty()
    role = ndb.IntegerProperty()
    week_sunday_date = ndb.DateProperty()

    @staticmethod
    def qryGetNextWeekShifts():
        nextWeekDate = Staticfunctions.nextWeekDate(1)
        qry = "SELECT * FROM Shift WHERE week_sunday_date = DATE('%s')" % (nextWeekDate)
        return ndb.gql(qry)