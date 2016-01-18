import pyodbc
import pickle
import datetime


# Get the last date we checked for events
try:
	with open('C:\Program Files (x86)\Texecom\Texbase\data\Timestamp') as picklejar:
		current_timestamp = pickle.load(picklejar)
except IOError as e:
	print "Unable to open timestamp file: {}".format(e)
	print "Setting timestamp to midnight last night"
	current_timestamp = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())


# Connect to the database
LOCATION = "C:\Program Files (x86)\Texecom\Texbase\data"
cnxn = pyodbc.connect(r"Driver={{Microsoft Paradox Driver (*.db )\}};DriverID=538;Fil=Paradox 5.X;DefaultDir={0};Dbq={0};CollatingSequence=ASCII;".format(LOCATION), autocommit=True, readonly=True)
cursor = cnxn.cursor()

# Log the current time, which will be used to update the timestamp.
# We do this now to avoid missing events that get logged while we're still doing processing
new_timestamp = datetime.datetime.now()

#array for storing new events
events = []

# Fetch all the events from the History table
# the Paradox driver doesn't support casts, so we can't easily filter at this point
for row in cursor.execute("SELECT * FROM History WHERE DateTime >= ?", current_timestamp).fetchall():
	events.append(row)


for row in events:
	print row[6]

