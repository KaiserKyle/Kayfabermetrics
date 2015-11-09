import pymysql as mdb
import math
import statistics
import datetime
import time
import collections
import csv
import json

def getWrestlerId(name):
    for wrestler in wrestlers:
        names = wrestler[1].split('; ');
        for wrestlername in names:        
            if name == wrestlername:
                return wrestler[0];
    
    return 0;

def printWrestle(rating):
    name = "";
    for wrestler in wrestlers:
        if wrestler[0] == rating[1]:
            print(wrestler[1], end=" ");
            name = wrestler[1];
    print(time.strftime('%Y-%m-%d', time.localtime(rating[2]))+ " (" + str(rating[1]) +"): " + str(round(rating[3])));
    return name;

def updateRankingDb(cur, wrestlerid, epochtime, rating):
    queryString = "UPDATE ELO_current SET epochtime=" + str(epochtime) + ", rating=" + str(rating) + " WHERE wrestlerid=" + str(wrestlerid);
    cur.execute(queryString);
    
def updateTopDb(cur, toplist, rank, wrestlerid, epochtime, rating, name):
    queryString = "UPDATE toplists SET wrestlerid=" + str(wrestlerid) + ", epochtime=" + str(epochtime) + ", rating=" + str(rating) + ", name=\"" + name + "\" WHERE toplist='" + toplist + "' AND rank=" + str(rank);
    cur.execute(queryString);
    
def insertTopDb(cur, toplist, rank, wrestlerid, epochtime, rating, name):
    queryString = "INSERT INTO toplists VALUE ('" + toplist + "'," + str(rank) + "," + str(wrestlerid) + "," + str(epochtime) + "," + str(rating) + ",\"" + name + "\");";
    print(queryString);
    cur.execute(queryString);

thirtydays = datetime.timedelta(days=30);
thirtydaysbeforetoday = datetime.datetime.now() - thirtydays;
finalthirty = time.mktime(thirtydaysbeforetoday.timetuple());
ninteydaysbefore = thirtydaysbeforetoday - thirtydays - thirtydays;
finalninety = time.mktime(ninteydaysbefore.timetuple());

configDataFile=open('config.json')
configData = json.load(configDataFile)
configDataFile.close()

print ("Connecting")
con = mdb.connect(host=configData["host"], user=configData["username"], passwd=configData["password"], db=configData["database"])
print("Connected");
cur = con.cursor();

queryString = "SELECT ID, Name FROM wrestlers_temp WHERE IsPrimary=1 GROUP BY ID";
cur.execute(queryString)
con.commit()
wrestlers = cur.fetchall();

queryString = "SELECT * FROM (SELECT * FROM ELO_ratings ORDER BY wrestlerid, epochtime DESC) x GROUP BY wrestlerid ORDER BY rating DESC";
cur.execute(queryString);
con.commit();
currentRatings = cur.fetchall();

queryString = "SELECT * FROM (SELECT * FROM ELO_ratings WHERE epochtime > " + str(finalthirty) + " ORDER BY wrestlerid, epochtime DESC) x GROUP BY wrestlerid ORDER BY rating DESC";
cur.execute(queryString);
con.commit();
last30days = cur.fetchall();

queryString = "SELECT * FROM (SELECT * FROM ELO_ratings WHERE epochtime < " + str(finalthirty) + " ORDER BY wrestlerid, epochtime DESC) x GROUP BY wrestlerid ORDER BY rating DESC";
cur.execute(queryString);
con.commit();
thirtydaysago = cur.fetchall();

queryString = "SELECT * FROM (SELECT * FROM ELO_ratings WHERE epochtime > " + str(finalninety) + " ORDER BY wrestlerid, epochtime DESC) x GROUP BY wrestlerid ORDER BY rating DESC";
cur.execute(queryString);
con.commit();
last90days = cur.fetchall();

cur.close();
con.close();

toptenthirtydays = list();
toptenninetydays = list();
toptenalltime = list();
bottomtenninetydays = collections.deque();
bottomtenalltime = collections.deque();
databaseEntries = list();
newDatabaseEntries = list();
allEntries = list();
allDatabase = list();

