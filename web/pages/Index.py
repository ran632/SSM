
from google.appengine.ext.webapp import template
import webapp2
import json
#import simplejson
from models.user import User
from models.shift import Shift
from models.submission import *
from models.staticfunctions import Staticfunctions
from models.switch import Switch
from datetime import *


class HomeHandler(webapp2.RequestHandler):
    def get(self):

        user = None
        if self.request.cookies.get('our_token'):    #the cookie that should contain the access token!
            user = User.checkToken(self.request.cookies.get('our_token'))

        if not user:
            self.redirect('/Login')
            return

        template_variables = {}

        thisUserThisWeekShifts = Shift.qryGetWeekShiftsByDateEmpFromNow(date.today(),User.emailToEmpno(user.email)).get()
        template_variables['ShiftsNum'] = Shift.qryGetWeekShiftsByDateEmp(date.today(),User.emailToEmpno(user.email)).count()
        if thisUserThisWeekShifts != None:
            template_variables['Nextshift'] = Staticfunctions.dayToString(thisUserThisWeekShifts.day_of_the_week) + " " + Staticfunctions.hourToString(thisUserThisWeekShifts.shift_hour)
        if Note.isSentSubmissionByEmp(date.today()+timedelta(days=7), User.emailToEmpno(user.email)):
            template_variables['isSent'] = True
        template_variables['sundayDate'] = Staticfunctions.getSundayDate(date.today(), 1)
        template_variables['saturdayDate'] = Staticfunctions.getSundayDate(date.today(), 7)
        template_variables['nextSundayDate'] = Staticfunctions.getSundayDate(date.today()+timedelta(days=7), 1)
        template_variables['nextSaturdayDate'] = Staticfunctions.getSundayDate(date.today()+timedelta(days=7), 7)

        schedule = Shift.qryGetWeekShiftsByDate(date.today())
        template_variables['schedule'] = []
        for sft in schedule:
            template_variables['schedule'].append({
                "empno": sft.employee_number,
                "day": sft.day_of_the_week,
                "hour": sft.shift_hour,
                "role": sft.role
            })

        scheduleNext = Shift.qryGetWeekShiftsByDate(date.today()+ timedelta(days=7))
        if scheduleNext.count == 0:
            print 0
        else:
            template_variables['scheduleNext'] = []
            for sft in scheduleNext:
                template_variables['scheduleNext'].append({
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

        if self.request.get('date') == "":
            givendate = Staticfunctions.getSundayDate(date.today(), 1)
        else:
            givendate = datetime.strptime(self.request.get('date'), '%Y-%m-%d').date()

        sundayOfGivenDate = Staticfunctions.getSundayDate(givendate,1)
        template_variables['sundayDateISO'] = sundayOfGivenDate.isoformat()
        template_variables['sundayDate'] = sundayOfGivenDate
        template_variables['saturdayDate'] = sundayOfGivenDate + timedelta(days=6)

        schedule = Shift.qryGetWeekShiftsByDate(givendate)
        template_variables['schedule'] = []
        for sft in schedule:
            template_variables['schedule'].append({
                "empno": sft.employee_number,
                "day": sft.day_of_the_week,
                "hour": sft.shift_hour,
                "role": sft.role
            })

        usersList = User.getAllUsers() #QUERY
        template_variables['userlist'] = []
        for tmpuser in usersList:
            template_variables['userlist'].append({
                "empno": tmpuser.employee_number,
                "email": tmpuser.email,
                "firstname": tmpuser.first_name,
                "lastname": tmpuser.last_name,
                "phone_num": tmpuser.phone_num
            })


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

            note = Note.qryGetNoteByEmp(Staticfunctions.nextWeekDate(1) ,user.employee_number).get()
            if note != None:
                template_variables['note'] = note.note
                template_variables['shiftnum'] = note.num


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
            template_variables['userempno'] = user.employee_number
        else:
            self.redirect('/Login')
            return

        if self.request.get('cms'): #chosen my shift
            cms = self.request.get('cms')
            template_variables['cms'] = cms
            print cms
        if self.request.get('ce'): #chosen employee
            ce = self.request.get('ce')
            template_variables['ce'] = ce

        usersList = User.getAllActiveUsers() #QUERY
        template_variables['userlist'] = []
        for tmpuser in usersList:
            template_variables['userlist'].append({
                "empno": tmpuser.employee_number,
                "name": tmpuser.first_name + " " + tmpuser.last_name,
            })

        allshifts = Shift.qryGetWeekShiftsByDate(date.today())
        template_variables['allshifts'] = []
        for sft in allshifts:
            template_variables['allshifts'].append({
                "id": sft.key.id(),
                "empno": sft.employee_number,
                "shift": Shift.shiftToString(sft)
            })
        allshifts2 = Shift.qryGetWeekShiftsByDate(date.today()+timedelta(days=7))
        template_variables['allshifts2'] = []
        for sft in allshifts2:
            template_variables['allshifts2'].append({
                "id": sft.key.id(),
                "empno": sft.employee_number,
                "shift": Shift.shiftToString(sft)
            })

        recRequests = Switch.recRequests(user.employee_number)
        template_variables['recRequests'] = []
        for req in recRequests:
            try:
                from_shift = Shift.shiftToString(Shift.get_by_id(int(req.from_shift_id)))
            except:
                from_shift = ""
            try:
                to_shift = Shift.shiftToString(Shift.get_by_id(int(req.to_shift_id)))
            except:
                to_shift = ""
            template_variables['recRequests'].append({
                "id": req.key.id(),
                "from_empno": req.from_empno,
                "from_shift": from_shift,
                "to_shift": to_shift,
                "status": req.status
            })
        myRequests = Switch.myRequests(user.employee_number)
        template_variables['myRequests'] = []
        for req in myRequests:
            try:
                from_shift = Shift.shiftToString(Shift.get_by_id(int(req.from_shift_id)))
            except:
                from_shift = ""
            try:
                to_shift = Shift.shiftToString(Shift.get_by_id(int(req.to_shift_id)))
            except:
                to_shift = ""
            template_variables['myRequests'].append({
                "id": req.key.id(),
                "from_shift": from_shift,
                "to_empno": req.to_empno,
                "to_shift": to_shift,
                "status": req.status
            })

        html = template.render('web/templates/Switch_shifts.html', template_variables)
        self.response.write(html)

class SwitchAttHandler(webapp2.RequestHandler):
    def get(self):
        user = None
        if self.request.cookies.get('our_token'):    #the cookie that should contain the access token!
            user = User.checkToken(self.request.cookies.get('our_token'))
        if not user:
            self.redirect("/")
            return

        #from_shift_id:from_shift_id, to_empno:to_empno, to_shift_id:to_shift_id
        from_shift_id = (self.request.get('from_shift_id'))
        to_empno = (self.request.get('to_empno'))
        to_shift_id = (self.request.get('to_shift_id'))

        switch = Switch()
        switch.date = date.today()
        switch.status = 'pending'
        switch.from_empno = user.employee_number
        switch.from_shift_id = from_shift_id
        switch.to_empno = to_empno
        switch.to_shift_id = to_shift_id
        switch.put()

        self.response.set_cookie('our_token', str(user.key.id()))
        self.response.write(json.dumps({'status': 'OK'}))


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
            self.redirect('/')

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

        lastnote = Note.qryGetNoteByEmp(Staticfunctions.nextWeekDate(1),user.employee_number)
        for tmpnote in lastnote:
            tmpnote.key.delete()


        notes = Note()
        notes.note = self.request.get('notes')
        notes.employee_number = user.employee_number
        notes.week_sunday_date = Staticfunctions.nextWeekDate(1)
        notes.date_sent = datetime.now()
        shiftnum = self.request.get('numofshifts')
        try:
            notes.num = int(shiftnum)
        except:
            pass
        notes.put()

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
            #email = self.request.get(act['email'])
            user2 = User.query(User.email == act['email']).get()
            user2.isActive = True
            user2.put()

        for non_act in non_activation:
            #non_email = self.request.get(non_act['non_email'])
            user3 = User.query(User.email == non_act['non_email']).get()
            user3.isActive = False
            user3.put()


        self.response.write(json.dumps({'status': 'OK'}))


app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/Home', HomeHandler),
    ('/History', HistoryHandler),
    ('/About', AboutHandler),
    ('/SubmissionShifts', SubmissionShiftsHandler),
    ('/SwitchShifts', SwitchShiftsHandler),
    ('/switchAtt', SwitchAttHandler),
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
    ('/(.*)', FourOFourHandler)

], debug=True)
