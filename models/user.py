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
        qry = "SELECT email,employee_number,first_name,last_name FROM User WHERE isActive=True"
        return ndb.gql(qry)
