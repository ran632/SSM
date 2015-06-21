from google.appengine.ext.db import StringProperty
from staticfunctions import Staticfunctions
__author__ = 'Elad'
from google.appengine.ext import ndb
from datetime import *

class Submission(ndb.Model):
    employee_number = ndb.StringProperty()
    dateSent = ndb.DateTimeProperty()
    shift_hour = ndb.IntegerProperty()
    day_of_the_week = ndb.IntegerProperty()
    week_sunday_date = ndb.DateProperty()

    @staticmethod
    def qryGetWeekSubmissionsByDate(tmpdate):
        sundayDate = Staticfunctions.getSundayDate(tmpdate,1)
        qry = "SELECT employee_number,shift_hour,day_of_the_week FROM Submission WHERE week_sunday_date = DATE('%s') ORDER BY day_of_the_week ASC, shift_hour ASC" % (sundayDate)
        return ndb.gql(qry)


    @staticmethod
    def qryGetNextWeekSubmissionsByEmp(empno):
        nextWeekDate = Staticfunctions.nextWeekDate(1)
        qry = "SELECT * FROM Submission WHERE week_sunday_date = DATE('%s') AND employee_number = '%s' ORDER BY day_of_the_week ASC, shift_hour ASC" % (nextWeekDate, empno)
        return ndb.gql(qry)

    @staticmethod
    def countSubmissionBy(empno, day, hour):
        qry = "SELECT * FROM Submission WHERE employee_number = '%s' AND day_of_the_week = %s AND shift_hour = %s" % (empno, day, hour)
        return ndb.gql(qry).count()

    @staticmethod
    def countSubmissionByDate(empno, date):
        qry = "SELECT * FROM Submission WHERE employee_number = '%s' AND week_sunday_date = DATE('%s')" % (empno, date)
        return ndb.gql(qry).count()

class Note(ndb.Model):
    note = ndb.StringProperty()
    num = ndb.IntegerProperty() #number of wanted shifts
    week_sunday_date = ndb.DateProperty()
    employee_number = ndb.StringProperty()
    date_sent = ndb.DateTimeProperty()

    @staticmethod
    def qryGetNoteByEmp(sundate, empno):
        qry = "SELECT * FROM Note WHERE week_sunday_date = DATE('%s') AND employee_number = '%s'" % (sundate, empno)
        return ndb.gql(qry)

    @staticmethod
    def qryGetNotesByDate(tmpDate):
        tmp2Date = Staticfunctions.getSundayDate(tmpDate, 1)
        qry = "SELECT * FROM Note WHERE week_sunday_date = DATE('%s')" % tmp2Date
        return ndb.gql(qry)

    @staticmethod
    def isSentSubmissionByEmp(tmpdate, empno):
        query = Note.qryGetNoteByEmp(Staticfunctions.getSundayDate(tmpdate,1), empno)
        return query.count()

