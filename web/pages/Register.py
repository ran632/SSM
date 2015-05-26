
from google.appengine.ext.webapp import template
from models.user import User
import webapp2
import json


class IndexHandler(webapp2.RequestHandler):
    def get(self):
        template_params = {}
        html = template.render("web/templates/Register.html", template_params)
        self.response.write(html)


class RegistrationHandler(webapp2.RequestHandler):
    def get(self):
        first_name = self.request.get('FirstName')
        last_name = self.request.get('LastName')
        employee_num = self.request.get('EmployeeNumber')
        email = self.request.get('Email')
        password = self.request.get('Pass')

        if not first_name or not last_name or not employee_num or not email or not password:
            self.response.write("Missing fields!")
            return

        employee = User.query(User.email == email).get()

        if employee:
            self.response.write('This username already exist!')
            return

        employee = User()
        employee.first_name - first_name
        employee.last_name = last_name
        employee.email = email
        employee.set_password(password)
        employee.put()

        self.response.write(json.dumps({'status': 'OK'}))


app = webapp2.WSGIApplication([('/Register', IndexHandler)
                               , ('/Home', RegistrationHandler)
                               ], debug=True)