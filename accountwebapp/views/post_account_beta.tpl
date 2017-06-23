<!DOCTYPE html>

<html>
  <body>
    <head>
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css"/>
      <link rel="stylesheet" type="text/css" href="{{ url('static', filename='post_account.css') }}" />

      <script type="text/javascript">

	function disableKeyDownload()
	{
	var submit = document.getElementById('submitDownloadKey');
	submit.disabled = true;
	}


      </script>
    </head>    
    
    % if not errors:
    <div>
      <p>
	<h2>Thank you for your account request.</h2>
	Please note that this is <b>not</b> an automatic process.<br>
	Account requests may take 2 school days to process.
      </p>
      
      % if keyChoice == "generate":
      <form action="/{{clusterName}}" method="post" enctype="multipart/form-data"> 
	<input type = "hidden" name = "keyZipPath" value = "{{keyZipPath}}"/>
	<input type = "submit" name = "submitDownloadKey" value = "Download Private Key" onclick="this.disabled=true;this.value='Downloading...';this.form.submit();"/>
      </form>	
      % end

      % else:
      <p><b>Submission failed:</b></p>
      % for error in errors:
      % if error == "email":
      <p>Invalid email address.</p>
      
      % elif error == "phone":
      <p>Missing phone.</p>
      
      % elif error == "missingKey":
      <p>Missing public key.</p>

      % elif error == "privateKey":
      <p>Private key was uploaded. Please resubmit form with public key.<br>You may want to regenerate your key pair.</p>

      % elif error == "password":
      <p>Password field required.</p>

      % elif error == "passwordMatch":
      <p>Passwords do not match.</p>

      % elif error == "passwordLength":
      <p>Password must be greater than four characters.</p>
      % end
      % end
      % end
      

      % if keyChoice == "generate":
      <p>
	Private key will deleted after one download.<br>
	<font color="red"><u>Please save your password.</u></font><br>
	You will use your password for this key to log in.
      </p>
      % end
    </div>
  </body>
</html>
