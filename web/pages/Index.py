
from google.appengine.ext.webapp import template
import webapp2
import json
from models.user import User
from models.shift import Shift
from models.submission import *
from models.staticfunctions import Staticfunctions
from datetime import *


class HomeHandler(webapp2.RequestHandler):
    def get(self):

        user = None
        if self.request.cookies.get('our_token'):    #the cookie that should contain the access token!
            user = User.checkToken(self.request.cookies.get('our_token'))

        template_variables = {}

        template_variables['sundayDate'] = Staticfunctions.getSundayDate(date.today(), 1)
        template_variables['saturdayDate'] = Staticfunctions.getSundayDate(date.today(), 7)

        schedule = Shift.qryGetWeekShiftsByDate(date.today())
        template_variables['schedule'] = []
        for sft in schedule:
            template_variables['schedule'].append({
                "empno": sft.employee_number,
                "day": sft.day_of_the_week,
                "hour": sft.shift_hour,
                "role": sft.role
            })

        schedule2 = Shift.qryGetWeekShiftsByDate(date.today()+timedelta(days=7))
        if schedule2.count == 0:
            print 0
        else:
            template_variables['schedule2'] = []
            for sft in schedule:
                template_variables['schedule2'].append({
                    "empno": sft.employee_number,
                    "day": sft.day_of_the_week,
                    "hour": sft.shift_hour,
                    "role": sft.role
                })
        usersList = User.getAllActiveUsers() #QUERY
        template_variables['userlist'] = []
        for tmpuser in usersList:
            template_variables['userlist'].append({
                "empno": tmpuser.employee_number,
                "email": tmpuser.email,
                "firstname": tmpuser.first_name,
                "lastname": tmpuser.last_name,
                "phone_num": tmpuser.phone_num
            })
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


class SubmissionShiftsHandler(webapp2.RequestHandler):
    def get(self):
        user = None
        if self.request.cookies.get('our_token'):    #the cookie that should contain the access token!
                user = User.checkToken(self.request.cookies.get('our_token'))

        template_variables = {}
        if user:
            template_variables['user'] = user.email

            nws = Submission.qryGetNextWeekSubmissionsByEmp(user.employee_number) #next week submission by empno
            template_variables['submissions'] = []
            for sub in nws:
                print sub
                template_variables['submissions'].append({
                    "shift_hour": sub.shift_hour,
                    "day_of_the_week": sub.day_of_the_week
                })

            noteqr = Note.qryGetNoteByEmp(user.employee_number)

            note = ""
            for nt in noteqr:
                note = nt.note
            template_variables['note'] = note

            for x in range(1,8):
                template_variables['day%d' % (x)] = Staticfunctions.nextWeekDate(x)
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
        self.response.write(json.dumps({'status': 'OK'}))


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
        phone_num = self.request.get('phone_num')
        if not password or not email or not isAdmin or not firstname or not lastname or not empno or not phone_num:
            self.error(403)
            self.response.write('Missing Fields!')
            return

        user = User.query(User.email == email).get()
        if user:
            self.error(402)
            self.response.write('Email taken!')
            return

        num = User.query(User.employee_number == empno).get()
        if num:
            self.error(402)
            self.response.write('Employee Number Taken!')
            return

        import re

        def validate_email(email):
            if len(email) > 7:
                if re.match("^[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", email):
                    return 1
            return 0

        is_valid = validate_email(email)

        if is_valid == 0:
            self.error(402)
            self.response.write('Email Is Not valid!')
            return

        phone_length = len(phone_num)

        if phone_length != 10:
            self.error(402)
            self.response.write('Phone Number Not Valid!')
            return

        user = User()
        user.email = email
        user.setPassword(password)
        user.isAdmin = ('1' == isAdmin)
        user.first_name = firstname
        user.last_name = lastname
        user.employee_number = empno
        user.phone_num = phone_num
        user.isActive = True
        user.put()
        self.response.set_cookie('our_token', str(user.key.id()))
        self.response.write(json.dumps({'status': 'OK'}))


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


class SubmissionAttHandler(webapp2.RequestHandler):
    def get(self):
        user = None
        if self.request.cookies.get('our_token'):    #the cookie that should contain the access token!
            user = User.checkToken(self.request.cookies.get('our_token'))
        if not user:
            self.redirect("/")
        nws = Submission.qryGetNextWeekSubmissionsByEmp(user.employee_number)
        for sub in nws:
            sub.key.delete()

        shifts = json.loads(self.request.get('shifts'))
        for tmpshift in shifts:
            submission = Submission()
            submission.dateSent = datetime.today()
            submission.shift_hour = int(tmpshift['shiftHour'])
            submission.day_of_the_week = int(tmpshift['weekDay'])
            submission.week_sunday_date = Staticfunctions.nextWeekDate(1)
            submission.employee_number = user.employee_number
            submission.put()

        lastnote = Note.qryGetNoteByEmp(user.employee_number)
        for tmpnote in lastnote:
            tmpnote.key.delete()

        notes = Note()
        notes.note = self.request.get('notes')
        notes.employee_number = user.employee_number
        notes.week_sunday_date = Staticfunctions.nextWeekDate(1)
        notes.date_sent = datetime.today()
        notes.put()

        self.response.write('Shifts sent successfully')
        self.response.set_cookie('our_token', str(user.key.id()))
        self.response.write(json.dumps({'status': 'OK'}))


