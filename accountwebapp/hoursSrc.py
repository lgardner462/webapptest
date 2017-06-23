if (__name__ == "__main__"):
	print("Run webapp through wrapper.")
	print("Exiting...")
	exit()


#TO RUN FROM WRAPPER CLASSES:
# - csvInit(readerFile)
# - smtpInit(mailTo)
# - setClusterName(cname)
# - setDevMode(dmode)

import os
#import csv
import time
import smtplib
import sys
#import zipfile

#apache
os.chdir(os.path.dirname(__file__))
sys.path.insert(1, os.path.dirname(__file__))

from bottle import Bottle, route, run, request, response, template, static_file, default_app, redirect, SimpleTemplate, url, get, post

# Record class
from Record import Record


curTimeLong = time.strftime("%Y %b %d %X")
curTimeShort = time.strftime("%Y-%m-%d")

# for css reading in templates
SimpleTemplate.defaults["url"] = url

# directory for saving hours information
hoursDir = "hours"

### SMTP ###
sender = "root"

# sent to admins
subject = ""

# sent to user
userSubject = ""

# sent to user
userEmail =  ""


### SMTP ###############################################################################################

def smtpInit(mailTo):
	# this is called from the wrapper file
	# sets the admin email
	global receivers
	receivers = [mailTo]
### DEV MODE ###########################################################################################

def setDevMode(dmode):
	global devMode
	devMode = dmode
	print("DEV MODE: " + str(devMode))


# for css reading in templates
@route('/static/<filename>', name='static')
def server_static(filename):
    return static_file(filename, root='static')


########################################################################################################
######################################  	HOURS FORM START	 ###########################################
########################################################################################################
'''
$ <-- done

DONE:
	$ posting to hours should refresh the page with the updated information
	$ generate current date and duration
	maybe have the time be a time selection module if it exists
	$ ability to remove a record
	$ reusing the name if the record table exists
	$ add Y/N checkboxes for emergency, remote 

	NEXT THING:
	$ add up/down arrows to records
	$ learn to make dynamic dropdown fieldset for adding records in specific places
	$ automatically adjust times in subsequent records
	$ http://www.w3schools.com/bootstrap/tryit.asp?filename=trybs_navbar_collapse&stacked=h

	NEXT:
	$ finish passing parsedRecords into template
	$ wire template to access parsedRecords for filling in start/end times
	$ wire submit buttons to properly pass information back (figuring out how to insert a record in the middle of the list)
	plan:
		$ add current record to a list of records (split up into fields)
			$ the addition is based on which record's buttons were clicked on
		$ shift the time of everything after that point in the list by the duration amount of the new record
		$ ex: records = [[1, 10:00, 11:00, 1.0], [2, 11:00, 12:15, 1.25]]
			$ click on 1's down arrow...
			$ add [3, 11:00, 12:00, 1.0] // figure out ids or something
			$ records = [[1, 10:00, 11:00, 1.0], [3, 11:00, 12:00, 1.0], [2, 12:00, 13:15, 1.25]]

'''

'''
TODO: 
	$ distinguish between up/down arrows
		$ fill end time instead of start time for up arrow
	email records
	subtotal counter
		modified by adding/removing records
	reverse adjusting subsequent record times (on deletion)
		may just be a call to the same function but with passing in a negative duration (may also need to play around with indices)

	maybe: ability to drag and drop records into different order, if that's really wanted by sb

	maybe: field for retrieving existing record log (in case of browser closing, for example)
		may just require setting the name cookie and refreshing page (also hiding that field if successful)

	maybe fix accordion animation (now that it uses a custom js function for opening and closing)

	add time checks for splicing in a record
		if start time is before previous record's, then take time from previous
		if end time is after next record's, then take time from next

	move billable/emergency to the bottom of the form, since they are rarely changed

	fix hours routes
	  working on trying to splice in a record and adjusting the times of surrounding records
	  try to get code into functions and consistent
	  currently doesn't adjust other records' times

	might need to create functions:
		modifyStartTime
		modifyEndTime
			these can call modifyDuration or something

	look through any TODOs left over



	migrate to using Record class in src, template, etc.
	comment Record class
	continue with splicing in records, etc.
''' 


