import piVirtualWire.piVirtualWire as piVirtualWire;
import time;
import pigpio;
import re;
import MySQLdb;
import argparse;
import sys;
import os;

parser = argparse.ArgumentParser();
parser.add_argument('-v', action='store_true');
parser.add_argument('-c');

args = parser.parse_args();
verbose = args.v;
if(args.c): filename = args.c;
else: filename = 'certs.txt';

if(verbose): print('Starting modules...');

pi = pigpio.pi();
rx = piVirtualWire.rx(pi, 3, 1000);

dbuser='';
dbpass='';
dbname='';
dbhost='';
table='';

if(os.path.exists(filename)):
	file = open(filename);
	certs = file.read().split('\n');
	for cert in certs:
		if(cert != ''): globals()[cert.split("=")[0]] = cert.split("=")[1];

else:
	print("No cert file found, please specify a file with -c or create a certs.txt file");
	sys.exit();

if(verbose): print('Done!');

def convertMessage(message):

	result = [];

	for char in message:
		result.append(chr(char));

	result = ''.join(map(str, result));
	return result;

def processResult(message):

	result = '';
	message = message.split(': ');
	if(message[0] == 'N1'): result = message[1].split('\x00')[0].split(',');
	return result;

def sendToDB(values):

	connected = False;

	if(verbose): print('Connecting to DataBase...');
	try:
		db = MySQLdb.connect(dbhost, dbuser, dbpass, dbname);
		cursor = db.cursor();
		connected = True;

	except MySQLdb.OperationalError:
		if(verbose): print('Unable to connect, aborting write!');

	if(connected):

		if(verbose): print('Connected!\nWriting data...');

		sql = "insert into %s (temperature, humidex, pressure, light, battery) values (%s, %s, %s, %s, %s)" % (table, values[0], values[1], values[2], values[3], values[4]);
		cursor.execute(sql);

		if(verbose): print('Done writing!');

		db.commit();
		db.close();

if(verbose): print('Waiting for data...');

while True:

	while rx.ready():

		received_message = convertMessage(rx.get());
		result = processResult(received_message);
		if(verbose): print(result);
		if(verbose): print('writing to DB');
		sendToDB(result);
		if(verbose): print('\nWaiting for data...');

rx.cancel();
pi.stop();
