<html>
	<head>
		<style type="text/css">
			.fieldset-auto-width
			{
				display: inline-block;
    			}
			p
			{
				font-size: 0.85em;
			}
		</style>
	</head>
	
	<body>
		<script type="text/javascript">
                        
function checkEmail(affectField)
{
	if(typeof(affectField)==='undefined') affectField = true;

	var email = document.getElementById('email');
	var message = document.getElementById('emailMessage');
   
	var defaultColor = "#ffffff"; 
	var goodColor = "#66cc66";
	var badColor = "#ff6666";
	var testresults = false;

	var filter=/^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
	if (filter.test(email.value))
	{
		testresults=true;
		if(affectField)
		{
			email.style.backgroundColor = goodColor;
			emailMessage.innerHTML = "";
		}
	}
	else if(email.value != "")
	{
		testresults=false;
		if(affectField)
		{
			email.style.backgroundColor = badColor;
			emailMessage.style.color = badColor;
			emailMessage.innerHTML = "Invalid email.";
		}
	}
	else
	{
		testresults = false;
		email.style.backgroundColor = defaultColor;
		emailMessage.innerHTML = "";
	}

	return (testresults);
}


function checkPhone(affectField)
{
	if(typeof(affectField)==='undefined') affectField = true;

	var phone = document.getElementById('phone');
	var message = document.getElementById('phoneMessage');

	var defaultColor = "#ffffff"; 
	var goodColor = "#66cc66";
	var badColor = "#ff6666";
	var testresults = false;

	var filter=/^[(]{0,1}[0-9]{3}[)]{0,1}[-\s\.]{0,1}[0-9]{3}[-\s\.]{0,1}[0-9]{4}$/;
	if (filter.test(phone.value))
	{
		testresults=true;
		if(affectField)
		{
			phone.style.backgroundColor = goodColor;
			phoneMessage.innerHTML = "";
		}
	}
	else if(phone.value != "")
	{
		testresults=false;
		if(affectField)
		{
			phone.style.backgroundColor = badColor;
			phoneMessage.style.color = badColor;
			phoneMessage.innerHTML = "Invalid phone.";
		}
	}
	else
	{
		testresults = false;
		phone.style.backgroundColor = defaultColor;
		phoneMessage.innerHTML = "";
	}

	return (testresults);
}


function checkPass(affectField)
{
	if(typeof(affectField)==='undefined') affectField = true;
	var testresults = false;

	//Store the password field objects into variables
	var pass1 = document.getElementById('pass1');
	var pass2 = document.getElementById('pass2'); 
	var submit = document.getElementById('submit');

	//Store the Confimation Message Object 
	var message = document.getElementById('passwordMessage');
	var submit = document.getElementById('submit');

	//Set the colors we will be using
	var defaultColor = "#ffffff"; 
	var goodColor = "#66cc66";
	var badColor = "#ff6666";

	//Compare the values in the password field and the confirmation field
	if(pass1.value == pass2.value && pass1.value.length > 4)
	{
		testresults = true;
		if(affectField)
		{        
			pass1.style.backgroundColor = goodColor;
			pass2.style.backgroundColor = goodColor;
			message.style.color = goodColor;
			message.innerHTML = "Passwords match.";
	
			if(checkEmail(false) && checkPhone(false))
			{	
				submit.disabled = false;
			}
			else
			{
				submit.disabled = true;
			}
		}
	}
	else if(pass1.value == "" && pass2.value == "")
	{
		testresults = false;
		submit.disabled = true;
		pass1.style.backgroundColor = defaultColor;
		pass2.style.backgroundColor = defaultColor;
		message.innerHTML = "";
	}
	else if(pass1.value.length <= 4)
	{
		testresults = false;
		submit.disabled = true;
		if(affectField)
		{	
			pass1.style.backgroundColor = badColor;
			pass2.style.backgroundColor = badColor;
			message.style.color = badColor;
			message.innerHTML = "Password must be greater than four characters.";    
		}
	}
	else
	{
		testresults = false;
		submit.disabled = true;
		if(affectField)
		{        
			pass1.style.backgroundColor = badColor;
			pass2.style.backgroundColor = badColor;
			message.style.color = badColor;
			message.innerHTML = "Passwords do not match.";
		}
	}

	return (testresults);
}



function checkFields()
{
	var submit = document.getElementById('submit');
	var keyChoice = document.querySelector('input[name = "keyChoice"]:checked').value;

	if(checkEmail(false) && checkPhone(false) && (keyChoice == "upload" || checkPass(false)))
	{
		submit.disabled = false;
	}
	else
	{
		submit.disabled = true;
	}
	return;
}



function uploadButton()
{ 
	var pass1 = document.getElementById('pass1');
	var pass2 = document.getElementById('pass2');
	var message = document.getElementById('passwordMessage');

	document.getElementById('keyButton').disabled = false;
	document.getElementById('keyButton').required = true;

	pass1.disabled = true;
	pass2.disabled = true;
	var defaultColor = "#ffffff"; 
	pass1.style.backgroundColor = defaultColor;
	pass2.style.backgroundColor = defaultColor;
	message.innerHTML = "";
}


