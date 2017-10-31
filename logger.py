import piVirtualWire.piVirtualWire as piVirtualWire;
import time;
import pigpio;
import re;
import MySQLdb;
import argparse;
import sys;
import os;

#Setup arguments for runtime
parser = argparse.ArgumentParser();
parser.add_argument('-v', action='store_true');
parser.add_argument('-c');

#Process arguments for logging, and permissions location
args = parser.parse_args();
verbose = args.v;
if(args.c): filename = args.c;
else: filename = 'certs.txt';

if(verbose): print('Starting modules...');

#Start pigpio and piVirtualWire
pi = pigpio.pi();
rx = piVirtualWire.rx(pi, 3, 1000);

#Initialize database credential variables
dbuser='';
dbpass='';
dbname='';
dbhost='';
table='';

#Look for and parse permissions
if(os.path.exists(filename)):
	file = open(filename);
	certs = file.read().split('\n');
	for cert in certs:
		if(cert != ''): globals()[cert.split("=")[0]] = cert.split("=")[1];

#Exit if no permissions are located
else:
	print("No cert file found, please specify a file with -c or create a certs.txt file");
	sys.exit();

if(verbose): print('Done!');

#Convert the received message from an array of ASCII values to a string
def convertMessage(message):

	result = [];

	#Convert each character back to ASCII text
	for char in message:
		result.append(chr(char));

	#Join characters into a string (comma separated)
	result = ''.join(map(str, result));
	return result;

#Split the message into an array of numeric values from the logger
def processResult(message):

	result = '';
	#Trim out the node identifier 'N1' and generate the array
	message = message.split(': ');
	if(message[0] == 'N1'): result = message[1].split('\x00')[0].split(',');
	return result;

#Send received data to the database server
def sendToDB(values):

	connected = False;

	if(verbose): print('Connecting to DataBase...');
	#Attempt to connect using the provided permissions
	try:
		db = MySQLdb.connect(dbhost, dbuser, dbpass, dbname);
		cursor = db.cursor();
		connected = True;

	#Report a failed attempt to connect
	except MySQLdb.OperationalError:
		if(verbose): print('Unable to connect, aborting write!');

	if(connected):

		if(verbose): print('Connected!\nWriting data...');

		#Insert the received values into the sql query and write it to the database
		sql = "insert into %s (temperature, humidex, pressure, light, battery) values (%s, %s, %s, %s, %s)" % (table, values[0], values[1], values[2], values[3], values[4]);
		cursor.execute(sql);

		if(verbose): print('Done writing!');

		#Commit changes to the database and close the connection
		db.commit();
		db.close();

if(verbose): print('Waiting for data...');

#Main running loop
while True:

	#Wait for a message from the RF receiver
	while rx.ready():

		#Convert the received message and upload it to the database
		received_message = convertMessage(rx.get());
		result = processResult(received_message);
		if(verbose): print(result);
		if(verbose): print('writing to DB');
		sendToDB(result);
		if(verbose): print('\nWaiting for data...');

	time.sleep(0.01);

#Close piVirtualWire and pigpio
rx.cancel();
pi.stop();
