#!/bin/bash
# Tested on MySQL 5.5.54
# Creates a database for storing data 
. ../my_config.cfg # This file contains user credentials
# $user and $password are set from values in configuration file above

# Default MySQL credentials for root user are root/root. 
DEFAULT_MYSQL_USER=root
DEFAULT_MYSQL_PASS=root

# DB stuff
DB_NAME="routerstats"


# Create user
mysql -u $DEFAULT_MYSQL_USER -p${DEFAULT_MYSQL_PASS} -e "delete from mysql.db where db='${DB_NAME}'; DELETE FROM mysql.user WHERE User = '$user'; FLUSH PRIVILEGES; CREATE USER '$user'@'localhost' IDENTIFIED BY '${password}'"
# Create database
mysql -u $DEFAULT_MYSQL_USER -p${DEFAULT_MYSQL_PASS} -e "DROP DATABASE IF EXISTS $DB_NAME; CREATE DATABASE $DB_NAME; GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$user'@'localhost' with grant option;"

# Populate database
mysql -u $user -p${password} -D $DB_NAME -e 'DROP TABLE IF EXISTS stats; CREATE TABLE stats (id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, timestamp TIMESTAMP, data TEXT);'
