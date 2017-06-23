#!/usr/bin/python

if (__name__=="__main__"):
	print("Run webapp through wrapper.")
	print("Exiting...")
	exit()

#TO RUN FROM WRAPPER CLASSES:
# - csvInit(readerFile)
# - smtpInit(mailTo)
# - setClusterName(cname)
# - setDevMode(dmode)

import os
import csv
import time
import smtplib
import sys
import zipfile

#apache
os.chdir(os.path.dirname(__file__))
sys.path.insert(1, os.path.dirname(__file__))

from bottle import Bottle, route, run, request, response, template, static_file, default_app, redirect, SimpleTemplate, url

# for css reading in templates
SimpleTemplate.defaults["url"] = url

### EXPLICITLY GLOBAL VARS #############################################################################

### CSV ###
nameLocZipped = {}
nameMacZipped = {}
nameCSVZipped = {}

### SMTP ###
receivers = []

### GROUPS ### (implicit)
groupsList = []
groupsDict = {}

### GLOBAL CONSTANTS ###################################################################################

# if true, disables sending mail to other receivers 
devMode = False # set in httpd.py

# used for the name of the downloaded zip file containing generated keys
clusterName = "cluster" # placeholder to avoid missing variable

# directory for saving new account information
usersDir = "newaccounts"
nackDir = "denyaccounts"

# name of file supplying group information
groupsFilePath = "groups.txt"
# number of group fields in ack_accounts
NUM_GROUP_FIELDS = 3

# current time
curTimeLong = time.strftime("%Y %b %d %X")
curTimeShort = time.strftime("%Y-%m-%d")

### SMTP ###
sender = "root"

# sent to admins
subject = "User has requested account - " + curTimeShort

# sent to user
userSubject = "You have requested an account - " + curTimeShort

# sent to user
userEmail =  """
Thank you for your account request.
Please note that this is *not* an automatic process.
Account requests may take 2 school days to process.
"""

### CSV ################################################################################################

def csvInit(readerFile):
	# 1 - reads from csv file (supplied in wrapper file)
	# 2 - parses data into lists
	# 3 - creates dictionaries from lists (dicts are GLOBAL)
	try:
		global nameLocZipped
		global nameMacZipped
		global nameCSVZipped

		# 1 #
		reader = open(readerFile)

		reader.readline()
		reader.readline()

		#Initialize Lists
		csvFull = []
		nodeNames = []
		nodeLoc = []
		nodeMac = []

		#ROW CONSTANTS
		NAME = 0
		LOC = 1
		MAC = -1 

		# 2 # lists: full, name, loc, mac
		for row in reader:
			if (".xml" not in row): #removes invalid lines that contain ".xml"
				csvFull.append(row)

				rowSplit = row.split(',')

				nodeNames.append(rowSplit[NAME])
				nodeLoc.append(rowSplit[LOC])

				mac = rowSplit[MAC]
				mac = mac.translate(None, "[]\\u\'") #deletes chars
				nodeMac.append(mac)

		# 3 # dicts: name --> nodeLoc, nodeMac, csvFull
		nameLocZipped = dict(zip(nodeNames,nodeLoc))
		nameMacZipped = dict(zip(nodeNames,nodeMac))
		nameCSVZipped = dict(zip(nodeNames,csvFull))

		reader.close()

	except IOError:
		print("Error: CSV file missing.\n")
		exit()

### end csvInit() ###

#IF YOU NEED TO ACCESS A VAR *FROM THIS* FILE IN A WRAPPER FILE, USE RETURN VALUE:
#def test():
#	global nameCSVZipped
	#print "$$$:", nameCSVZipped
#	return nameCSVZipped

### SMTP ###############################################################################################

def smtpInit(mailTo):
	# this is called from the wrapper file
	# sets the admin email
	global receivers
	receivers = [mailTo]

### CLUSTER NAME #######################################################################################

def setClusterName(cname):
	global clusterName
	clusterName = cname
	print("CLUSTER: " + clusterName)

### DEV MODE ###########################################################################################

