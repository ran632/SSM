from google.appengine.ext.webapp import template
import webapp2
import json
from web.pages.Index import *
from models.shift import Shift
from models.user import User
from models.submission import *
from models.staticfunctions import Staticfunctions
from datetime import *


class SwitchShiftsHandler(webapp2.RequestHandler):
    def get(self):
        user = None
        if self.request.cookies.get('our_token'):    #the cookie that should contain the access token!
                user = User.checkToken(self.request.cookies.get('our_token'))

        template_variables = {}
        if user:
            template_variables['user'] = user.email
            template_variables['userempno'] = user.employee_number
            if user.isAdmin:
                template_variables['useradmin'] = True
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

        allReq = Switch.allRequests()
        template_variables['requests'] = []
        for req in allReq:
            #check=======
            if req.status == 'pending':
                if req.from_shift_id:
                    from_shift = Shift.get_by_id(int(req.from_shift_id))
                    if from_shift == None or from_shift.employee_number != req.from_empno:
                        req.key.delete()
                        continue

                if req.to_shift_id:
                    to_shift = Shift.get_by_id(int(req.to_shift_id))
                    if to_shift == None or to_shift.employee_number != req.to_empno:
                        req.key.delete()
                        continue
            try:
                from_shift_str = Shift.shiftToString(Shift.get_by_id(int(req.from_shift_id)))
            except:
                from_shift_str = ""
            try:
                to_shift_str = Shift.shiftToString(Shift.get_by_id(int(req.to_shift_id)))
            except:
                to_shift_str = ""

            template_variables['requests'].append({
                "id": req.key.id(),
                "to_empno": req.to_empno,
                "from_empno": req.from_empno,
                "from_shift": from_shift_str,
                "to_shift": to_shift_str,
                "date": req.date,
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
        switch.date = datetime.utcnow() + timedelta(hours=3)
        switch.status = 'pending'
        switch.from_empno = user.employee_number
        switch.from_shift_id = from_shift_id
        switch.to_empno = to_empno
        switch.to_shift_id = to_shift_id
        switch.put()

        self.response.set_cookie('our_token', str(user.key.id()))
        self.response.write(json.dumps({'status': 'OK'}))

class SwitchAppHandler(webapp2.RequestHandler):
    def get(self):
        user = None
        if self.request.cookies.get('our_token'):    #the cookie that should contain the access token!
            user = User.checkToken(self.request.cookies.get('our_token'))
        if not user:
            self.redirect("/")
            return

        reqID = int(self.request.get('req_id'))
        req = Switch.get_by_id(reqID)


        if req.from_shift_id:
            from_shift = Shift.get_by_id(int(req.from_shift_id))
            print from_shift
            print from_shift.employee_number
            print req.from_empno
            if from_shift and from_shift.employee_number == req.from_empno:
                from_shift.employee_number = req.to_empno
                from_shift.put()

        if req.to_shift_id:
            to_shift = Shift.get_by_id(int(req.to_shift_id))
            print to_shift
            print to_shift.employee_number
            print req.to_empno
            if to_shift and to_shift.employee_number == req.to_empno:
                to_shift.employee_number = req.from_empno
                to_shift.put()

        req.status = 'approved'
        req.put()

        self.response.set_cookie('our_token', str(user.key.id()))
        self.response.write(json.dumps({'status': 'OK'}))

class SwitchDecHandler(webapp2.RequestHandler):
    def get(self):
        user = None
        if self.request.cookies.get('our_token'):    #the cookie that should contain the access token!
            user = User.checkToken(self.request.cookies.get('our_token'))
        if not user:
            self.redirect("/")
            return

        reqID = int(self.request.get('req_id'))
        req = Switch.get_by_id(reqID)
        req.status = 'declined'
        req.put()

        self.response.set_cookie('our_token', str(user.key.id()))
        self.response.write(json.dumps({'status': 'OK'}))

class SwitchRemHandler(webapp2.RequestHandler):
    def get(self):
        user = None
        if self.request.cookies.get('our_token'):    #the cookie that should contain the access token!
            user = User.checkToken(self.request.cookies.get('our_token'))
        if not user:
            self.redirect("/")
            return

        reqID = int(self.request.get('req_id'))
        req = Switch.get_by_id(reqID)
        req.key.delete()

        self.response.set_cookie('our_token', str(user.key.id()))
        self.response.write(json.dumps({'status': 'OK'}))


class FourOFourHandler(webapp2.RequestHandler):
    def get(self, args=None):
        template_params = {}
        html = template.render("web/templates/404.html", template_params)
        self.response.write(html)


app = webapp2.WSGIApplication([
	('/SwitchShifts', SwitchShiftsHandler),
    ('/SwitchShifts/switchAtt', SwitchAttHandler),
    ('/SwitchShifts/switchApproved', SwitchAppHandler),
    ('/SwitchShifts/switchDeclined', SwitchDecHandler),
    ('/SwitchShifts/switchRemove', SwitchRemHandler),
	('/SwitchShifts/(.*)', FourOFourHandler)
	

], debug=True)
