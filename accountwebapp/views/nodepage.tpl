<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css"/>
    <link rel="stylesheet" type="text/css" href="{{ url('static', filename='csvCommon.css') }}" />
    <link rel="stylesheet" type="text/css" href="{{ url('static', filename='nodepage.css') }}" />
  </head>

  <body>
    <div class="container">
      
      <div class="row">
	<h1 class="col-mid-12">Node Page</h1>
      </div>

      <div class="row">
	<div class="navbar navbar-default">
	  <ul class="nav nav-tab">
	    <li class="col-md-3"><a href="download/txe1_node_hwtab.csv">Download CSV</a></li>
	    <li class="col-md-3"><a href="top">Show All Nodes</a></li>
	    <li class="col-md-3"><a href="showmac">Show Mac Addresses</a></li>
	    <li class="col-md-3"><a href="showrack">Show Rack Locations</a></li>
	  </ul>
	</div>
      </div>
      
      <br><br>

      <table border = '1'>
	%fields = data.split(',')
	%for field in fields:
	%stripped = field.translate(None, '[]\"') 
	
	<tr> <td>
	    %if ("node" in stripped):
	    <h2><center>{{stripped}}</center></h2>
	    %else:
	    {{stripped}}
	    %end
	</td> </tr>

	%end
      </table>
    </div>
  </body>
</html>
