#from google.appengine.api import users
from google.appengine.ext.webapp import template


import webapp2

class FourOFourHandler(webapp2.RequestHandler):
	#we provide args=None becuase that's how webapp2 treats the (.*) in /(.*)
	def get(self, args=None):
		template_params = {}
					
		html = template.render("web/templates/404.html", template_params)
		self.response.write(html)

app = webapp2.WSGIApplication([
	('/(.*)', FourOFourHandler)
], debug=True)
