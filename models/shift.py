__author__ = 'Elad'
from google.appengine.ext import ndb
from staticfunctions import Staticfunctions
from datetime import *

class Shift(ndb.Model):
    employee_number = ndb.StringProperty()
    shift_hour = ndb.IntegerProperty()
    day_of_the_week = ndb.IntegerProperty()
    role = ndb.IntegerProperty()
    week_sunday_date = ndb.DateProperty()


    @staticmethod
    def qryGetSunMorningAfter(tmpdate):
        sundayDate = Staticfunctions.getSundayDate(tmpdate + timedelta(days=7) ,1)
        qry = "SELECT employee_number FROM Shift WHERE week_sunday_date = DATE('%s') AND day_of_the_week = 1 AND shift_hour = 0" % (sundayDate)
        return ndb.gql(qry)
    @staticmethod
    def qryGetSatNightBefore(tmpdate):
        sundayDate = Staticfunctions.getSundayDate(tmpdate - timedelta(days=7) ,1)
        qry = "SELECT employee_number FROM Shift WHERE week_sunday_date = DATE('%s') AND day_of_the_week = 7 AND shift_hour = 2" % (sundayDate)
        return ndb.gql(qry)
    @staticmethod
    def qryGetWeekShiftsByDate(tmpdate):
        sundayDate = Staticfunctions.getSundayDate(tmpdate,1)
        qry = "SELECT * FROM Shift WHERE week_sunday_date = DATE('%s')" % (sundayDate)
        return ndb.gql(qry)

    @staticmethod
    def qryGetWeekShiftsByDateEmpFromNow(tmpdate, empno):
        sundayDate = Staticfunctions.getSundayDate(tmpdate,1)
        today = date.today().isoweekday()+1
        if today == 8:
            today = 1
        qry = "SELECT * FROM Shift WHERE week_sunday_date = DATE('%s') AND employee_number = '%s' AND day_of_the_week >= %s  ORDER BY day_of_the_week ASC, shift_hour ASC" % (sundayDate,empno,today)
        return ndb.gql(qry)

    @staticmethod
    def qryGetWeekShiftsByDateEmp(tmpdate, empno):
        sundayDate = Staticfunctions.getSundayDate(tmpdate,1)
        qry = "SELECT * FROM Shift WHERE week_sunday_date = DATE('%s') AND employee_number = '%s'" % (sundayDate,empno)
        return ndb.gql(qry)