for rating in currentRatings:
    allEntries.append(rating);
    if (len(toptenalltime) < 10):
        toptenalltime.append(rating);
    if (rating[2] > finalthirty and len(toptenthirtydays) < 10):
        toptenthirtydays.append(rating);
    if (rating[2] > finalninety):
        if (len(toptenninetydays) < 10):
            toptenninetydays.append(rating);
        bottomtenninetydays.append(rating);
        if (len(bottomtenninetydays) == 11):
            bottomtenninetydays.popleft();
    bottomtenalltime.append(rating);
    if (len(bottomtenalltime) == 11):
        bottomtenalltime.popleft();

last30dayschange = list();

for rating in last30days:
    oldRatingList = [x for x in thirtydaysago if rating[1] == x[1]];
    oldRating = 1500;
    if (len(oldRatingList) != 0):
        oldRating = oldRatingList[0][3];
    name = printWrestle(rating);
    #print("30 days ago: " + str(oldRating));
    change = round(rating[3] - oldRating);
    #print("Change: " + str(change));
    entry = [rating[1], rating[2], change, name];
    #print(entry);
    last30dayschange.append(entry);
last30dayschange.sort(key=lambda tup: tup[2], reverse=True);

print();
print("Active in last 90 days");
for rating in last90days:
    name = printWrestle(rating);

biggestgainers = last30dayschange[0:10];
biggestlosers = list(reversed(last30dayschange[-10:]));

print();
print ("Biggest Gainers");
index = 1;
for rating in biggestgainers:
    print(rating);
    entry = ["toptenbiggestgainer", index, rating[0], rating[1], rating[2], rating[3]];
    databaseEntries.append(entry);
    index += 1;
print();
print ("Biggest Losers");
index = 1;
for rating in biggestlosers:
    print(rating);
    entry = ["toptenbiggestlosers", index, rating[0], rating[1], rating[2], rating[3]];
    databaseEntries.append(entry);
    index += 1;
    
bottomtenalltime.reverse();
bottomtenninetydays.reverse();
print("");
print("Top ten last thirty days");
index = 1;
for rating in toptenthirtydays:
    name = printWrestle(rating);
    entry = ["toptenthirtydays", index, rating[1], rating[2], rating[3], name];
    databaseEntries.append(entry);
    index += 1;
index = 1;
print("");
print("Top ten last thirty days query");
for rating in last30days:
    name = printWrestle(rating);
    index += 1;
    if (11 == index):
        break;
index = 1;
print("");
print("Top ten last ninety days");
for rating in toptenninetydays:
    name = printWrestle(rating);
    entry = ["toptenninetydays", index, rating[1], rating[2], rating[3], name];
    databaseEntries.append(entry);
    index += 1;
index = 1;
print("");
print("Top ten all time");
for rating in toptenalltime:
    name = printWrestle(rating);
    entry = ["toptenalltime", index, rating[1], rating[2], rating[3], name];
    databaseEntries.append(entry);
    index += 1;
index = 1;
print("");
print("Bottom ten all time");
for rating in bottomtenalltime:
    name = printWrestle(rating);
    entry = ["bottomtenalltime", index, rating[1], rating[2], rating[3], name];
    databaseEntries.append(entry);
    index += 1;
index = 1;
print("");
print("Bottom ten last ninety days");
for rating in bottomtenninetydays:
    name = printWrestle(rating);
    entry = ["bottomtenninetydays", index, rating[1], rating[2], rating[3], name];
    databaseEntries.append(entry);
    index += 1;
    
con = mdb.connect(host=configData["host"], user=configData["username"], passwd=configData["password"], db=configData["database"]);
cur = con.cursor();    
for rating in allEntries:
    index += 1;
    updateRankingDb(cur, rating[1], rating[2], rating[3]);
for entry in databaseEntries:
    index += 1;
    updateTopDb(cur, entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]);
for entry in newDatabaseEntries:
    insertTopDb(cur, entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]);
con.commit();
cur.close();
con.close();