def setDevMode(dmode):
	global devMode
	devMode = dmode
	print("DEV MODE: " + str(devMode))

### GROUPS #############################################################################################
# 1 - reads from local file
# 2 - parses data into list and dict global vars

try:
	g = open(groupsFilePath, 'r')
	tempGroups = g.read().split("\n")
	
	for pair in tempGroups:
		if(pair):
			tempPair = pair.split(" -- ")
			groupsList.append(tempPair[0]) #for populating drop down list
			groupsDict[tempPair[0]] = tempPair[1] #for getting appropriate real group name

	g.close()

except IOError:
	print "Error: groups file missing.\n"
	exit()























########################################################################################################
################################################ ROUTES ################################################
########################################################################################################

# for css reading in templates
@route('/static/<filename>', name='static')
def server_static(filename):
    return static_file(filename, root='static')

########################################################################################################
############################################ REQUEST ACCOUNT ###########################################

# deprecated
@route('/create_account')
def create_account():
	redirect('/request_account')

########################################################################################################
########################################################################################################

@route('/request_account')
def request_account():
	return template("request_account", groupsList = groupsList)

@route('/request_account_beta')
def request_account():
	return template("request_account_beta", groupsList = groupsList)

########################################################################################################
########################################################################################################

@route('/request_account', method = 'POST')
def submit_info():
	
	######
	name = request.forms.get('name').strip()
	nameAff = request.forms.get('nameAffiliation').strip()

	sponsor = request.forms.get('sponsor').strip()
	sponsorAff = request.forms.get('sponsorAffiliation').strip()

	email = request.forms.get('email').strip().lower()
	phone = request.forms.get('phone').strip()
	
	username = request.forms.get('username').strip().lower()
	group = groupsDict[request.forms.get('group')]
	
	projectDescription = request.forms.get('projectDescription').strip()
	######

	curUserDir = usersDir + "/" + email + "/"

	keyChoice = request.forms['keyChoice']
	keyName = username + "_id_rsa"
	keyPath = curUserDir + keyName
	key = ""

	pass1 = ""
	pass2 = ""

	errors = []

########################################################################################################

	if keyChoice == "upload":
		key = request.files.get('key')
		
		try:
			key.save("/tmp/")
		except IOError:
			pass
		
		keyFilename = "/tmp/" + key.filename

		#check key: 0 == public, non-0 == private
		keyIsPrivate = os.system("ssh-keygen -lf " + keyFilename)
		
		if(keyIsPrivate):
			#openssh - needed for Windows PuTTy user keys
			opensshKeyFilename = "/tmp/openssh_" + key.filename #key.filename w/o /tmp/

			#openssh - converts key //needed for Windows PuTTy user keys
			os.system("ssh-keygen -if " + keyFilename + " > " + opensshKeyFilename)
			
			#openssh - check key: 0 == public, non-0 == private //same test
			opensshIsPrivate = os.system("ssh-keygen -lf " + opensshKeyFilename)
			
			#result of testing the key twice
			if(opensshIsPrivate):
				errors.append("privateKey")
			
			os.system("rm " + opensshKeyFilename)

		os.system("rm " + keyFilename)
	
	if keyChoice == "generate":
		pass1 = request.forms.get('pass1')
		pass2 = request.forms.get('pass2')

########################################################################################################

	if not name:
		errors.append("name")

	if not nameAff:
		errors.append("nameAff")

	if not sponsor:
		errors.append("sponsor")

	if not sponsorAff:
		errors.append("sponsorAff")	

	if not email or '@' not in email:
		errors.append("email")

	if not phone:
		errors.append("phone")

	if not projectDescription:
		errors.append("projectDescription")

        if keyChoice == "upload" and not key:
		errors.append("missingKey")

	if keyChoice == "generate":
	        if(not pass2 or not pass1):
			errors.append("password")
	
	        if(pass1 != pass2):
			errors.append("passwordMatch")
	
	        if(pass1 and pass2 and pass1 == pass2 and len(pass1) < 4):
			errors.append("passwordLength")
	
