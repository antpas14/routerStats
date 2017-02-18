#!/usr/bin/python
import socket
import struct
import subprocess;
import os;
import time;
import json;

TOTAL_BYTES = {}
CURR_BYTES = {}
IP_ADDRESS = {}
tmp_file="file"
return_value = subprocess.call(["../backend/getRawStats.sh", tmp_file]);

interval = 5;
index=0
key = ""
value = ""
with open(tmp_file) as f:
	for line in f:
		lineArray = line.split("=");
		if (len(lineArray) == 2):
			key = lineArray[0];
			value = lineArray[1]
		
		if line.startswith("["):
			index = index + 1
		if index < 2:
			if key == "interval":
				interval = value;
		else:
			if key == "currBytes":
				CURR_BYTES[index] = value
			if key == "ipAddress":
				try:
					IP_ADDRESS[index] = socket.inet_ntoa(struct.pack('!L',int(value)))
				except Exception:
					pass
			if key == "totalBytes":
				TOTAL_BYTES[index] = value;

def bytes_to_bitrate(bytes, interval = 5):
	return ((int(bytes) * 8 / 1000) / int(interval))

results = []
for x in range(2, index):
	result = {}
	try:
		result["address"] = IP_ADDRESS[x];
		result["current_bitrate"] = bytes_to_bitrate(CURR_BYTES[x], interval);
		results.append(result)
	except Exception:
		pass
output = {};
output["time"] = str(time.time()).split(".")[0];
output["results"] = results;
print json.dumps(output);

# Delete tmp file
if os.path.isfile(tmp_file):
	os.remove(tmp_file);
