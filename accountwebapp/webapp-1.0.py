#!/usr/bin/python

from bottle import route, run, request
import os


@route('/create_account')
def create_account():
	groups = ["darwin_projects",
			  "chill_projects",
			  "crebbi_projects",
			  "gcooperman_projects",
			  "guest",
			  "mit_general",
			  "pshenoy_projects"]	
	
	s= """
		<html>
		   <body>
			  <form action="/create_account" method="post" enctype="multipart/form-data">
			  	<fieldset style = "width:0px">
			  		<legend>Create Account</legend>
			  		Email: <br>
			  		<input type = "text" name = "email">
			  		<br><br>
			  		Group: <br>
			  		<select name = "group">\n
			  		"""
	
	for group in groups:
		s += "<option value= \"" + group + "\">" + group + "</option>\n"
		
	s += """	
					</select>
			  		<br><br>
			  		Public key: <br>
			  		<input type="file" name="key"/>
			  		<br><br><br>
			  		<input type = "submit" value = "Submit"/><br>
			  	</fieldset>
			  </form>
		   </body>
		</html>
		"""
	return s



@route('/create_account', method = 'POST')
def submit_info():
	s = ""
	email = request.forms.get('email')
	group = request.forms.get('group')
	key =   request.files.get('key')
	
	if email and key and '@' in email:
		os.mkdir(email)
		path = email + "/"
		name, ext = os.path.splitext(key.filename)
		key.save(path)
	
		f = open(path + "userInfo.txt", 'w')
		f.write(email + "\n" + group + "\n")
		f.close()
		s = "<p>Your email was submitted successfully!\n</p>"
				
	if email and '@' not in email:	
		s += "<p>Invalid email address.\n</p>"
	
	if not email:
		s += "<p>Missing email.\n</p>"
	
	if not key:
		s += "<p>Missing public key.\n</p>"
	
	
	return s


run(host='localhost', port=8081, debug=True)
