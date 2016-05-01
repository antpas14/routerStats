#!/usr/bin/python
# Simple script that allows to interrogate a router via telnet and gather info about its connection status
# Currently supported models:
# - TP Link WD8970v1

import sys
import telnetlib
import time
import os
import getopt

## Constants ##
LOG_FILE_HEADER = "Timestamp\tDW rate\tUP rate\tSNR DW\tSNR UP\n"
LOG_FILE="./connection.txt" # TODO add to config file
LOGGED_VALUES= {'downstreamCurrRate': 1, 'upstreamCurrRate':2, 'downstreamNoiseMargin':3, 'upstreamNoiseMargin':4}
DELIMITER = "\t"

## Variables ##
global host
global user
global password
global config_file

def retrieve_config(config_file):
	global host
	global user
	global password
	if os.path.isfile(config_file):
		with open(config_file) as f:
			for line in f:
				arr_line = line.split("=")
				if len(arr_line) == 2:
					key = arr_line[0];
					value = arr_line[1]
				if key == "host":
					host = value;
				elif key == "user":
					user = value
				elif key == "password":
					password = value;
	else:
		exit
def retrieve_info():
	tn = telnetlib.Telnet(host)
	tn.read_until("username:")
	tn.write(user.strip() + "\n")
	tn.read_until("password:")
	tn.write(password.strip() + "\n")

	tn.write("adsl show info\n")
	tn.write("logout\n")

	tn_output = tn.read_all()

	arr_tn_output = tn_output.split("\n")
	result_row = [time.time(), "-", "-", "-", "-"]
	for row in arr_tn_output:
		element = row.split("=");
		if len(element) == 2:
			key = element[0];
			value = element[1];
			if key in LOGGED_VALUES:
				result_row[LOGGED_VALUES[key]] = value.replace("\r", "");
	return result_row;

def dump_to_file(result_row):
	write_header = False
	if not os.path.exists(LOG_FILE):
		write_header = True
	f = open(LOG_FILE, "a")
	if write_header:
		f.write(LOG_FILE_HEADER)
	f.write(str(result_row[0]) + DELIMITER + str(result_row[1]) + DELIMITER + str(result_row[2]) + DELIMITER + str(result_row[3]) + DELIMITER + str(result_row[4]) + "\n")
	f.close

def usage():
	pass
	#TODO

def main():
	global host
	global user
	global password
	host = "localhost"
	config_file="./default.cfg"
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hf:", ["help"])
	except getopt.GetoptError as err:
	        print str(err) 
        	usage()
	        sys.exit(2)
	for o, a in opts:
		if o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-f"):
			config_file = a
		else:
			assert False, "unhandled option"
	result_row = [time.time(), "-", "-", "-", "-"]
	while result_row[1] == "-": # Added this loop because sometimes retrieve_info function fail to fill result_row values 
		time.sleep(5)

		retrieve_config(config_file)
		result_row = retrieve_info()

	# When result row is filled, then dump info to the file
	dump_to_file(result_row)
if __name__ == "__main__":
    main()
