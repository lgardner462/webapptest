<!DOCTYPE html>
<html>
	<head>
	  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css"/>
	  <link rel="stylesheet" type="text/css" href="{{ url('static', filename='csvCommon.css') }}" />
	  <link rel="stylesheet" type="text/css" href="{{ url('static', filename='top1.css') }}" />
	</head>

	<body>
	        <div class="container">
		  
		  <div class="row">
		    <h1 class="col-md-12">All Nodes</h1>
		  </div>

		  <div class="row">
		    <div class="navbar navbar-default">
		      <ul class="nav nav-tab">
			<li class="col-md-4"><a href="download/txe1_node_hwtab.csv">Download CSV</a></li>
			<li class="col-md-4"><a href="showmac">Show Mac Addresses</a></li>
			<li class="col-md-4"><a href="showrack">Show Rack Locations</a></li>
		      </ul>
		    </div>
		  </div>
		
		  <div class="row">
		    <div class="nodes">
        	      <table border="1">
			%for node in sorted(nameCSVZipped):
			<tr>
			  <td><a href="{{node}}"><h3>{{node}}</h3></a></td>
			  <td>{{nameCSVZipped[node]}}</td>
			</tr>
        		%end
		      </table>
		    </div>
		  </div>

		  <div class="row">
		    <div class="footer">
		      
		    </div>
		  </div>

		</div>
	</body>
</html>
