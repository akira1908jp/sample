import webapp2
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequesHandler):
	def get(self):
		user = users.get_current_user();

		if user:
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.our.write('Hello,' + user.nickname())
		else:
			self.redirect.(user.create_login_url(self.request.url))

application = webapp.WSGIApplication(
                                     [('/hello', MainPage)],
                                     debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()