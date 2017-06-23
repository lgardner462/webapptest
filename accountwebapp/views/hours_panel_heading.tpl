% i_s = str(i)
% recordID = "record" + i_s


<div class="panel-heading"> 				
	<div class="container-fluid">
		<div class="row">
			<div class="col-md-2 no-padding">
				<!-- ######################################################################################################### -->
				<!-- INSERT BUTTON -->
  			<button class="btn btn-success" type="button" data-toggle="collapse" data-target="#{{recordID}}" data-parent="#accordion">
  				<span class="glyphicon glyphicon-chevron-up"></span>
  			</button>
				<!-- ######################################################################################################### -->

				<!-- ######################################################################################################### -->
				<!-- DELETE RECORD FORM -->
				<form class="form-inline" action="/deleteOne" method="post" enctype="multipart/form-data">
						<div class="form-group">
						<!-- INDEX FOR DELETING RECORD : HIDDEN -->
						<input type="hidden" name="recordIndex" value={{i}}/>
						<button class="btn btn-default x-button" type="submit">
						<span class="glyphicon glyphicon-remove"></span>
						</button>
					</div>
				</form>
				<!-- ######################################################################################################### -->
			</div>

			<div class="col-md-10 no-padding">
				% if is_new_record:

					<h4>New Record</h4>


				% else:

					<!-- ######################################################################################################### -->
					<!-- FORMATTED RECORD TEXT -->
					<h4 class="panel-title pull-left">

					<!-- FORMAT RECORD START/END/DESCRIPTION -->

					<!-- name|date <start>|date <end>|duration|label|billable|emergency|<description> -->
					{{r.name}} |
					{{r.date}}<strong> <u>{{r.fstart}}</u></strong> |
					{{r.date}}<strong> <u>{{r.fend}}</u></strong> |
					
					% if (float(r.duration) <= 0):
						<span class="negative-duration">{{r.duration}}</span>
					% else:
						{{r.duration}}
					% end
					
					| {{r.label}} | {{r.billable}} | {{r.emergency}} |
					<strong>{{r.description}}</strong>
					<!-- END OF FORMAT -->

					</h4>

				% end

				<!-- ######################################################################################################### -->
			</div>
		</div>
	</div>
</div>
