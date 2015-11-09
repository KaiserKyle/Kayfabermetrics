#!/usr/bin/env python

import pymysql as mdb
from optparse import OptionParser
import json
import urllib.request, urllib.error, urllib.parse
import urllib.request, urllib.parse, urllib.error
import sys
import zlib
import time


def getRequiredConfigData(configData, configName):
	if configData[configName] is None:
		print(("Missing required option: " + configName))
		print("This option needs to be in a config file, or supplied on the commandline")
		sys.exit(1)

def getOptionalConfigData(configData, configName, default):
	if default is not None and configName not in configData:
		configData[configName] = default

def getConfigOptions(configData): 

	#print(configData)

	# Get required config data
	getRequiredConfigData(configData, "sourceUUID")
	getRequiredConfigData(configData, "table")
	getRequiredConfigData(configData, "database")

	getRequiredConfigData(configData, "ioUserID")
	getRequiredConfigData(configData, "ioAPIKey")
	getRequiredConfigData(configData, "inputUrl")

	# Grab optional configuration parameters, use defaults if they don't exist
	getOptionalConfigData(configData, "host", "localhost")
	getOptionalConfigData(configData, "port", 3306)
	getOptionalConfigData(configData, "username", None)
	getOptionalConfigData(configData, "password", None)
	getOptionalConfigData(configData, "crawl", False);

	return configData

# Grab the data from a crawler snapshot
def grabFromCrawlSnapshot(sourceUUID, ioUserID, ioAPIKey):
	urlAuthParams = urllib.parse.urlencode({"_user": ioUserID, "_apikey": ioAPIKey})

	connectorUrl = 'https://api.import.io/store/data/' + sourceUUID + "?" + urlAuthParams
	connectorResponse = json.loads(urllib.request.urlopen(connectorUrl).read())
	snapshotGuid = connectorResponse["snapshot"]

	#Have to use gzip encoding for this
	request = urllib.request.Request('https://api.import.io/store/data/' + sourceUUID + "/_attachment/snapshot/" + snapshotGuid + "?" + urlAuthParams)
	request.add_header('Accept-encoding', 'gzip')
	response = urllib.request.urlopen(request)
	snapshotResponse = json.loads(zlib.decompress(response.read(), 16+zlib.MAX_WBITS))

	crawledPages = snapshotResponse["tiles"][0]["results"][0]["pages"]

	results = []

	for page in crawledPages:
		results.extend(page["results"])

	return results
	

# Grab the data from import.io
def importRESTQuery(sourceUUID, inputUrl, ioUserID, ioAPIKey):
	urlParams = urllib.parse.urlencode({"input/webpage/url": inputUrl, "_user": ioUserID, "_apikey": ioAPIKey})
	url = 'https://api.import.io/store/data/' + sourceUUID + '/_query?' + urlParams

	response = urllib.request.urlopen(url).read().decode('utf-8')
	jsonresponse = json.loads(response);
	#print (jsonresponse);
	return jsonresponse["results"];

