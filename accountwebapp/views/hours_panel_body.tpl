

% nameID = "name" + i_s
% startID = "start" + i_s
% endID = "end" + i_s
% durationID = "duration" + i_s
% billableID = "billable" + i_s
% emergencyID = "emergency" + i_s
% labelID = "label" + i_s
% descriptionID = "description" + i_s
% submitID = "submit" + i_s
% insertID = "insert" + i_s

<div class="panel-body">
	<form action="/hours" method="post" enctype="multipart/form-data">
		<fieldset class="inputs form-group">
			<!-- ######################################################################################################### -->
			<hr />
			<!-- ######################################################################################################### -->
			<!-- SINGLE LINE -->
			<div class="form-inline">
				<!-- NAME : TEXT -->
				<input name="name" id={{nameID}} type="text" class="form-control quarter-width" placeholder="Name" pattern={{NAME_REGEX}} required/>
				<!-- START TIME -->
				<input name="start" id={{startID}} type="text" class="form-control" placeholder="Start Time" pattern={{TIME_REGEX}} required/>
				<!-- END TIME -->
				<input name="end" id={{endID}} type="text" class="form-control" placeholder="End Time" pattern={{TIME_REGEX}} required/>
				<!-- DURATION : TEXT -->
				<input name="duration" id={{durationID}} type="text" class="form-control" placeholder="Duration"/>
			</div>
			<!-- END OF SINGLE LINE -->
			<!-- ######################################################################################################### -->
			<hr />
			<!-- ######################################################################################################### -->
			<!-- SINGLE LINE -->
			<div class="form-inline">
				<!-- LABEL : TEXT -->
				<input name="label" id={{labelID}} type="text" class="form-control" placeholder="Label" required/>
				<!-- DESCRIPTION : TEXT // not required (ex. lunch) -->
				<input name="description" id={{descriptionID}} type="text" class="form-control half-width" placeholder="Description" />
			</div>
			<!-- END OF SINGLE LINE -->
			<!-- ######################################################################################################### -->
			<hr />
			<!-- ######################################################################################################### -->
			<!-- SINGLE LINE -->
			<div class="form-inline padded-top">
				<!-- LEFT SIDE -->
				<div class="pull-left">
					<!-- BILLABLE CHECKBOX -->
					<div class="billable">
						<span class="checkboxtext">Billable: </span>
						<input type="checkbox" name="billable" id={{billableID}} checked />
					</div>
					<!-- EMERGENCY CHECKBOX -->
					<div class="emergency">
						<span class="checkboxtext">Emergency: </span>
						<input type="checkbox" name="emergency" id={{emergencyID}} />
					</div>
				</div>
				<!-- RIGHT SIDE -->
				<div class="pull-right">
					<!-- SUBMIT BUTTON : SUBMIT -->
					<button type="submit" name="submit" id={{submitID}} class="btn btn-default">Add Record</button>
					<!-- ######################################################################################################### -->
				</div>
			</div>
			<!-- END OF SINGLE LINE -->
			<!-- ######################################################################################################### -->

			<!-- INDEX FOR NEXT RECORD : HIDDEN -->
			<input type="hidden" name="insert" id={{insertID}} value={{0}} />
		</fieldset>
	</form>
</div> <!-- /.panel-body -->