#######################################################################################################
	
	if not errors:
		if(not os.path.isdir(usersDir)): # newaccounts
			os.mkdir(usersDir)

                if(not os.path.isdir(nackDir)): # denyaccounts
                        os.mkdir(nackDir)
			
		if(not os.path.isdir(curUserDir)):
			os.mkdir(curUserDir)
			
#######################################################################################################
		
		if keyChoice == "upload":	
			keyName, keyExt = os.path.splitext(key.filename)
			
			try:
				key.save(curUserDir)
			except IOError:
				pass				

			#key - upload
			f = open(curUserDir + "keys.txt", 'a')
			f.write(keyName + keyExt + "\n")
			f.close()
							
#######################################################################################################

		if keyChoice == "generate":
			if(os.path.exists(keyPath)):
				os.system("rm " + keyPath)

			if(os.path.exists(keyPath + ".pub")):
				os.system("rm " + keyPath + ".pub")
	
			os.system("ssh-keygen -N " + pass2 + " -t rsa -f " + keyPath + " -C " + email)

			#key - generate
			f = open(curUserDir + "keys.txt", 'a')
			f.write(keyName + ".pub" + "\n")
			f.close()

#######################################################################################################	
		
		# RESET TIME WHEN USER SUCCESSFULLY MAKES AN ACCOUNT
		curTimeLong = time.strftime("%Y %b %d %X")
		curTimeShort = time.strftime("%Y-%m-%d")

#######################################################################################################	

		#name/nameAff
		f = open(curUserDir + "name.txt", 'w')
		f.write(name + "\n")
		f.write(nameAff + "\n")
		f.close()

		#sponsor/sponsorAff
		f = open(curUserDir + "sponsor.txt", 'w')
		f.write(sponsor + "\n")
		f.write(sponsorAff + "\n")
		f.close()

		#group
		f = open(curUserDir + "groups.txt", 'w')
		f.write(group + "\n")
		f.close()
		
		#projectDescription
		f = open(curUserDir + "projectDescription.txt", 'w')
		f.write(projectDescription + "\n")
		f.close()

		#username
		f = open(curUserDir + "username.txt", 'w')
		f.write(username + "\n")
		f.close()
		
		#phone
		f = open(curUserDir + "phone.txt", 'w')
		f.write(phone + "\n")
		f.close()

		
		#ACK_INFO - USED FOR ack_accounts PAGE
		f = open(curUserDir + "ACK_INFO.txt", 'w')	
		f.write(curTimeShort + "\n")
		f.write(email + "\n")
		f.write(group + "\n")
		f.write(phone + "\n")
		f.write(sponsor + "\n")
		f.write(sponsorAff + "\n")
		f.write(projectDescription)
		f.close()

#######################################################################################################
### Email sent to admins
		
		body = curTimeLong + "\n\n" + email + "\n" + group

		message = "Subject: %s\n\n%s" % (subject, body)

		try:
			mail = smtplib.SMTP("localhost")
			mail.sendmail(sender, receivers, message)
			mail.quit()

		except smtplib.SMTPException:
			print "Error: could not send email to admin.\n"
			exit()

#######################################################################################################
### Email sent to user

		body = curTimeLong + "\n" + userEmail

		message = "Subject: %s\n\n%s" % (userSubject, body)

		try:
			mail = smtplib.SMTP("localhost")
			mail.sendmail(sender, [email], message)
			mail.quit()

		except smtplib.SMTPException:
			print "Error: could not send email to user.\n"
			exit()

	
#######################################################################################################
		
	return template("post_account", errors=errors, keyChoice=keyChoice, keyPath=keyPath)

#######################################################################################################
########################################## BETA ROUTE #################################################
#######################################################################################################