# Convert the data to a reasonable format and stick it in SQL
def pushToSQL(configData, results):

	fieldMappings = None

	if "mapping" in configData:
		fieldMappings = configData["mapping"]
		sqlFieldMapping = [];

		for mapping in fieldMappings:
			sqlFieldMapping.append(fieldMappings[mapping])

		sqlFieldMappingString = ", ".join(sqlFieldMapping)
		#print (sqlFieldMappingString)

		#print(("Mappings: %s" % fieldMappings))


	con = None
	try:
		eventno = configData["inputUrl"].split('-');
		eventno = eventno[-1].split('.');
		eventno = eventno[0];
		
		print("Parsing event number " + eventno);
						
		#print ("Connecting")
		con = mdb.connect(host=configData["host"], user=configData["username"], passwd=configData["password"], db=configData["database"])
		#print("Connected");
		cur = con.cursor()
		
		for result in results:
			values = []
			if(fieldMappings is not None):
				# Get the values for each row based on the mapping that we supplied in config.json
				for mapping in fieldMappings:
					if result[mapping] is not None:
						values.append("'"+result[mapping]+"'")
			else:
				# Get the values from the import.io source (assume the field names are identical)
				sqlFieldMapping = [];
				for key in result:
					if (type(result[key]) is str):
						result[key] = result[key].replace('"','')
					if (key == "no_number"):
						continue;
					if (key == "no_number/_source"):
						sqlFieldMapping.append("no_number")
						values.append("\""+result[key]+"\"")
					elif (key == "dateurl"):
						sqlFieldMapping.append("dateurl")
						sqlFieldMapping.append("datestring");
						sqlFieldMapping.append("epochtime")
						dateurl = result[key];
						date = dateurl.split('/');
						date = date[-1].split('.');
						datenumber = time.strptime(date[0], "%m-%d-%Y")
						epochtime = time.mktime(datenumber);
						values.append("\""+ dateurl +"\"")
						values.append("\""+ date[0] +"\"")
						values.append("\""+ str(epochtime) +"\"")
					else:
						sqlFieldMapping.append(key.replace("/_","_"))
						if (type(result[key]) is list):
							values.append("\"" + "; ".join(result[key]).replace('"','') + "\"")
						else:
							values.append("\""+result[key]+"\"")
				if "titles" not in sqlFieldMapping:
					sqlFieldMapping.append("titles");
					values.append("\"\"")
				if "match_type" not in sqlFieldMapping:
					sqlFieldMapping.append("match_type");
					values.append("\"\"")
				if "duration" not in sqlFieldMapping:
					sqlFieldMapping.append("duration");
					values.append("\"\"")
				if "_pageUrl" not in sqlFieldMapping:
					sqlFieldMapping.append("_pageUrl");
					sqlFieldMapping.append("event_no");
					values.append("\""+ configData["inputUrl"] +"\"")
					values.append("\"" + eventno + "\"")
				sqlFieldMappingString = ", ".join(sqlFieldMapping)

			sqlFieldValuesString = ", ".join(values)
			#print(("row data: %s" % sqlFieldValuesString))
			wrestler1 = result["match_link"];
			wrestler2 = result["match_3_link"];
			if (type(wrestler1) is list):
				wrestler1 = "; ".join(wrestler1);
			if (type(wrestler2) is list):
				wrestler2 = "; ".join(wrestler2);
			
			print(wrestler1 +  " " + result["match_2"] + " " + wrestler2);

			queryString = "INSERT INTO " + configData["table"] + " (" + sqlFieldMappingString + ") VALUES("+sqlFieldValuesString+");"

			#print(queryString)
			cur.execute(queryString)
			con.commit()

		cur.close()

		#print(("%s"  % (configData["host"])))

	except (RuntimeError, TypeError, NameError, mdb.Error) as e:
		print(e);
	finally:
		if con:
			con.rollback()
			con.close()
		#sys.exit(1)
		
def checkIfExists(configData):
	eventno = configData["inputUrl"].split('-');
	eventno = eventno[-1].split('.');
	eventno = eventno[0];
	con = mdb.connect(host=configData["host"], user=configData["username"], passwd=configData["password"], db=configData["database"])
	cur = con.cursor()
	queryString = "SELECT * FROM " + configData["table"] + " WHERE event_no=" + eventno;
	#print(queryString)
	cur.execute(queryString)
	con.commit()
	
	rows = cur.fetchall();
	cur.close();
	con.close();
	
	if (0 != len(rows)):
		print("Event already uploaded!");
		return False;
	else:
		print ("New event!");
		return True;

def checkIfEventExists(configData, table, eventno):
	con = mdb.connect(host=configData["host"], user=configData["username"], passwd=configData["password"], db=configData["database"])
	cur = con.cursor()
	queryString = "SELECT * FROM " + table + " WHERE event_no=" + eventno;
	#print(queryString)
	cur.execute(queryString)
	con.commit()
	
	rows = cur.fetchall();
	cur.close();
	con.close();
	
	if (0 != len(rows)):
		print("Event already uploaded!");
		return False;
	else:
		print ("New event!");
		return True;
	
def getEventNumbers(configData, table):
	con = mdb.connect(host=configData["host"], user=configData["username"], passwd=configData["password"], db=configData["database"])
	cur = con.cursor()
	queryString = "SELECT DISTINCT event_no FROM " + table;
	#print(queryString)
	cur.execute(queryString)
	con.commit()
	
	rows = cur.fetchall();
	cur.close();
	con.close();
	
	return rows;

def doImport(configData):
	if (checkIfExists(configData) == False):
		return;

	if configData["crawl"] == True:
		results = grabFromCrawlSnapshot(configData["sourceUUID"], configData["ioUserID"], configData["ioAPIKey"])
	else:
		results = importRESTQuery(configData["sourceUUID"], configData["inputUrl"], configData["ioUserID"], configData["ioAPIKey"]);
	print(("Recieved %d rows of data" % (len(results))))
	pushToSQL(configData, results)

def importUrl(url):
	try:
		configDataFile=open('config.json')
		configData = json.load(configDataFile)
		configDataFile.close()
		#print ("CONFIG FOUND, YAY!")
	except IOError:
		print(('NO CONFIG FILE FOUND, going to use defaults', 'config.json'))
	
	configData = getConfigOptions(configData)
	configData["inputUrl"] = url;
	doImport(configData)