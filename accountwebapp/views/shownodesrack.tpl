<html>
	<body>
		<table border="1">
		       <a href="dl link goes here">download csv</a>
		       %for row in nodeNames[2:]:
		       <tr>
				<td><a href="shownode/{{row}}">{{row}}</a></td>
		       </tr>
		       %end
		 </table>
	</body>
</html>
