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

class Note(ndb.Model):
    note = ndb.StringProperty()
    week_sunday_date = ndb.DateProperty()
    employee_number = ndb.StringProperty()
    date_sent = ndb.DateTimeProperty()

    @staticmethod
    def qryGetNoteByEmp(empno):
        nextWeekDate = Staticfunctions.nextWeekDate(1)
        qry = "SELECT * FROM Note WHERE week_sunday_date = DATE('%s') AND employee_number = '%s'" % (nextWeekDate, empno)
        return ndb.gql(qry)

    @staticmethod
    def qryGetNotesByDate(tmpDate):
        tmp2Date = Staticfunctions.getSundayDate(tmpDate, 1)
        qry = "SELECT * FROM Note WHERE week_sunday_date = DATE('%s')" % tmp2Date
        return ndb.gql(qry)

    @staticmethod
    def isSentSubmissionByEmp(empno):
        query = Note.qryGetNoteByEmp(empno)
        return query.count()