@route('/request_account_beta', method = 'POST')
def submit_info():
	
	######
	name = request.forms.get('name').strip()
	nameAff = request.forms.get('nameAffiliation').strip()

	sponsor = request.forms.get('sponsor').strip()
	sponsorAff = request.forms.get('sponsorAffiliation').strip()

	email = request.forms.get('email').strip().lower()
	phone = request.forms.get('phone').strip()
	
	username = request.forms.get('username').strip().lower()
	# currently only one group is picked by the user
	groups = groupsDict[request.forms.get('group')]
	
	projectDescription = request.forms.get('projectDescription').strip()
	######

	curUserDir = usersDir + "/" + email + "/"

	keyChoice = request.forms['keyChoice']
	keyName = username + "_id_rsa"
	keyPath = curUserDir + keyName
	key = ""

	# converted from id_rsa key (when generating a key)
	puttyKeyName = username + "_private.ppk"
	puttyKeyPath = curUserDir + puttyKeyName

	# archive for the keys
	keyZipName = username + "_keys.zip"
	keyZipPath = curUserDir + keyZipName

	pass1 = ""
	pass2 = ""

	errors = []

########################################################################################################

	if keyChoice == "upload":
		key = request.files.get('key')
		
		try:
			key.save("/tmp/")
		except IOError:
			pass
		
		keyFilename = "/tmp/" + key.filename

		#check key: 0 == public, non-0 == private
		keyIsPrivate = os.system("ssh-keygen -lf " + keyFilename)
		
		if(keyIsPrivate):
			#openssh - needed for Windows PuTTy user keys
			opensshKeyFilename = "/tmp/openssh_" + key.filename #key.filename w/o /tmp/

			#openssh - converts key //needed for Windows PuTTy user keys
			os.system("ssh-keygen -if " + keyFilename + " > " + opensshKeyFilename)
			
			#openssh - check key: 0 == public, non-0 == private //same test
			opensshIsPrivate = os.system("ssh-keygen -lf " + opensshKeyFilename)
			
			#result of testing the key twice
			if(opensshIsPrivate):
				errors.append("privateKey")
			
			os.system("rm -f " + opensshKeyFilename)

		os.system("rm -f " + keyFilename)
	
	if keyChoice == "generate":
		pass1 = request.forms.get('pass1')
		pass2 = request.forms.get('pass2')

########################################################################################################

	if not name:
		errors.append("name")

	if not nameAff:
		errors.append("nameAff")

	if not sponsor:
		errors.append("sponsor")

	if not sponsorAff:
		errors.append("sponsorAff")	

	if not email or '@' not in email:
		errors.append("email")

	if not phone:
		errors.append("phone")

	if not projectDescription:
		errors.append("projectDescription")

        if keyChoice == "upload" and not key:
		errors.append("missingKey")

	if keyChoice == "generate":
	        if(not pass2 or not pass1):
			errors.append("password")
	
	        if(pass1 != pass2):
			errors.append("passwordMatch")
	
	        if(pass1 and pass2 and pass1 == pass2 and len(pass1) < 4):
			errors.append("passwordLength")
	
#######################################################################################################
	
	if not errors:
		if(not os.path.isdir(usersDir)): # newaccounts
			os.mkdir(usersDir)

                if(not os.path.isdir(nackDir)): # denyaccounts
                        os.mkdir(nackDir)
			
		if(not os.path.isdir(curUserDir)):
			os.mkdir(curUserDir)
			
#######################################################################################################
		
		if keyChoice == "upload":	
			keyName, keyExt = os.path.splitext(key.filename)
			
			try:
				key.save(curUserDir)
			except IOError:
				pass				

			#key - upload
			f = open(curUserDir + "keys.txt", 'a')
			f.write(keyName + keyExt + "\n")
			f.close()
							