'''
NEXT:
	added New Record form in template
		organize and comment
	wire Record objects to template
		make sure duration adjustment works
		finish commenting Record methods
	maybe make the initial record form a different page to cut down on document size/redundancy

	finish organizing and splitting up templates
		bootlint
		variables and passing them to other templates

	then also finish doing css for templates, once it fully works

'''

########################################################################################################
########################################################################################################







########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################

@route('/hours')
def hours():
	#######################################################
	name = str(request.get_cookie("name"))
	start = str(request.get_cookie("start"))
	#######################################################

	# try to open file with user's name and retrieve data
	filePath = hoursDir + "/" + name
	# for each record, create a new Record object and add to list to pass to template
	# list of records as [obj]
	records = Record.parseRecordsFromFile(filePath)
	
	# DEBUG
	print("\n***DEBUG***")
	for r in records:
		print(r)
	print("***********\n")
	
	# if file doesn't exist, nullify cookies and proceed
	if not records:
		name = ""
		start = ""

	#######################################################
	return template('hours', records=records, name=name, start=start)


########################################################################################################
########################################################################################################
########################################################################################################

@route('/hours', method="POST")
def hours_post():
	
	#######################################################	
	# name of user
	name = request.forms.get("name").strip()
	
	# index for inserting new Record into the list of records
	index = int(request.forms.get("insert").strip())

	filePath = hoursDir + "/" + name

	#######################################################
	# parses form data and returns a Record obj
	new_record = Record.getRecordFromHTML(request)

	#######################################################

	# reads and parses Records on file
	records = Record.parseRecordsFromFile(filePath)

	#######################################################

	# if the cookie is set, the user has pulled any existing files
	# if there are no existing files, the cookie will be null
	records_pulled = request.get_cookie("name")

	if records and not records_pulled:
		# append to the end of unpulled existing records
		# prevents adding to the beginning of an unexpected list
		records.append(new_record)
		print("Appending to list")
	else:
		print("Inserting in list at index:", index)
		# insert new record at index provided from template form
		records.insert(index, new_record)
		Record.adjustAdjacentRecords(records, index)

	#for i in range(len(records)):
	#	Record.adjustAdjacentRecords(records, i)
	

	# write back updated list
	Record.writeRecords(filePath, records)
	#######################################################

	response.set_cookie("name", name)
	#response.set_cookie("start", end) # end of record becomes start of next record

	redirect('hours')


########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################











########################################################################################################
########################################################################################################
########################################################################################################

@route('/setName', method="POST")
def set_name():
	# get name of user provided in specified field
	name = request.forms.get("setName")

	# set name cookie
	response.set_cookie("name", name)

	# redirect to /hours to read file
	redirect('hours')


########################################################################################################
########################################################################################################

### deletes records of current user
@route('/delete', method="POST")
def delete_records():
	# get the name cookie
	name = request.get_cookie("name")
	if name:
		# delete the name cookie
		response.delete_cookie("name")
		# delete the user's record file
		os.system("rm -f hours/" + name)
	
	# redirect back to hours page
	redirect('hours')

########################################################################################################
########################################################################################################

### deletes a single record
@route('/deleteOne', method="POST")
def delete_single_record():

	# get w/o last char, since it comes in with a trailing '/'
	index = int(request.forms.get('recordIndex')[:-1])

	# get name cookie
	name = request.get_cookie("name")

	if name:
		filePath = hoursDir + "/" + name
		
		try:
			# read records
			f = open(filePath, 'r')
			records = f.read().split('\n')
			f.close()

			# delete record
			del records[index]
			#records = records[:index] + records[index+1:]

			if records:
				# write back records
				f = open(filePath, 'w')
				f.write('\n'.join(records))
				f.close()
			else:
				# if no records are left, delete the file
				os.system("rm -f " + filePath)

		except IOError:
			pass

	redirect('hours')

########################################################################################################
########################################################################################################

### emails records
@route('/email', method="POST")
def email_records():
	return("Under construction...")


########################################################################################################
######################################  	HOURS FORM END		 ###########################################
########################################################################################################