function generateButton()
{
	document.getElementById('pass1').disabled = false;
	document.getElementById('pass2').disabled = false;
	document.getElementById('keyButton').disabled = true;
	document.getElementById('keyButton').required = false;

	checkPass();
}

		</script>

		<form action="/create_account" method="post" enctype="multipart/form-data"> 
			<fieldset class="fieldset-auto-width">
				<legend>Create account</legend>
				
				<label for="name">Name and Affiliation(s):</label><br>
				<input type = "text" name = "name" id = "name" required/>
				<input type = "text" name = "nameAffiliation" id = "nameAffiliation" required/>

				<br><br>	
		
				<label for="sponsor">Sponsor Name and Affiliation(s):</label><br>
				<input type = "text" name = "sponsor" id = "sponsor" required/>
				<input type = "text" name = "sponsorAffiliation" id = "sponsorAffiliation" required/>

				<br><br>		

				<label for="email">Email:</label><br>
				<input type = "text" name = "email" id = "email" onchange = "checkEmail(); checkFields()"/>
				<span id="emailMessage" class="confirmMessage"></span>
		
				<br><br>	
		
				<label for="phone">Phone:</label><br>
				<input type = "text" name = "phone" id = "phone" onchange = "checkPhone(); checkFields()"/>
				<span id="phoneMessage" class="confirmMessage"></span>
		
				<br><br>

				<label for="group">Group:</label><br>
				<select name = "group">
					% for group in groupsList:
						<option value={{group}}>{{group}}</option>
					% end
				</select>

				<br><br>
				
				<label for="projectDescription">Short sentence about project:</label><br>
				<input type = "text" name = "projectDescription" id = "projectDescription" size = "40" required/>
		
				<br><br>				
				
				<fieldset style="width:500px">
					<legend>
						<input type="radio" name = "keyChoice" id = "keyChoice" value = "generate" onclick = "generateButton(); checkFields()" checked />Generate Key Pair
					</legend>
		
					<label for="pass1">Password:</label>
					<br>
					<input type="password" name="pass1" id="pass1" disabled onkeyup = "checkPass()"/>
					<br>
		
					<label for="pass2">Confirm Password:</label>
					<br>
					<input type="password" name="pass2" id="pass2" disabled onkeyup = "checkPass()"/>
					<span id="passwordMessage" class="confirmMessage"></span>
				</fieldset>		

				<br>

				<fieldset style="width:500px">
					<legend>
						<input type="radio" name = "keyChoice" id = "keyChoice" value = "upload" onclick = "uploadButton(); checkFields()"/>Upload <b>Public</b> Key
					</legend>
					<font color="red">Only use this option if you have a SSH key that you know and love.</font><br><br>
			  		<input type="file" name="key" id = "keyButton" required/>
					<br><br>
					<font color="red"><u>Usually has .pub file extension</u> (ex. "id_rsa.pub")</font>
				</fieldset>			  		

				<br><br>
		
		  		<label for = "username">Username (no special characters):</label>
				<br>
		  		<input type = "text" name = "username" id = "username" required/>
				<br><br>
		  		
				<input type = "submit" value = "Submit" id = "submit" disabled/><br>
			</fieldset></div><br><br>

	
			<fieldset>
				<legend>Generating SSH key pairs locally</legend>

				<br>
				-- Windows --
				<br>
		
				<ol>
					<li>Download PuTTYgen (available <a href = "http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html">here</a>) and run the executable.</li><br>
					<li>Click on the <b>Generate</b> button and follow on-screen instructions.</li><br>
					<li>Create and confirm a <b>Key passphrase</b>.</li><br>
					<li>Save public and private keys. Saving the public key with the extension <b>.pub</b> can help to distinguish between the two keys.</li><br>
					<li> Upload the <b>public</b> key file.</li>
				</ol>

				<br>
				-- Linux/Mac --
				<br>
		
				<ol>
					<li>In a terminal, type the command <b>ssh-keygen -t rsa</b>, and press enter.</li>
						<ul>      
							<li>To save the key pair in a different directory or with a different name, add the <b>-f</b> flag followed by the directory and key pair name (e.g. ~/Desktop/key).</li>
						</ul>
					<br>
					<li> When asked to enter file in which to save the key, press enter without typing in a name.
						<ul>
							<li>If a file name is supplied, the key pair will be saved in the terminal's current directory with the supplied name.</li>
							<li>By default, keys are saved in the <b>~/.ssh</b> directory with the names <b>id_rsa</b>, <b>id_rsa.pub</b>.</li>
						</ul>
					<br>
					<li>Enter a password for the key pair, and press enter. You will be asked to retype the password for confirmation.</li>
					<br>
					<li>Upload the <b>public</b> key file (the one ending in <b>.pub</b>).</li>
				</ol>
			</fieldset>

				<br>

			<fieldset>
				<legend>Logging in with SSH</legend>

				<br>
				-- Windows --
				<br>
		
				<ol>
					<li>Download PuTTY (available <a href = "http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html">here</a>) and run the executable.</li>
					<br>
					<li>In the Session tab, enter the <b>Host Name</b> and select SSH as the connection type.</li>
					<br>
					<li>In the Auth tab (located in SSH), browse for and select your private key.</li>
					<br>
					<li>Click Open and enter your login credentials.</li>
				</ol>

				<br>
				-- Linux/Mac --
				<br>

				<ol>
					<li>In a terminal, type the command <b>ssh</b> followed by the remote host name.
						<ul>
							<li>If your local machine account name is different from your login username, include the <b>-l</b> flag followed by your login username. This should go before the remote host name.</li>
							<li>If the private key has a non-default name or directory, include the <b>-i</b> flag followed by the correct directory and name. This should go before the remote host name.</li>
							<li>Your command might look like this: <b>ssh -l <i>userName</i> -i <i>pathToKey remoteHostName</i></b></li>
						</ul>
					<br>
					<li>Press enter, and type the password associated with the key pair.</li>
				</ol>
			</fieldset>	
		</form>
	</body>
</html>











