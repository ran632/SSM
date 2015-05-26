
from google.appengine.ext.webapp import template
from models.user import User
import webapp2
import json


class IndexHandler(webapp2.RequestHandler):
    def get(self):
        template_params = {}

        html = template.render("web/templates/Login.html", template_params)
        self.response.write(html)


class LoginUserHandler(webapp2.RequestHandler):
    def get(self):
        email = self.request.get('Email')
        password = self.request.get('Pass')
        employee = User.query(User.email == email).get()
        if not employee or not employee.checkPassword(password):
            self.response.write("Wrong username or password")
            return

        self.response.write(json.dumps({'status': 'OK'}))

app = webapp2.WSGIApplication([
    ('/Login', IndexHandler),
    ('/Home', LoginUserHandler),
    ('/', LoginUserHandler)
], debug=True)
