<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css"/>
    <link rel="stylesheet" type="text/css" href="{{ url('static', filename='csvCommon.css') }}" />
    <link rel="stylesheet" type="text/css" href="{{ url('static', filename='showmac.css') }}" />
  </head>

  <body>
    <div class="container">
      
      <div class="row">
	<h1 class="col-mid-12">Mac Addresses</h1>
      </div>

      <div class="row">
	<div class="navbar navbar-default">
	  <ul class="nav nav-tab">
	    <li class="col-md-4"><a href="download/txe1_node_hwtab.csv">Download CSV</a></li>
	    <li class="col-md-4"><a href="top">Show All Nodes</a></li>
	    <li class="col-md-4"><a href="showrack">Show Rack Locations</a></li>
	  </ul>
	</div>
      </div>

      <div class="threeColumn">
	% for node in sorted(nameMacZipped):
	%mac = nameMacZipped[node]
	
	<p><a href="{{node}}">{{node}}</a> - {{mac}}</p>
	% end
      </div>
    </div>
    <div class="footer">
      
    </div>
  </body>
</html>

