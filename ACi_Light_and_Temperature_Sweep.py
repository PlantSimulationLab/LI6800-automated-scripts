from bpdefs import EXEC, GROUP, ASSIGN, IF, DIALOG, RETURN, LOOP, SETCONTROL, SHOW, WAIT, WHILE, LOG, ELSE, Nothing, CheckBox, Text, Button, DropDown, RadioBtns, EditBox, DataDict

steps=[
# Compile and run python: EXEC(scope, [source=code] or [file=filename])
EXEC(0,file="/home/licor/resources/lib/dyn_tools.py"),
# Collection: GROUP(enabled, label)
GROUP("True","Opening Dialog",
	steps=(
		# Assign a variable to an expression: ASSIGN('varname', exp="expression" [,dlg=Nothing()])
		ASSIGN("begin_co2",
			exp="10",
			dlg=EditBox("'Starting CO2'", units="'\u00b5mol mol\u207b\u00b9'", desc="'Starting CO2_r for ramp'")),
		# Assign a variable to an expression: ASSIGN('varname', exp="expression" [,dlg=Nothing()])
		ASSIGN("init_wait",
			exp="1",
			dlg=EditBox("'Pre ramp wait'", units="'min'", desc="'Equil time at starting CO2 before starting ramp'")),
		# Assign a variable to an expression: ASSIGN('varname', exp="expression" [,dlg=Nothing()])
		ASSIGN("end_co2",
			exp="2000",
			dlg=EditBox("'Ending CO2'", units="'\u00b5mol mol\u207b\u00b9'", desc="'Ending CO2_r for ramp'")),
		# Assign a variable to an expression: ASSIGN('varname', exp="expression" [,dlg=Nothing()])
		ASSIGN("post_co2",
			exp="400",
			dlg=EditBox("'Post-ramp CO2'", units="'\u00b5mol m\u207b\u00b2 s\u207b\u00b9'", desc="'Post ramp value for CO2_r'")),
		# Assign a variable to an expression: ASSIGN('varname', exp="expression" [,dlg=Nothing()])
		ASSIGN("ramp_rate",
			exp="300",
			dlg=EditBox("'Ramp rate'", units="'\u00b5mol mol\u207b\u00b9 min\u207b\u00b9'", desc="'Rate of change of CO2 to use'")),
            # Assign a variable to an expression: ASSIGN('varname', exp="expression" [,dlg=Nothing()])
		ASSIGN("light_levels",
    		exp="[0,200,600,1200,1600,2000]",
    		dlg=EditBox("'Light levels'", units="'\u00b5mol m\u207b\u00b2 s\u207b\u00b9'", desc="'Light fluxes'")),
		# Assign a variable to an expression: ASSIGN('varname', exp="expression" [,dlg=Nothing()])
		ASSIGN("temperatures",
    		exp="[25,30,35,38,40,43]",
    		dlg=EditBox("'Temperatures'", units="'C'", desc="'Air Temperatures'")),
		# Assign a variable to an expression: ASSIGN('varname', exp="expression" [,dlg=Nothing()])
		ASSIGN("log_int",
			exp="5",
			dlg=EditBox("'Logging interval'", units="'s'", desc="'Log every __ during ramp'")),
		# Assign a variable to an expression: ASSIGN('varname', exp="expression" [,dlg=Nothing()])
		ASSIGN("post_wait",
			exp="0",
			dlg=EditBox("'Post ramp wait'", units="'min'", desc="'Equil time after ramp ends'")),
		# Assign a variable to an expression: ASSIGN('varname', exp="expression" [,dlg=Nothing()])
		ASSIGN("pwlog",
			exp="{'checked':False, 'value':15}",
			dlg=EditBox("'Log post ramp'", units="'s'", desc="'Logging interval'", checkable=True)),
		# Collection: GROUP(enabled, label)
		GROUP("True","Last time defaults",
			steps=(
				# Compile and run python: EXEC(scope, [source=code] or [file=filename])
				EXEC(0,source="BP.setDlgFile('/home/licor/apps/dynamic/_dat_co2_cont_rep.json')"),
			)
		),
		# Open a dialog: DIALOG(title=string [,sub=string] [,text=string] [,items=list_of_edit_items] [,buttons=list_of_buttons] [var=pressed_btn_name])
		DIALOG(title="'Repetitive DAT CO2 Continuous Ramp'",
			sub="'Multiple reps of Low to High, or High to Low'",
			items="begin_co2,init_wait,end_co2,post_wait,log_int,pwlog,ramp_rate,light_levels,temperatures,post_co2",
			buttons="'Cancel','Continue'",
			var="button"),
		IF("button == 'Cancel'",
			steps=(
				RETURN(),
			)
		),
		# Collection: GROUP(enabled, label)
		GROUP("True","Check validity",
			steps=(
				# Compile and run python: EXEC(scope, [source=code] or [file=filename])
				EXEC(0,source="issues=checkValidity(True)"),
				IF("len(issues)",
					steps=(
						# Open a dialog: DIALOG(title=string [,sub=string] [,text=string] [,items=list_of_edit_items] [,buttons=list_of_buttons] [var=pressed_btn_name])
						DIALOG(title="'Not Ready to Run'",
							sub="'Fix the following issues, then try again:'",
							text="'\\n'.join(issues)",
							buttons="'Ok'",
							var="button"),
						RETURN(),
					)
				),
			)
		),
	)
),

# Start Curve ID counter
ASSIGN("curve_id", dd=DataDict("User:CurveID", "Ctrl")),
IF("curve_id == '' or curve_id is None", steps=(
    ASSIGN("curve_id", exp="0"),
)),
ASSIGN("curve_id", exp="int(curve_id)"),

# Loop through a list: LOOP(list=itemList [,var=varname] [,mininc=''])
LOOP(list="light_levels",
	var="light_level",
	steps=(
		# Collection: GROUP(enabled, label)
		GROUP("True","Transition to start",
			steps=(
				# Set a control: SETCONTROL('target', 'value', 'eval' [,opt_target=''])
				SETCONTROL("CO2_r","begin_co2","float"),
				SETCONTROL("Tair","25","float"),
                SETCONTROL("Qin","light_level","float"),
				# Assign a variable to a Data Dictionary entry: ASSIGN('varname', dd=DataDict('group', 'name' [,bool_logged]) [,track=False] [,optvar='varname'] [dlg=Nothing()))])
				ASSIGN("co2",
					dd=DataDict('CO2_r','Meas'),
					track=True),
				# Print to run log: SHOW([items=(list of items)] or [string='string_to_print'])
				SHOW(string="'Waiting for CO2 to reach {0}...'.format(begin_co2)"),
				# Wait for an event: WAIT(event="bool expression"
				WAIT(event="abs(co2 - begin_co2)<20"),
				# Print to run log: SHOW([items=(list of items)] or [string='string_to_print'])
				SHOW(string="'Equilibration wait...'"),
				# Wait for a time duration: WAIT(dur="float" [,units='Seconds' (Seconds|Minutes|Hours)])
				WAIT(dur="init_wait",units="Minutes"),
			)
		),
		# Collection: GROUP(enabled, label)
		GROUP("True","Collect New Data",
			steps=(
				# Compile and run python: EXEC(scope, [source=code] or [file=filename])
				EXEC(0,source="BP.setLogBuffering(15)"),
				# Assign a variable to an expression: ASSIGN('varname', exp="expression" [,dlg=Nothing()])
				ASSIGN("period",
					exp="abs(end_co2-begin_co2)/ramp_rate*60"),
				# Generate curve ID using counter
				ASSIGN("curve_id", exp="int(curve_id) + 1"),
				# Save back as int
				SETCONTROL("User:CurveID", "curve_id", "int"),
				SHOW(string="'Running curve #{}'.format(curve_id)"),
				# Add response type
				ASSIGN("response_type", exp="'light'"),
				SETCONTROL("User:Response", "response_type", "string"),
				# Compile and run python: EXEC(scope, [source=code] or [file=filename])
				EXEC(0,source="ramp = DynamicRamp('CO2_r', begin_co2, end_co2, period, repcount=1)   "),
				# Compile and run python: EXEC(scope, [source=code] or [file=filename])
				EXEC(0,source="BP.launch(ramp)"),
				# Collection: GROUP(enabled, label)
				GROUP("True","This sets log averaging to match log interval",
					steps=(
						# Set a control: SETCONTROL('target', 'value', 'eval' [,opt_target=''])
						SETCONTROL("LogOpts:AvgTime","True,min(15, log_int)","int"),
					)
				),
				# Wait for a time duration: WAIT(dur="float" [,units='Seconds' (Seconds|Minutes|Hours)])
				WAIT(dur="2",units="Seconds"),
				# Loop while something is True: WHILE("bool_expression", [,var='elapsed_seconds'] [,mininc="secs"])
				WHILE("ramp.is_alive()",
					mininc="log_int",
					steps=(
						# Log a data record: LOG([avg='Default'] [,match='Default'] [,matchH2O='Default'] [,flr='Default'] [flash='Default'])
						LOG(match="Off",
							matchH2O="Off",
							flr="0: Nothing"),
					)
				),
			)
		),
		# Set a control: SETCONTROL('target', 'value', 'eval' [,opt_target=''])
		SETCONTROL("CO2_r","post_co2","float"),
		IF("pwlog['checked']",
			steps=(
				# Collection: GROUP(enabled, label)
				GROUP("True","This sets log averaging to match log interval",
					steps=(
						# Set a control: SETCONTROL('target', 'value', 'eval' [,opt_target=''])
						SETCONTROL("LogOpts:AvgTime","1,min(15, pwlog['value])","int"),
					)
				),
				# Loop for a duration: LOOP(dur="float" [,units='Seconds' Second|Minutes|Hours ] [,var=''] [,mininc=''])
				LOOP(dur="post_wait",
					units="Minutes",
					mininc="pwlog['value']",
					steps=(
						# Log a data record: LOG([avg='Default'] [,match='Default'] [,matchH2O='Default'] [,flr='Default'] [flash='Default'])
						LOG(match="Off",
							matchH2O="Off",
							flr="0: Nothing"),
					)
				),
			)
		),
		ELSE(steps=(
				# Wait for a time duration: WAIT(dur="float" [,units='Seconds' (Seconds|Minutes|Hours)])
				WAIT(dur="post_wait",units="Minutes"),
			)
		),
	)
),
LOOP(list="temperatures",
	var="temperature",
	steps=(
		# Collection: GROUP(enabled, label)
		GROUP("True","Transition to start",
			steps=(
				# Set a control: SETCONTROL('target', 'value', 'eval' [,opt_target=''])
				SETCONTROL("CO2_r","begin_co2","float"),
				SETCONTROL("Tair","temperature","float"),
				ASSIGN("elapsed", exp="0"),
				ASSIGN("tair", dd=DataDict('Tchamber', 'Meas'), track=True),
				WHILE("abs(tair - temperature) > 0.5 and elapsed < 300",
					var="elapsed",
					mininc="5",
					steps=(
						ASSIGN("tair", dd=DataDict('Tchamber', 'Meas'), track=True),
						SHOW(string="'Elapsed: {0:.1f}s, Tair: {1:.2f}°C, Target: {2:.1f}'.format(elapsed, tair, temperature)"),
					)
				),
				# Assign a variable to a Data Dictionary entry: ASSIGN('varname', dd=DataDict('group', 'name' [,bool_logged]) [,track=False] [,optvar='varname'] [dlg=Nothing()))])
				ASSIGN("co2",
					dd=DataDict('CO2_r','Meas'),
					track=True),
				# Print to run log: SHOW([items=(list of items)] or [string='string_to_print'])
				SHOW(string="'Waiting for CO2 to reach {0}...'.format(begin_co2)"),
				# Wait for an event: WAIT(event="bool expression"
				WAIT(event="abs(co2 - begin_co2)<20"),
				# Print to run log: SHOW([items=(list of items)] or [string='string_to_print'])
				SHOW(string="'Equilibration wait...'"),
				# Wait for a time duration: WAIT(dur="float" [,units='Seconds' (Seconds|Minutes|Hours)])
				WAIT(dur="init_wait",units="Minutes"),
			)
		),
		# Collection: GROUP(enabled, label)
		GROUP("True","Collect New Data",
			steps=(
				# Compile and run python: EXEC(scope, [source=code] or [file=filename])
				EXEC(0,source="BP.setLogBuffering(15)"),
				# Assign a variable to an expression: ASSIGN('varname', exp="expression" [,dlg=Nothing()])
				ASSIGN("period",
					exp="abs(end_co2-begin_co2)/ramp_rate*60"),
				# Generate curve ID using counter
				ASSIGN("curve_id", exp="int(curve_id) + 1"),
				# Save back as int
				SETCONTROL("User:CurveID", "curve_id", "int"),
				SHOW(string="'Running curve #{}'.format(curve_id)"),
				# Add response type
				ASSIGN("response_type", exp="'temperature'"),
				SETCONTROL("User:Response", "response_type", "string"),
				# Compile and run python: EXEC(scope, [source=code] or [file=filename])
				EXEC(0,source="ramp = DynamicRamp('CO2_r', begin_co2, end_co2, period, repcount=1)   "),
				# Compile and run python: EXEC(scope, [source=code] or [file=filename])
				EXEC(0,source="BP.launch(ramp)"),
				# Collection: GROUP(enabled, label)
				GROUP("True","This sets log averaging to match log interval",
					steps=(
						# Set a control: SETCONTROL('target', 'value', 'eval' [,opt_target=''])
						SETCONTROL("LogOpts:AvgTime","True,min(15, log_int)","int"),
					)
				),
				# Wait for a time duration: WAIT(dur="float" [,units='Seconds' (Seconds|Minutes|Hours)])
				WAIT(dur="2",units="Seconds"),
				# Loop while something is True: WHILE("bool_expression", [,var='elapsed_seconds'] [,mininc="secs"])
				WHILE("ramp.is_alive()",
					mininc="log_int",
					steps=(
						# Log a data record: LOG([avg='Default'] [,match='Default'] [,matchH2O='Default'] [,flr='Default'] [flash='Default'])
						LOG(match="Off",
							matchH2O="Off",
							flr="0: Nothing"),
					)
				),
			)
		),
		# Set a control: SETCONTROL('target', 'value', 'eval' [,opt_target=''])
		SETCONTROL("CO2_r","post_co2","float"),
		IF("pwlog['checked']",
			steps=(
				# Collection: GROUP(enabled, label)
				GROUP("True","This sets log averaging to match log interval",
					steps=(
						# Set a control: SETCONTROL('target', 'value', 'eval' [,opt_target=''])
						SETCONTROL("LogOpts:AvgTime","1,min(15, pwlog['value])","int"),
					)
				),
				# Loop for a duration: LOOP(dur="float" [,units='Seconds' Second|Minutes|Hours ] [,var=''] [,mininc=''])
				LOOP(dur="post_wait",
					units="Minutes",
					mininc="pwlog['value']",
					steps=(
						# Log a data record: LOG([avg='Default'] [,match='Default'] [,matchH2O='Default'] [,flr='Default'] [flash='Default'])
						LOG(match="Off",
							matchH2O="Off",
							flr="0: Nothing"),
					)
				),
			)
		),
		ELSE(steps=(
				# Wait for a time duration: WAIT(dur="float" [,units='Seconds' (Seconds|Minutes|Hours)])
				WAIT(dur="post_wait",units="Minutes"),
			)
		),
	)
),
]
