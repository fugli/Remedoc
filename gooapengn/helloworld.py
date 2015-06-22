import webapp2
# import webaap
from google.appengine.ext import db
from google.appengine.api import users


html = """ <html>
            <body>
              <form action="/sign" method="post">
                
                Firstname: <input name = "fname" type = "text" value="Prince"><br>
                Lastname : <input name = "lname" type = "text" value = "kumar"> <br><br>
                
                desc urself in brief :<div><textarea name="content" rows="1" cols="60"></textarea></div>
                <div><input type="submit" value="Sign Guestbook"></div>
              </form>
            </body>
          </html>"""


def guestdirec_key (guestname=None):


class MainPage(webapp2.RequestHandler):
    def get(self):
    	user1 = users.get_current_user()
    	if user1:
    		self.response.out.write("hellloo"+user1.nickname())
    	else:
    		a=self.request.uri
    		self.redirect(users.create_login_url(a))
        # self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(html)
	   		# a=self.request.uri
	    	# users.create_login_url(a)
    	# self.redirect(users.create_login_url(self.request.uri))

class Guestbook(webapp2.RequestHandler):
	def post(self):   #on submitting the form post mesthod is called
		self.response.out.write('<html><body>about u <br> </body></html>')
		About = self.request.get('content')
		Fname = self.request.get('fname')
		Lname = self.request.get('lname')

		# self.response.out.write('<html><body>'+Fname+' '+Lname+'<br>'+ About +'<br> </body></html>')
		self.response.out.write('<html><body>%s<br> %s <br> %s <br> </body></html>'%(Fname,Lname,About))

		guestname = self.request.get()





app = webapp2.WSGIApplication([
    ('/', MainPage),('/sign', Guestbook)
], debug=True)
# print type(app)
def main():
    appl.run()