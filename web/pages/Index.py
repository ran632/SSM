
from google.appengine.ext.webapp import template
import webapp2
import json
from models.user import User
class HomeHandler(webapp2.RequestHandler):
    def get(self):

        user = None
        if self.request.cookies.get('our_token'):    #the cookie that should contain the access token!
            user = User.checkToken(self.request.cookies.get('our_token'))

        template_variables = {}
        if user:
            template_variables['user'] = user.email
        else:
            self.redirect('/Login')

        html = template.render('web/templates/Home.html', template_variables)
        self.response.write(html)

class HistoryHandler(webapp2.RequestHandler):
    def get(self):
        user = None
        if self.request.cookies.get('our_token'):    #the cookie that should contain the access token!
                user = User.checkToken(self.request.cookies.get('our_token'))

        template_variables = {}
        if user:
            template_variables['user'] = user.email
        else:
            self.redirect('/Login')

        html = template.render('web/templates/History.html', template_variables)
        self.response.write(html)
		
class AboutHandler(webapp2.RequestHandler):
    def get(self):
        user = None
        if self.request.cookies.get('our_token'):    #the cookie that should contain the access token!
                user = User.checkToken(self.request.cookies.get('our_token'))

        template_variables = {}
        if user:
            template_variables['user'] = user.email

        html = template.render('web/templates/About.html', template_variables)
        self.response.write(html)
		
class AdminHandler(webapp2.RequestHandler):
    def get(self):
        user = None
        if self.request.cookies.get('our_token'):    #the cookie that should contain the access token!
                user = User.checkToken(self.request.cookies.get('our_token'))

        template_variables = {}
        if user and user.isAdmin == True:
            template_variables['user'] = user.email
        else:
            if user:
                self.redirect('/Home')
            else:
                self.redirect('/Login')

        html = template.render('web/templates/Admin.html', template_variables)
        self.response.write(html)
		
class SubmissionShiftsHandler(webapp2.RequestHandler):
    def get(self):
        user = None
        if self.request.cookies.get('our_token'):    #the cookie that should contain the access token!
                user = User.checkToken(self.request.cookies.get('our_token'))

        template_variables = {}
        if user:
            template_variables['user'] = user.email
        else:
            self.redirect('/Login')

        html = template.render('web/templates/Submission_shifts.html', template_variables)
        self.response.write(html)
		
class SwitchShiftsHandler(webapp2.RequestHandler):
    def get(self):
        user = None
        if self.request.cookies.get('our_token'):    #the cookie that should contain the access token!
                user = User.checkToken(self.request.cookies.get('our_token'))

        template_variables = {}
        if user:
            template_variables['user'] = user.email
        else:
            self.redirect('/Login')

        html = template.render('web/templates/Switch_shifts.html', template_variables)
        self.response.write(html)
		
class FourOFourHandler(webapp2.RequestHandler):
	def get(self, args=None):
		template_params = {}
		html = template.render("web/templates/404.html", template_params)
		self.response.write(html)

		
#============Login system handlers===================================
class LoginHandler(webapp2.RequestHandler):
    def get(self):
        user = None
        if self.request.cookies.get('our_token'):    #the cookie that should contain the access token!
            user = User.checkToken(self.request.cookies.get('our_token'))

        template_variables = {}
        if user:
            template_variables['user'] = user.email

        html = template.render('web/templates/Login.html', template_variables)
        self.response.write(html)
		

class LoginAttHandler(webapp2.RequestHandler):
    def get(self):
        email = self.request.get('email')
        password = self.request.get('password')
        user = User.query(User.email == email).get()
        if not user or not user.checkPassword(password):
            self.error(403)
            self.response.write('Wrong username or password')
            return

        self.response.set_cookie('our_token', str(user.key.id()))
        self.response.write(json.dumps({'status':'OK'}))
		
class RegisterHandler(webapp2.RequestHandler):
    def get(self):
        user = None
        if self.request.cookies.get('our_token'):    #the cookie that should contain the access token!
                user = User.checkToken(self.request.cookies.get('our_token'))

        template_variables = {}
        if user:
            self.redirect('/')

        html = template.render('web/templates/Register.html', template_variables)
        self.response.write(html)

class RegisterAttHandler(webapp2.RequestHandler):
    def get(self):
        email = self.request.get('email')
        password = self.request.get('password')
        isAdmin = self.request.get('isAdmin')
        firstname = self.request.get('firstname')
        lastname = self.request.get('lastname')
        empno = self.request.get('empno')
        if not password:
            self.error(403)
            self.response.write('Empty password submitted')
            return

        user = User.query(User.email == email).get()
        if user:
            self.error(402)
            self.response.write('Email taken')
            return

        user = User()
        user.email = email
        user.setPassword(password)
        user.isAdmin = ('1' == isAdmin)
        user.first_name = firstname
        user.last_name = lastname
        user.employee_number = empno
        user.isActive = True
        user.put()
        self.response.set_cookie('our_token', str(user.key.id()))
        self.response.write(json.dumps({'status':'OK'}))
		

class LogoutHandler(webapp2.RequestHandler):
    def get(self):
        self.response.delete_cookie('our_token')
        self.redirect('/')

class PersonalHandler(webapp2.RequestHandler):
    def get(self):
        user = None
        if self.request.cookies.get('our_token'):    #the cookie that should contain the access token!
            user = User.checkToken(self.request.cookies.get('our_token'))

        template_variables = {}
        if user:
            template_variables['user'] = user.email

        html = template.render('web/templates/Home.html', template_variables)
        self.response.write(html)

app = webapp2.WSGIApplication([
    ('/', HomeHandler),
	('/Home', HomeHandler),
	('/History', HistoryHandler),
	('/About', AboutHandler),
	('/Admin', AdminHandler),
	('/SubmissionShifts', SubmissionShiftsHandler),
	('/SwitchShifts', SwitchShiftsHandler),
	('/Login', LoginHandler),
    ('/loginAtt', LoginAttHandler),
	('/Register', RegisterHandler),
    ('/registerAtt', RegisterAttHandler),
    ('/logout', LogoutHandler),
    ('/personal', PersonalHandler),
	('/(.*)', FourOFourHandler)
	
], debug=True)