class UserProfileAttHandler(webapp2.RequestHandler):
    def get(self):
        user = None
        if self.request.cookies.get('our_token'):    #the cookie that should contain the access token!
            user = User.checkToken(self.request.cookies.get('our_token'))
        if not user:
            self.redirect("/")
        email = self.request.get('email')
        firstname = self.request.get('firstname')
        lastname = self.request.get('lastname')
        empno = self.request.get('empno')
        phone_num = self.request.get('phone_num')
        user2 = User.query(User.email == email).get()

        user2.first_name = firstname
        user2.last_name = lastname
        user2.employee_number = empno
        user2.phone_num = phone_num

        user2.put()

        self.response.write(json.dumps({'status': 'OK'}))


class DeleteEmployeeHandler(webapp2.RequestHandler):
    def get(self):
        user = None
        if self.request.cookies.get('our_token'):    #the cookie that should contain the access token!
                user = User.checkToken(self.request.cookies.get('our_token'))

        template_variables = {}
        usersList = User.getAllUsers() #QUERY
        template_variables['user_list'] = []
        for tmpuser in usersList:
            template_variables['user_list'].append({
                "empno": tmpuser.employee_number,
                "email": tmpuser.email,
                "firstname": tmpuser.first_name,
                "lastname": tmpuser.last_name,
                "phone_num": tmpuser.phone_num,
                "isActive": tmpuser.isActive
            })
        if user:
            template_variables['user'] = user.email
        else:
            self.redirect('/Admin')

        html = template.render('web/templates/DeleteEmployee.html', template_variables)
        self.response.write(html)


class DeleteEmployeeAttHandler(webapp2.RequestHandler):
    def get(self):
        user = None
        if self.request.cookies.get('our_token'):    #the cookie that should contain the access token!
            user = User.checkToken(self.request.cookies.get('our_token'))
        if not user:
            self.redirect("/")
        activation = json.loads(self.request.get('activation'))
        non_activation = json.loads(self.request.get('non_activation'))

        for act in activation:
            user2 = User.query(User.email == act['email']).get()
            user2.isActive = True
            user2.put()

        for non_act in non_activation:
            user3 = User.query(User.email == non_act['non_email']).get()
            user3.isActive = False
            user3.put()

        self.response.write(json.dumps({'status': 'OK'}))


class ResetPasswordHandler(webapp2.RequestHandler):
    def get(self):
        user = None
        if self.request.cookies.get('our_token'):    #the cookie that should contain the access token!
            user = User.checkToken(self.request.cookies.get('our_token'))

        template_variables = {}
        if user:
            template_variables['user'] = user.email

        html = template.render('web/templates/ResetPassword.html', template_variables)
        self.response.write(html)


class ResetPasswordAttHandler(webapp2.RequestHandler):
    def get(self):
        email = self.request.get('email')
        password = self.request.get('password')

        if not password or not email:
            self.error(403)
            self.response.write('Missing Fields!')
            return

        import re

        def validate_email(email):
            if len(email) > 7:
                if re.match("^[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", email):
                    return 1
            return 0

        is_valid = validate_email(email)

        if is_valid == 0:
            self.error(402)
            self.response.write('Email Is Not valid!')
            return

        user = User.query(User.email == email).get()
        if not user:
            self.error(402)
            self.response.write('Email Not Exist!')
            return

        user.setPassword(password)
        user.put()

        from google.appengine.api import mail
        url = 'http://shiftssm.appspot.com'
        user_address = "<" + email + ">"
        sender_address = "SSM - Shift Submitter Support <ssmshift@shiftssm.appspotmail.com>"
        subject = "New Password"
        body = """Your new Password: """ + password + """\n"""
        body += """Click here to go back to site """ + url

        mail.send_mail(sender_address, user_address, subject, body)

        #self.response.set_cookie('our_token', str(user.key.id()))
        self.response.write(json.dumps({'status': 'OK'}))


app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/Home', HomeHandler),
    ('/History', HistoryHandler),
    ('/About', AboutHandler),
    ('/SubmissionShifts', SubmissionShiftsHandler),
    ('/SwitchShifts', SwitchShiftsHandler),
    ('/Login', LoginHandler),
    ('/loginAtt', LoginAttHandler),
    ('/Register', RegisterHandler),
    ('/registerAtt', RegisterAttHandler),
    ('/UserProfileAtt', UserProfileAttHandler),
    ('/logout', LogoutHandler),
    ('/personal', PersonalHandler),
    ('/submissionAtt', SubmissionAttHandler),
    ('/DeleteEmployee', DeleteEmployeeHandler),
    ('/DeleteEmployeeAtt', DeleteEmployeeAttHandler),
    ('/ResetPassword', ResetPasswordHandler),
    ('/ResetPasswordAtt', ResetPasswordAttHandler),
    ('/(.*)', FourOFourHandler)

], debug=True)
