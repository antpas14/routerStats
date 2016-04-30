# routerStats
A simple script in python that allows to interrogate a router (TP Link TD-W8970) about Internet connection status

Tested with python 2.7.10

Usage:
- Copy the template file default.cfg and edit it with credentials and ip address of your router
- Call the script with the command:
	./router_stats.py -f <config-file>

The results are written (for now!) in a file called connection.txt in the same directory of the script
This file includes:
<Timestamp> <Downstream current rate> <upstream current rate> <SNR downstream> <SNR upstream>

To call it periodically (every five minutes) just add an entry in your cronjob file like this:
5 * * * * /home/myhome/routerStats/router_stats.py -f /home/myhome/routerStats/my_config.cfg