#######################################################################################################

		if keyChoice == "generate":
			# remove prior private key
			if(os.path.exists(keyPath)):
				os.system("rm -f " + keyPath)

			# remove prior public key
			if(os.path.exists(keyPath + ".pub")):
				os.system("rm -f " + keyPath + ".pub")

			# remove prior PuTTy key
			if(os.path.exists(puttyKeyPath)):
				os.system("rm -f " + puttyKeyPath)
			
			# generate new key
			os.system("ssh-keygen -N " + pass2 + " -t rsa -f " + keyPath + " -C " + email)

			# convert private key to PuTTy ppk format via Expect script
			os.system("./convert_to_ppk.sh " + keyPath + " " + puttyKeyPath + " " + pass2)

			# add three files to zip archive: both id_rsa keys and ppk key
			# cd to current user directory; after this os command, it returns to the directory of this file
			os.system("cd " + curUserDir + " ; zip " + keyZipName + " " + keyName + " " + keyName + ".pub " + puttyKeyName)

			# delete id_rsa and private.ppk (only id_rsa.pub remains)
			os.system("rm -f " + keyPath + " " + puttyKeyPath)

			# record name of public key (username_id_rsa.pub)
			f = open(curUserDir + "keys.txt", 'a')
			f.write(keyName + ".pub" + "\n")
			f.close()

#######################################################################################################	
		
		# RESET TIME WHEN USER SUCCESSFULLY MAKES AN ACCOUNT
		curTimeLong = time.strftime("%Y %b %d %X")
		curTimeShort = time.strftime("%Y-%m-%d")

#######################################################################################################	

		#name/nameAff
		f = open(curUserDir + "name.txt", 'w')
		f.write(name + "\n")
		f.write(nameAff + "\n")
		f.close()

		#sponsor/sponsorAff
		f = open(curUserDir + "sponsor.txt", 'w')
		f.write(sponsor + "\n")
		f.write(sponsorAff + "\n")
		f.close()

		#groups
		f = open(curUserDir + "groups.txt", 'w')
		f.write(groups + "\n")
		f.close()
		
		#projectDescription
		f = open(curUserDir + "projectDescription.txt", 'w')
		f.write(projectDescription + "\n")
		f.close()

		#username
		f = open(curUserDir + "username.txt", 'w')
		f.write(username + "\n")
		f.close()
		
		#phone
		f = open(curUserDir + "phone.txt", 'w')
		f.write(phone + "\n")
		f.close()

		
		#ACK_INFO - USED FOR ack_accounts PAGE
		f = open(curUserDir + "ACK_INFO.txt", 'w')	
		f.write(curTimeShort + "\n")
		f.write(email + "\n")
		f.write(groups + "\n")
		f.write(phone + "\n")
		f.write(sponsor + "\n")
		f.write(sponsorAff + "\n")
		f.write(projectDescription)
		f.close()

#######################################################################################################
### Email sent to admins
		
		body = curTimeLong + "\n\n" + email + "\n" + groups

		message = "Subject: %s\n\n%s" % (subject, body)

		try:
			mail = smtplib.SMTP("localhost")
			mail.sendmail(sender, receivers, message)
			mail.quit()

		except smtplib.SMTPException:
			print "Error: could not send email to admin.\n"
			exit()

#######################################################################################################
### Email sent to user

		body = curTimeLong + "\n" + userEmail

		message = "Subject: %s\n\n%s" % (userSubject, body)

		try:
			mail = smtplib.SMTP("localhost")
			mail.sendmail(sender, [email], message)
			mail.quit()

		except smtplib.SMTPException:
			print "Error: could not send email to user.\n"
			exit()

	
#######################################################################################################
		
	return template("post_account_beta", errors=errors, keyChoice=keyChoice, keyZipPath=keyZipPath, clusterName=clusterName)

########################################################################################################
########################################################################################################

@route('/id_rsa', method = 'POST')
def download_key():

	response.content_type = 'application/ssh'

	keyPath = request.forms.get('keyPath')

	privateKey = ""
	try:
		f = open(keyPath)
		privateKey = f.read()
		f.close()
	
	except IOError:
		pass
	
	if(os.path.exists(keyPath)):
		os.system("rm " + keyPath)

	return privateKey


###### BETA #############
@route('/<clusterName>', method = 'POST')
def download_key(clusterName):
	# clusterName variable not further referenced, but needed here for the route initialization
	response.content_type = 'application/zip'

	keyZipPath = request.forms.get('keyZipPath')

	zipFileString = ""
	
	try:
		f = open(keyZipPath)
		zipFileString = f.read()
		f.close()
	
	except IOError:
		pass
	
	if(os.path.exists(keyZipPath)):
		os.system("rm -f " + keyZipPath)

	return zipFileString


