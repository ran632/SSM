
from google.appengine.ext import ndb
from staticfunctions import Staticfunctions
from datetime import *

class Switch(ndb.Model):
    from_empno = ndb.StringProperty()
    from_shift_id = ndb.StringProperty()
    to_empno = ndb.StringProperty()
    to_shift_id = ndb.StringProperty()
    date = ndb.DateProperty()
    status = ndb.StringProperty()

    @staticmethod
    def myRequests(empno):
        qry = "SELECT * FROM Switch WHERE from_empno = '%s' ORDER BY status ASC, date ASC" % (empno)
        return ndb.gql(qry)

    @staticmethod
    def recRequests(empno):
        qry = "SELECT * FROM Switch WHERE to_empno = '%s' ORDER BY status ASC, date ASC" % (empno)
        return ndb.gql(qry)


