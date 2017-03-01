#!/usr/bin/python

import sqlalchemy;
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json
#e = create_engine("mysql://admin:RP1H0m3s3rv3r@localhost/routerstats", connect_args={"encoding": "utf8"})
e = create_engine('mysql+mysqldb://admin:RP1H0m3s3rv3r@localhost/routerstats', pool_recycle=3600)
Base = declarative_base()

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")
class Stats(Base):
	__tablename__ = 'stats'

	id = Column(Integer, primary_key=True)
	timestamp = Column(DateTime)
	data = Column(String);
	def __repr__(self):
		return "<User(timestamp='%s', data='%s')>" % (
		self.timestamp, self.data)


Session = sessionmaker(bind=e)
session = Session()

timestamps = []
map = {}
for instance in session.query(Stats).filter(Stats.timestamp >= '2017-02-17').order_by(Stats.id.desc()).limit(20):
	timestamps.append(instance.timestamp)
	dictionary = json.loads(instance.data);	
	results = dictionary["results"];
	for e in results:
		if not e["address"] in map:
			map[e["address"]] = []
		element = []
		element.append(instance.timestamp);
		element.append(e["current_bitrate"]);
		map[e["address"]].append(element);

output = {}
#output['title'] = {}
#output['title']['text'] = "AAA"
#output['title']['subtext'] = "BBB"

output['tooltip'] = {}
output['tooltip']['trigger'] = 'axis'

#output['legend'] = {}
#output['legend']['data'] = map.keys();

output['calculable'] = 'true';
output['xAxis'] = {}
output['xAxis']['type'] = 'time' 

output['yAxis'] = {}
output['series'] = []
for name in map.keys():
	elementSeries = {}
	elementSeries['name'] = name;
	elementSeries['type'] = 'line';
	elementSeries['data'] = map[name];
	output['series'].append(elementSeries);
print json.dumps(output, default=json_serial);