########################################################################################################
############################################## ACK ACCOUNT #############################################

@route('/ack_account')
def ack_account():
	# AS IT STANDS: webapp/newaccounts/ must exist (and owned by apache for wsgi wrapper)
	tempList = next(os.walk(usersDir))[1] # this will error if newaccounts/ doesn't exist
 
	usersList = [] #accounts to be ACKed
	ackList = [] #accounts already ACKed
	userCount = -1

        acked = False #boolean for tracking if account has been ACKcked

	for user in tempList:
                curUserDir = usersDir + "/" + user

		#accounts that have been acknowledged will have "ack" file
		if(os.path.isfile(curUserDir + "/ack")):
			acked = True
		if(acked):
			ackList.append([])
                else:
			usersList.append([])
		
		++userCount

		f = open(curUserDir + "/ACK_INFO.txt", 'r')		
		info = f.readlines()		
	
		for line in info:
			if(acked):
				ackList[userCount].append(line)
                        else:
				usersList[userCount].append(line)
				
		f.close()

		acked = False

	return template("ack_account", usersList=usersList, ackList=ackList, groupsList=groupsList, groupsDict=groupsDict)

########################################################################################################
################################### ACK ACCOUNT BETA ###################################################
@route('/ack_account_beta')
def ack_account_beta():
	# AS IT STANDS: webapp/newaccounts/ must exist (and owned by apache for wsgi wrapper)
	tempList = next(os.walk(usersDir))[1] # this will error if newaccounts/ doesn't exist
 
	usersList = [] #accounts to be ACKed
	ackList = [] #accounts already ACKed
	userCount = -1

        acked = False #boolean for tracking if account has been ACKcked

	for user in tempList:
                curUserDir = usersDir + "/" + user

		#accounts that have been acknowledged will have "ack" file
		if(os.path.isfile(curUserDir + "/ack")):
			acked = True
		if(acked):
			ackList.append([])
                else:
			usersList.append([])
		
		++userCount

		f = open(curUserDir + "/ACK_INFO.txt", 'r')		
		info = f.readlines()		
	
		for line in info:
			if(acked):
				ackList[userCount].append(line)
                        else:
				usersList[userCount].append(line)
				
		f.close()

		acked = False

	return template("ack_account_beta", usersList=usersList, ackList=ackList, groupsList = groupsList, groupsDict = groupsDict)

########################################################################################################
################################### ACK ACCOUNT POST ###################################################

@route('/ack_account', method = 'POST')
def ack_account():
	# for template
	chgroupDict = {}
	ackList = []
	nackList = []

	#check all pending users for change in group
	tempList = next(os.walk(usersDir))[1] 

	for user in tempList:
		curUserDir = usersDir + "/" + user.strip()

		userGroupFilePath = curUserDir + "/groups.txt"
		userAckFilePath = curUserDir + "/ACK_INFO.txt"	

		f = open(userGroupFilePath, 'r')
		oldGroup = f.read().strip()
		f.close()

		newGroupDisplayName = request.forms.get(user)
		newGroup = groupsDict[newGroupDisplayName]

		if newGroup != oldGroup:
			chgroupDict[user.strip()] = newGroupDisplayName ### into template

			#recreate groups.txt file with new group
			f = open(userGroupFilePath, 'w')
			f.write(newGroup + "\n")
			f.close()

			#recreate ACK_INFO.txt file with new group
			f = open(userAckFilePath, 'r')
			ackFields = f.read().split()
			f.close()

			f = open(userAckFilePath, 'w')
			for field in ackFields:
				if field == oldGroup:
					f.write(newGroup + "\n")
				else:
					f.write(field + "\n")
					f.close()

		###################### determine action on each user: ACK, DENY, none
		action = request.forms.get("action" + user)
		if action == "ACK":
			print("ACK ACHIEVED")
			os.system("touch " + curUserDir + "/ack")
        	ackList.append(user.strip()) ### into template
        elif action == "DENY":
        	print("DENY ACHIEVED")                                     
        	os.system("mv " + curUserDir + " " + nackDir)
            nackList.append(user.strip()) ### into template

	#run pending-accounts script every time accounts are acked
	for address in receivers:
		os.system("./pending-accounts -m " + address)

	# QUICK FIX: LIST OF OTHER RECEIVERS
	if not devMode: # toggle at the beginning of the file
	os.system("./pending-accounts -m rchelp-dev@mit.edu")

	return template('ack_post_account', chgroupDict=chgroupDict, ackList=ackList, nackList=nackList)


