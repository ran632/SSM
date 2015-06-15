from google.appengine.ext import ndb
import hashlib      #we need this to safely store passwords
import logging


class User(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    employee_number = ndb.StringProperty()
    email = ndb.StringProperty()
    password = ndb.StringProperty()
    isAdmin = ndb.BooleanProperty()
    isActive = ndb.BooleanProperty()
    phone_num = ndb.StringProperty()


    @staticmethod
    def checkToken(token):
        user = User.get_by_id(long(token))
        return user

    def setPassword(self, password):
        self.password = hashlib.md5(password).hexdigest()
        self.put()

    def checkPassword(self, password):
        if not password:
            return False
        logging.info("self.pass: {}, hashed pass: {}".format(self.password, hashlib.md5(password).hexdigest()))
        if self.password == hashlib.md5(password).hexdigest():
            return True
        return False

    @staticmethod
    def getAllActiveUsers():
        qry = "SELECT email,employee_number,first_name,last_name,phone_num FROM User WHERE isActive=True"
        return ndb.gql(qry)

    @staticmethod
    def getAllUsers():
        qry = "SELECT email,employee_number,first_name,last_name,phone_num,isActive FROM User"
        return ndb.gql(qry)

    @staticmethod
    def strNameByEmpNo(empno):
        for emp in User.getAllUsers():
            if empno == emp.employee_number and emp.first_name != None and emp.last_name != None:
                return emp.first_name + " " + emp.last_name
        return ""

    @staticmethod
    def getAllUsersEmail():
        qry = "SELECT email FROM User WHERE isActive=True"
        return ndb.gql(qry)
