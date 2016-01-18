import time

# Event types, SIA Standard
event_qualifiers = {
	"E": "New Event     ",
	"R": "Event Restored",
	"P": "Previous Event"
}

# Event codes, also SIA standard(-ish)
event_codes = {
	"100": "Medical:                 Emergency                      ",
	"102": "Medical:                 Fail to report in              ",
	"110": "Fire:                    FIRE                           ",
	"121": "Panic:                   Duress Alarm                   ",
	"122": "Panic:                   Silent Alarm                   ",
	"123": "Panic:                   Audible Alarm                  ",
	"129": "Panic:                   Confirmed Alarm                ",
	"130": "Burglary:                Burglary                       ",
	"133": "Burglary:                24 Hr Burglary                 ",
	"134": "Burglary:                Entry/Exit                     ",
	"137": "Burglary:                Tamper Alarm                   ",
	"139": "Burglary:                Verified Intrusion             ",
	"143": "General:                 Expansion Module Failure/Tamper",
	"145": "General:                 Expansion Module Failure/Tamper",
	"150": "24 Hr:                   Auxilary Alarm                 ",
	"151": "24 Hr:                   Gas Detected                   ",
	"220": "Monitored Alarm:         Key Tube Alarm                 ",
	"300": "System Issue:            System Trouble                 ",
	"301": "System Issue:            AC Power Loss                  ",
	"302": "System Issue:            Low Battery                    ",
	"305": "System Issue:            System Reset                   ",
	"320": "SOUNDER/RELAY TROUBLES:  Sounder/Relay                  ",
	"333": "SYS PERIPHERAL TROUBLES: Expansion Module Failure       ",
	"344": "SYS PERIPHERAL TROUBLES: RF Jamming Detected            ",
	"350": "COMMUNICATION TROUBLES:  Communication Failure          ",
	"351": "COMMUNICATION TROUBLES:  Telco 1 Fault                  ",
	"354": "COMMUNICATION TROUBLES:  Failure to Communicate         ",
	"355": "COMMUNICATION TROUBLES:  Loss of RF supervision         ",
	"373": "PROTECTION LOOP:         Fire Loop Trouble              ",
	"380": "SENSOR:                  Sensor Trouble                 ",
	"383": "SENSOR:                  Sensor Tamper                  ",
	"384": "SENSOR:                  RF Low Battery                 ",
	"401": "OPEN/CLOSE:              Open/Close by User             ",
	"403": "OPEN/CLOSE:              Automatic Open/Close           ",
	"405": "OPEN/CLOSE:              Deferred open/close            ",
	"406": "OPEN/CLOSE:              open canceled by user          ",
	"407": "OPEN/CLOSE:              remote arm/disarm              ",
	"408": "OPEN/CLOSE:              quick arm                      ",
	"409": "OPEN/CLOSE:              keyswitch open/close           ",
	"411": "REMOTE ACCESS:           Callback Requested             ",
	"412": "REMOTE ACCESS:           Successful Access              ",
	"421": "ACCESS CONTROL:          Access Denied                  ",
	"422": "ACCESS CONTROL:          Access Gained                  ",
	"457": "OPEN/CLOSE:              Exit Error                     ",
	"459": "OPEN/CLOSE:              Recent Close                   ",
	"570": "BYPASSES:                Zone/Sensor Bypass             ",
	"601": "TEST/MISC:               Manual Test                    ",
	"602": "TEST/MISC:               Periodic Test                  ",
	"607": "TEST/MISC:               Walk Test                      ",
	"623": "EVENT LOG:               Event Log 90% Full             ",
	"625": "EVENT LOG:               Time/Date Changed              ",
	"627": "EVENT LOG:               Program Mode Entry             ",
	"628": "EVENT LOG:               Program Mode Exit              "
}

# If your alarm is set up with multiple areas, these will be included in the logs. Areas are different from Zones, which tend to be a single sensor.
event_areas = {
	"01": "Area 1",
	"02": "Area 2"
}

# The alarm reports a zone or user code/ID, but does not differentiate which of the two it is
zones_users = {
	"000": "                   / Engineer",
	"001": "Main Entrance      / Master",
	"002": "Hall PIR           / John Smith",
	"003": "Main Office PIR 1  / Joe Bloggs",
	"004": "Main Office PIR 2  / Jane Smith",
	"005": "Kitchen PIR        / A. N. Other",
	"006": "Fire Exit          / U. N. Owen",
	"007": "Meeting Room 1 PIR / Cleaner",
	"008": "Meeting Room 2 PIR / Spare",
	"009": "Fire Alarm Relay   / ",
	"010": "Panic Button       / ",
}


# Lines read from the log file, keeps track of our process
lines_read = 0

# Loop forever
while True:
	# Open the log file
	with open("C:\Program Files (x86)\Texecom\Montex\Tx_Log.TXT") as logfile:
		# How many lines we've read this loop
		lines_read_now = 0
		# skip lines already read
		while lines_read_now <= lines_read:
			skipped = logfile.readline()
			lines_read_now += 1
		# Now we're at lines we haven't seen before
		for line in logfile:
			# Set defaults for each section of log data
			line_qualifier = "UNKNOWN QUALIFIER"
			line_timedate  = "UNKNOWN TIME & DATE"
			line_code      = "UNKNOWN EVENT"
			line_area      = "UNKNOWN AREA"
			line_userzone  = "UNKNOWN USER/ZONE"
			
			# There are two different log formats depending on the alarm model.
			# First log format, events start with the magic number "5041"
			if line[23:27] == "5041":
				# Extract each pieec of data from the log, starting with event type
				try:
					line_qualifier = event_qualifiers[line[34]]
				except KeyError:
					line_qualifier = "Unknown event qualifier ({})".format(line[34])
				# Date and Time
				try:
					line_timedate = line[0:19]
				except KeyError:
					pass
				# SIA Event Code
				try:
					line_code = event_codes[line[35:38]]
				except KeyError:
					line_code = "Unknown event code ({})".format(line[35:38])
				# Event area
				try:
					line_area = event_areas[line[38:40]]
				except KeyError:
					line_area = "Unknown event area ({})".format(line[38:40])
				# Zone or USer
				try:
					line_userzone = zones_users[line[40:43]]
				except KeyError:
					line_userzone = "Unknown event area ({})".format(line[40:43])
				# Demo script prints this to STDOUT in a useful format. Put your custom output here
				print "{} at {}. {}. Area {}, zone/user {}".format(line_qualifier, line_timedate, line_code, line_area, line_userzone)
			# Next log format, this is for devices checking in with no new events
			elif line[23:27] == "S041":
				try:
					checkin_code = line[34:40]
				except KeyError:
					checkin_code = "Unknown"
				# Again, demo just prints this to STDOUT.
				# Put your custom output here
				print "Device check-in, status {}".format(checkin_code)
			else:
				print "Unknown line type: {}".format(line[:-1])
			# Record that we've read some more lines
			lines_read += 1
			lines_read_now += 1
		# Wait a bit for more log entryes
		time.sleep(10)