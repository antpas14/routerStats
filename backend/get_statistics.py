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


