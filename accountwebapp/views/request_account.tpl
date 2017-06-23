<!DOCTYPE html>
<html>
<head>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css"/>
	<link rel="stylesheet" type="text/css" href="{{ url('static', filename='request_account.css') }}" />
</head>

<body>


<!-- ######################################################################################################### -->
<!-- ######################################################################################################### -->
<!-- JAVASCRIPT functions START -->

<script type="text/javascript">
// #########################################################################################################
var defaultColor = "#ffffff"; 
var goodColor = "#66cc66";
var badColor = "#ff6666";

var emailFilter = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
var phoneFilter = /^[(]{0,1}[0-9]{3}[)]{0,1}[-\s\.]{0,1}[0-9]{3}[-\s\.]{0,1}[0-9]{4}$/;
var userNameFilter = /^([a-z_][a-z0-9_]{0,30})$/;

// #########################################################################################################
function checkEmail(affectField) {
	if(typeof(affectField)==='undefined') affectField = true;

	var email = document.getElementById('email');
	var message = document.getElementById('emailMessage');
	
	var testresults = false;

	if (emailFilter.test(email.value)) {
		testresults=true;
		if(affectField) {
			email.style.backgroundColor = goodColor;
			emailMessage.innerHTML = "";
		}
	}
	else if(email.value != "") {
		testresults=false;
		if(affectField) {
			email.style.backgroundColor = badColor;
			emailMessage.style.color = badColor;
			emailMessage.innerHTML = "Invalid email.";
		}
	}
	else {
		testresults = false;
		email.style.backgroundColor = defaultColor;
		emailMessage.innerHTML = "";
	}

	return (testresults);
}

// #########################################################################################################
function checkPhone(affectField) {
	if(typeof(affectField)==='undefined') affectField = true;

	var phone = document.getElementById('phone');
	var message = document.getElementById('phoneMessage');

	var testresults = false;

	if (phoneFilter.test(phone.value)) {
		testresults=true;
		if(affectField) {
			phone.style.backgroundColor = goodColor;
			phoneMessage.innerHTML = "";
		}
	}
	else if(phone.value != "") {
		testresults=false;
		if(affectField) {
			phone.style.backgroundColor = badColor;
			phoneMessage.style.color = badColor;
			phoneMessage.innerHTML = "Invalid phone.";
		}
	}
	else {
		testresults = false;
		phone.style.backgroundColor = defaultColor;
		phoneMessage.innerHTML = "";
	}

	return (testresults);
}

// #########################################################################################################
function checkUserName(affectField) {
	if(typeof(affectField)==='undefined') affectField = true;

	var userName = document.getElementById('username');
	var userNameMessage = document.getElementById('usernameMessage')

	var testresults = false;
	
	if (userNameFilter.test(userName.value)) {
		testresults=true;
		
		if(affectField) {
			userName.style.backgroundColor = goodColor;
			userNameMessage.innerHTML = "";
		}
	}
	else if(userName.value != "") {
		testresults=false;
		if(affectField) {
			userName.style.backgroundColor = badColor;
			userNameMessage.style.color = badColor;
			userNameMessage.innerHTML = "Invalid username.";
		}
	}
	else {
		testresults = false;
		userName.style.backgroundColor = defaultColor;
		userNameMessage.innerHTML = "";
	}

	return (testresults);
}

// #########################################################################################################
function checkPass(affectField) {
	if(typeof(affectField)==='undefined') affectField = true;
	var testresults = false;

	//Store the password field objects into variables
	var pass1 = document.getElementById('pass1');
	var pass2 = document.getElementById('pass2'); 
	var submit = document.getElementById('submit');

	//Store the Confimation Message Object 
	var message = document.getElementById('passwordMessage');
	var submit = document.getElementById('submit');

	//Compare the values in the password field and the confirmation field
	if(pass1.value == pass2.value && pass1.value.length > 4) {
		testresults = true;
		if(affectField) {        
			pass1.style.backgroundColor = goodColor;
			pass2.style.backgroundColor = goodColor;
			message.style.color = goodColor;
			message.innerHTML = "Passwords match.";

			if(checkEmail(false) && checkPhone(false)) {	
				submit.disabled = false;
			}
			else {
				submit.disabled = true;
			}
		}
	}
	else if(pass1.value == "" && pass2.value == "") {
		testresults = false;
		submit.disabled = true;
		pass1.style.backgroundColor = defaultColor;
		pass2.style.backgroundColor = defaultColor;
		message.innerHTML = "";
	}
	else if(pass1.value.length <= 4) {
		testresults = false;
		submit.disabled = true;
		if(affectField) {	
			pass1.style.backgroundColor = badColor;
			pass2.style.backgroundColor = badColor;
			message.style.color = badColor;
			message.innerHTML = "Password must be greater than four characters.";    
		}
	}
	else {
		testresults = false;
		submit.disabled = true;
		if(affectField) {        
			pass1.style.backgroundColor = badColor;
			pass2.style.backgroundColor = badColor;
			message.style.color = badColor;
			message.innerHTML = "Passwords do not match.";
		}
	}

	return (testresults);
}