########################################################################################################
##################################### ACK ACCOUNT (POST) BETA ##########################################

@route('/ack_account_beta', method = 'POST')
def ack_account_beta():
    # for template
    chgroupDict = {}
    ackList = []
    nackList = []

	#check all pending users for change in group
	tempList = next(os.walk(usersDir))[1] 

	for user in tempList:
		curUserDir = usersDir + "/" + user.strip()

		userGroupFilePath = curUserDir + "/groups.txt"
		userAckFilePath = curUserDir + "/ACK_INFO.txt"	

		f = open(userGroupFilePath, 'r')
		oldGroups = f.read().split(" ").strip()
		while len(oldGroups) < NUM_GROUP_FIELDS:
			oldGroups.append("")
			f.close()

			newGroupsRealNames = []
		# for each (of the 3) groups
		for i in range(NUM_GROUP_FIELDS):
			displayName = "G" + str(i) + user
			# get group name
			group = request.forms.get(displayName)
			# if it is in dict (!= "--")
			if group in groupsDict:
				# get real name 
				newGroup = groupsDict[group]
			else:
				newGroup = ""

				newGroupsRealNames.append(newGroup)

				for i in range(NUM_GROUP_FIELDS):
					if newGroupsRealNames[i] != oldGroups[i]:
			chgroupDict[user.strip()] = newGroupsRealNames ### into template

			#recreate groups.txt file with new group
			f = open(userGroupFilePath, 'w')
			f.write(newGroupsRealNames.join("\n") + "\n")
			f.close()

			#recreate ACK_INFO.txt file with new group
			f = open(userAckFilePath, 'r')
			ackFields = f.read().split()
			f.close()

			f = open(userAckFilePath, 'w')
			for field in ackFields:
				if field == oldGroups.join(" "):
					f.write(newGroupsRealNames.join(" ") + "\n")
				else:
					f.write(field + "\n")
					f.close()

		###################### determine action on each user: ACK, DENY, none
		action = request.forms.get("action" + user)
		if action == "ACK":
			print("ACK ACHIEVED")
			os.system("touch " + curUserDir + "/ack")
			ackList.append(user.strip()) ### into template
		elif action == "DENY":
			print("DENY ACHIEVED")                                     
			os.system("mv " + curUserDir + " " + nackDir)
            nackList.append(user.strip()) ### into template

	#run pending-accounts script every time accounts are acked
	for address in receivers:
		os.system("./pending-accounts -m " + address)

	# QUICK FIX: LIST OF OTHER RECEIVERS
	if not devMode: # toggle at the beginning of the file or in httpd.py
	os.system("./pending-accounts -m rchelp-dev@mit.edu")

	return template('ack_post_account', chgroupDict=chgroupDict, ackList=ackList, nackList=nackList)



########################################################################################################
################################################## CSV #################################################

#Top page
@route('/top')
def top():	
	return template('top1', nameCSVZipped=nameCSVZipped)

#Routes to designated node's info
@route('/node<no>')
def index(no):
	data = nameCSVZipped['node'+str(no)]
	return template('nodepage', no=no, data=data)

#Shows rack location for all nodes	
@route('/showrack')
def showrack():
	return template('showrack',nameLocZipped=nameLocZipped)

#Show mac address for all notes
@route('/showmac')
def showmac():
	return template('showmac',nameMacZipped=nameMacZipped)

#Downloads csv file
@route('/download<filename:path>')
def download(filename):
	return static_file(filename, root = os.path.dirname(__file__),download=filename)

########################################################################################################
########################################################################################################
