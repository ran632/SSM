from google.appengine.ext.webapp import template
import webapp2
import json
from web.pages.Index import *
from models.shift import Shift
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
        print "DATE = " + self.request.get('date')
        if self.request.get('date') == "":
            givendate = Staticfunctions.nextWeekDate(1)
        else:
            givendate = datetime.strptime(self.request.get('date'), '%Y-%m-%d').date()

        sundayOfGivenDate = Staticfunctions.getSundayDate(givendate,1)

        template_variables['sundayDateISO'] = sundayOfGivenDate.isoformat()
        template_variables['sundayDate'] = sundayOfGivenDate
        template_variables['saturdayDate'] = sundayOfGivenDate + timedelta(days=6)

        shifts = Shift.qryGetWeekShiftsByDate(givendate)
        template_variables['shifts'] = []
        for sft in shifts:
            template_variables['shifts'].append({
                "day": sft.day_of_the_week,
                "hour": sft.shift_hour,
                "role": sft.role,
                "empno": sft.employee_number
            })

        nextWeekSubmissions = Submission.qryGetWeekSubmissionsByDate(givendate)
        template_variables['nextWeekSubmissions'] = []
        for sub in nextWeekSubmissions:
            template_variables['nextWeekSubmissions'].append({
                "day": sub.day_of_the_week,
                "hour": sub.shift_hour,
                "empno": sub.employee_number,
                "full_name": User.strNameByEmpNo(sub.employee_number)
            })

        usersList = User.getAllActiveUsers()
        template_variables['userlist'] = []
        for tmpuser in usersList:

            template_variables['userlist'].append({
                "empno": tmpuser.employee_number,
                "email": tmpuser.email,
                "firstname": tmpuser.first_name,
                "lastname": tmpuser.last_name,
                "phone_num": tmpuser.phone_num,
                "isSent": Note.isSentSubmissionByEmp(tmpuser.employee_number)
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
        user = None
        if self.request.cookies.get('our_token'):    #the cookie that should contain the access token!
            user = User.checkToken(self.request.cookies.get('our_token'))
        if not user:
            self.redirect("/")
            return

        #delete previous changes
        nws = Shift.qryGetNextWeekShifts()
        for sft in nws:
            sft.key.delete()

        schedule = json.loads(self.request.get('schedule'))
        #{"empno": empno, "day": dayCount, "hour": hourCount, "role": roleCount}
        for ob in schedule:
            if ob['empno'] == '':
                continue
            shift = Shift()
            shift.employee_number = ob['empno']
            shift.week_sunday_date = Staticfunctions.nextWeekDate(1)
            shift.day_of_the_week = int(ob['day'])
            shift.shift_hour = int(ob['hour'])
            shift.role = int(ob['role'])
            shift.put()

        self.response.write(json.dumps({'status':'OK'}))



app = webapp2.WSGIApplication([
	('/Admin', AdminHandler),
    ('/Admin/schedulizeAtt', SchedulizeHandler),
	('/Admin/(.*)', FourOFourHandler)
	

], debug=True)