// #########################################################################################################
function checkFields() {
	var submit = document.getElementById('submit');
	var keyChoice = document.querySelector('input[name = "keyChoice"]:checked').value;

	if(checkEmail(false) && checkPhone(false) && checkUserName(false) && (keyChoice == "upload" || checkPass(false))) {
		submit.disabled = false;
	}
	else {
		submit.disabled = true;
	}
	return;
}


// #########################################################################################################
function uploadButton() { 
	var pass1 = document.getElementById('pass1');
	var pass2 = document.getElementById('pass2');
	var message = document.getElementById('passwordMessage');

	document.getElementById('keyButton').disabled = false;
	document.getElementById('keyButton').required = true;

	pass1.disabled = true;
	pass2.disabled = true;

	pass1.style.backgroundColor = defaultColor;
	pass2.style.backgroundColor = defaultColor;

	message.innerHTML = "";
}

// #########################################################################################################
function generateButton() {
	document.getElementById('pass1').disabled = false;
	document.getElementById('pass2').disabled = false;
	document.getElementById('keyButton').disabled = true;
	document.getElementById('keyButton').required = false;

	checkPass();
}

</script>

<!-- JAVASCRIPT functions END -->	
<!-- ######################################################################################################### -->
<!-- ######################################################################################################### -->


















<!-- ######################################################################################################### -->
<!-- ######################################################################################################### -->
<!-- HTML START -->

