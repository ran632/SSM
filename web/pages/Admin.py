from google.appengine.ext.webapp import templateimport webapp2import jsonfrom web.pages.Index import *from models.shift import Shiftfrom models.user import Userfrom models.submission import *from models.staticfunctions import Staticfunctionsfrom datetime import *class AdminHandler(webapp2.RequestHandler):    def get(self):        user = None        if self.request.cookies.get('our_token'):    #the cookie that should contain the access token!            user = User.checkToken(self.request.cookies.get('our_token'))        template_variables = {}        if self.request.get('date') == "":            givendate = Staticfunctions.nextWeekDate(1)        else:            givendate = datetime.strptime(self.request.get('date'), '%Y-%m-%d').date()        sundayOfGivenDate = Staticfunctions.getSundayDate(givendate,1)        template_variables['sundayDateISO'] = sundayOfGivenDate.isoformat()        template_variables['sundayDate'] = sundayOfGivenDate        template_variables['saturdayDate'] = sundayOfGivenDate + timedelta(days=6)        shifts = Shift.qryGetWeekShiftsByDate(givendate)        # template_variables['shifts'] = []        # for sft in shifts:        #     template_variables['shifts'].append({        #         "day": sft.day_of_the_week,        #         "hour": sft.shift_hour,        #         "role": sft.role,        #         "empno": sft.employee_number        #     })        #        nextWeekSubmissions = Submission.qryGetWeekSubmissionsByDate(givendate)        template_variables['nextWeekSubmissions'] = []        #add Saturday evening as 02 and sunday morning as 80        empsOnSatBefore = Shift.qryGetSatNightBefore(givendate)        for emp in empsOnSatBefore:            template_variables['nextWeekSubmissions'].append({                "day": 0,                "hour": 2,                "empno": emp.employee_number,                "full_name": User.strNameByEmpNo(emp.employee_number)            })        empsOnSunAfter = Shift.qryGetSunMorningAfter(givendate)        for emp in empsOnSunAfter:            template_variables['nextWeekSubmissions'].append({                "day": 8,                "hour": 0,                "empno": emp.employee_number,                "full_name": User.strNameByEmpNo(emp.employee_number)            })        #===============================================        usersList = User.getAllActiveUsers()        template_variables['userlist'] = []        for tmpuser in usersList:            template_variables['userlist'].append({                "empno": tmpuser.employee_number,                "email": tmpuser.email,                "firstname": tmpuser.first_name,                "lastname": tmpuser.last_name,                "phone_num": tmpuser.phone_num,                "isSent": Note.isSentSubmissionByEmp(sundayOfGivenDate, tmpuser.employee_number)            })        allNotes = Note.qryGetNotesByDate(sundayOfGivenDate) #TODO        template_variables['notes'] = []        for note in allNotes:            template_variables['notes'].append({                "empno": note.employee_number,                "note": note.note,                "date_sent": note.date_sent,                "numofshifts": note.num            })        template_variables['pop'] = [[[[] for k in range(0,5)] for j in range(0,3)] for i in range(0,8)]        for day in range(0,8):            for hour in range(0,3):                for role in range(0,5):                    for tmpuser in usersList:                        isSelected = False                        isSubbed = False                        qry1 = nextWeekSubmissions.filter(Submission.employee_number == tmpuser.employee_number, Submission.day_of_the_week == day, Submission.shift_hour == hour)                        if qry1.count() > 0:                            isSubbed = True                        qry2 = shifts.filter(Shift.employee_number == tmpuser.employee_number, Shift.day_of_the_week == day, Shift.shift_hour == hour, Shift.role == role)                        if qry2.count() > 0:                            isSelected = True                        template_variables['pop'][day][hour][role].append({                            "empno": tmpuser.employee_number,                            "name": tmpuser.first_name + " " + tmpuser.last_name,                            "isSubbed": isSubbed,                            "isSelected": isSelected                        })        progress = (float(allNotes.count())/float(usersList.count()))*100        print progress        template_variables['progress'] = progress        if user and user.isAdmin == True:            template_variables['user'] = user.email        else:            if user:                self.redirect('/Home')            else:                self.redirect('/Login')        html = template.render('web/templates/Admin.html', template_variables)        self.response.write(html)class SchedulizeHandler(webapp2.RequestHandler):    def get(self):        self.post()    def post(self):        user = None        if self.request.cookies.get('our_token'):    #the cookie that should contain the access token!            user = User.checkToken(self.request.cookies.get('our_token'))        if not user:            self.redirect("/")            return        givendate = datetime.strptime(self.request.get('date'), '%Y-%m-%d').date()        schedule = json.loads(self.request.get('schedule'))        sunday_date = Staticfunctions.getSundayDate(givendate, 1)        for ob in schedule:            shift = Shift.getShiftByDate(sunday_date,int(ob['day']),int(ob['hour']), int(ob['role']))            if not ob['empno']:                if shift:                    shift.key.delete()                continue            if not shift:                shift = Shift()            shift.employee_number = ob['empno']            shift.week_sunday_date = sunday_date            shift.day_of_the_week = int(ob['day'])            shift.shift_hour = int(ob['hour'])            shift.role = int(ob['role'])            shift.put()        # email_list = User.getAllUsersEmail()        # from google.appengine.api import mail        # url = 'http://shiftssm.appspot.com'        # for email in email_list:        #     user_address = "<" + email.email + ">"        #     sender_address = "SSM - Shift Submitter Support <ssmshift@shiftssm.appspotmail.com>"        #     subject = "New Schedule"        #     body = """New working schedule published, enter site to view it - """ + url        #     mail.send_mail(sender_address, user_address, subject, body)        self.response.write(json.dumps({'status': 'OK'}))class SendEmailsHandler(webapp2.RequestHandler):    def get(self):        user = None        if self.request.cookies.get('our_token'):    #the cookie that should contain the access token!            user = User.checkToken(self.request.cookies.get('our_token'))        if not user:            self.redirect("/")            return        email_list = User.getAllUsersEmail()        from google.appengine.api import mail        url = 'http://shiftssm.appspot.com'        for email in email_list:            user_address = "<" + email.email + ">"            sender_address = "SSM - Shift Submitter Support <ssmshift@shiftssm.appspotmail.com>"            subject = "New Schedule"            body = """New working schedule published, enter site to view it - """ + url            mail.send_mail(sender_address, user_address, subject, body)        self.response.write(json.dumps({'status': 'OK'}))class FourOFourHandler(webapp2.RequestHandler):    def get(self, args=None):        template_params = {}        html = template.render("web/templates/404.html", template_params)        self.response.write(html)app = webapp2.WSGIApplication([    ('/Admin', AdminHandler),    ('/Admin/schedulizeAtt', SchedulizeHandler),    ('/Admin/sendEmails', SendEmailsHandler),    ('/Admin/(.*)', FourOFourHandler)], debug=True)