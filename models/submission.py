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
    def qryGetNextWeekSubmissions():
        nextWeekDate = Staticfunctions.nextWeekDate(1)
        qry = "SELECT employee_number,shift_hour,day_of_the_week FROM Submission WHERE week_sunday_date = DATE('%s') ORDER BY day_of_the_week ASC, shift_hour ASC" % (nextWeekDate)
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

    @staticmethod
    def qryGetNoteByEmp(empno):
        nextWeekDate = Staticfunctions.nextWeekDate(1)
        qry = "SELECT * FROM Note WHERE employee_number = '%s'" % (empno)
        return ndb.gql(qry)