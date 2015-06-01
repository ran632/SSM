from google.appengine.ext.webapp import template
import webapp2
import json
from web.pages.Index import *
from models.user import User
from models.submission import *
from models.staticfunctions import Staticfunctions
from datetime import *


class AdminHandler(webapp2.RequestHandler):
    def get(self):
        user = None
        if self.request.cookies.get('our_token'):    #the cookie that should contain the access token!
            user = User.checkToken(self.request.cookies.get('our_token'))

        template_variables = {}
        template_variables['sundayDate'] = Staticfunctions.nextWeekDate(1)
        template_variables['saturdayDate'] = Staticfunctions.nextWeekDate(7)

        nextWeekSubmissions = Submission.qryGetNextWeekSubmissions()
        template_variables['nextWeekSubmissions'] = []
        for sub in nextWeekSubmissions:
            template_variables['nextWeekSubmissions'].append({
                "day": sub.day_of_the_week,
                "hour": sub.shift_hour,
                "sub_empno": sub.employee_number,
                "full_name": User.strNameByEmpNo(sub.employee_number)
            })

        usersList = User.getAllActiveUsers()
        template_variables['userlist'] = []
        for tmpuser in usersList:
            template_variables['userlist'].append({
                "empno": tmpuser.employee_number,
                "email": tmpuser.email,
                "firstname": tmpuser.first_name,
                "lastname": tmpuser.last_name
            })

        if user and user.isAdmin == True:
            template_variables['user'] = user.email
        else:
            if user:
                self.redirect('/Home')
            else:
                self.redirect('/Login')

        html = template.render('web/templates/Admin.html', template_variables)
        self.response.write(html)

class SchedulizeHandler(webapp2.RequestHandler):
    def get(self):
        print 'in schedulize'
        user = None
        if self.request.cookies.get('our_token'):    #the cookie that should contain the access token!
            user = User.checkToken(self.request.cookies.get('our_token'))
        if not user:
            self.redirect("/")
        print "data" + self.request.get('data')
        self.redirect("/History")

app = webapp2.WSGIApplication([
	('/Admin', AdminHandler),
    ('/Admin/schedulizeAtt', SchedulizeHandler),
	('/Admin/(.*)', FourOFourHandler)
	
], debug=True)