<form action="/request_account" method="post" enctype="multipart/form-data" id="form">
<div class="container">
	<h1>Request Account</h1>
	<!-- ######################################################################################################### -->
	<div class="fields">
    <fieldset class="col-md-6">
    	<!-- ############################################# -->
      <label for="name">Name and Affiliation(s):</label><br>
      <input type = "text" name = "name" id = "name" required/>
      <input type = "text" name = "nameAffiliation" id = "nameAffiliation" required/>
      <br><br>
      <!-- ############################################# -->
      <label for="sponsor">Sponsor Name and Affiliation(s):</label><br>
      <input type = "text" name = "sponsor" id = "sponsor" required/>
      <input type = "text" name = "sponsorAffiliation" id = "sponsorAffiliation" required/>
      <br><br>
      <!-- ############################################# -->
      <label for="email">Email: (Please use your institution's email)</label><br>
      <input type = "text" name = "email" id = "email" onchange = "checkEmail(); checkFields()"/>
      <span id="emailMessage" class="confirmMessage"></span>
      <br><br>
      <!-- ############################################# -->
      <label for="phone">Phone:</label><br>
      <input type = "text" name = "phone" id = "phone" onchange = "checkPhone(); checkFields()"/>
      <span id="phoneMessage" class="confirmMessage"></span>
      <br><br>
      <!-- ############################################# -->
      <label for="group">Group:</label><br>
      <select name = "group">
        % dropdownList=groupsList
        % if "mit_psfc" in dropdownList:
        % dropdownList.remove("mit_psfc") 
        % end
        % for group in dropdownList:
        
        <option value={{group}}>{{group}}</option>
        % end
      </select>
      <br><br>
      <!-- ############################################# -->
      <label for="projectDescription">Short sentence about project:</label><br>
      <input type = "text" name = "projectDescription" id = "projectDescription" size = "40" required/>
      <br><br>
      <!-- ############################################# -->		
      <div class="passwordOption">
        <fieldset>
          <legend>
            <input type="radio" Style="display:none"name = "keyChoice" id = "keyChoice" value = "generate" onclick = "generateButton(); checkFields()" checked /> Generate Key Pair
          </legend>
          <label for="pass1">Password:</label>
          <br>
          <input type="password" name="pass1" id="pass1" onkeyup = "checkPass()"/>
          <br>
          <label for="pass2">Confirm Password:</label>
          <br>
          <input type="password" name="pass2" id="pass2" onkeyup = "checkPass()"/>
          <span id="passwordMessage" class="confirmMessage"></span>
        </fieldset>
      </div>
      <!-- ############################################# -->
      <label for = "username">Username (Please use your institution's username):</label>
      <br>
      <input type = "text" name = "username" id = "username" onkeyup = "checkUserName(); checkFields()" required/>
      <span id="usernameMessage" class="confirmMessage"></span>
      <br><br>
      <!-- ############################################# -->
      <input type = "submit" value = "Submit" id = "submit" disabled/><br>
    </fieldset>
  </div>
	<br><br>












	<!-- ######################################################################################################### -->
	<!-- ######################################################################################################### -->

  <div class="instructions">
    <div class="col-md-6">
      <div class="tabs">
        <li>
          <input type="radio" id="tab-windows" name="tabs" checked>
          <label for="tab-windows">-- Windows --</label>
          <div id="tab-content-windows" class="tab-content animated fadeIn">
            <h2>Generating SSH key pairs locally</h2>
            <ol>
              <li>Download PuTTYgen (available <a href = "http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html">here</a>) and run the executable.</li>
              <li>Click on the <b>Generate</b> button and follow on-screen instructions.</li>
              <li>Create and confirm a <b>Key passphrase</b>.</li>
              <li>Save public and private keys. Saving the public key with the extension <b>.pub</b> can help to distinguish between the two keys.</li>
              <li> Upload the <b>public</b> key file.</li>
            </ol>
            <h2>Logging in with SSH</h2>
            <ol>
              <li>Download PuTTY (available <a href = "http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html">here</a>) and run the executable.</li>
              <li>In the Session tab, enter the <b>Host Name</b> and select SSH as the connection type.</li>
              <li>In the Auth tab (located in SSH), browse for and select your private key.</li>
              <li>Click Open and enter your login credentials.</li>
            </ol>
          </div>
          <!-- div contents -->
        </li>
        <!-- windows tab -->
        <li>
          <input type="radio" id="tab-linux" name="tabs">
          <label for="tab-linux">-- Linux/MacOS --</label>
          <div id="tab-content-linux" class="tab-content animated fadeIn">
            <h2>Generating SSH key pairs locally</h2>
            <ol>
              <li>In a terminal, type the command <b>ssh-keygen -t rsa</b>, and press enter.</li>
              <ul>
                <li>To save the key pair in a different directory or with a different name, add the <b>-f</b> flag followed by the directory and key pair name (e.g. ~/Desktop/key).</li>
              </ul>
              <li>
                When asked to enter file in which to save the key, press enter without typing in a name.
                <ul>
                  <li>If a file name is supplied, the key pair will be saved in the terminal's current directory with the supplied name.</li>
                  <li>By default, keys are saved in the <b>~/.ssh</b> directory with the names <b>id_rsa</b>, <b>id_rsa.pub</b>.</li>
                </ul>
              <li>Enter a password for the key pair, and press enter. You will be asked to retype the password for confirmation.</li>
              <li>Upload the <b>public</b> key file (the one ending in <b>.pub</b>).</li>
              <li>Make sure to run the command <b>chmod 600 <i>path/to/private/key</i></b> to secure your private key.
            </ol>
            <h2>Logging in with SSH</h2>
            <ol>
              <li>
                In a terminal, type the command <b>ssh</b> followed by the remote host name.
                <ul>
                  <li>If your local machine account name is different from your login username, include the <b>-l</b> flag followed by your login username. This should go before the remote host name.</li>
                  <li>If the private key has a non-default name or directory, include the <b>-i</b> flag followed by the correct directory and name. This should go before the remote host name.</li>
                  <li>Your command might look like this:<br>
                    <b>ssh -l <i>userName</i> -i <i>path/to/key remoteHostName</i></b>
                  </li>
                </ul>
              <li>Press enter, and type the password associated with the key pair.</li>
            </ol>
          </div>
          <!-- div contents -->
        </li>
        <!-- linux tab -->
      </div>
      <!-- div tabs -->
    </div>
    <!-- div col-md-6 -->
	</div>
  <!-- div instructions -->
  <!-- ######################################################################################################### -->
	<!-- ######################################################################################################### -->
</form>
</body>
</html>











