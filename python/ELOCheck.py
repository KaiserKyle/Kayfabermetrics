import pymysql as mdb
import math
import statistics
import datetime
import time
import csv
from decimal import *
import json

def getWrestlerId(name):
    for wrestler in wrestlers:
        names = wrestler[1].split('; ');
        for wrestlername in names:        
            if name == wrestlername:
                return wrestler[0];
    input("Wrestler not found: " + name);
    return 0;

configDataFile=open('config.json')
configData = json.load(configDataFile)
configDataFile.close()

print ("Connecting")
con = mdb.connect(host=configData["host"], user=configData["username"], passwd=configData["password"], db=configData["database"])
print("Connected");
cur = con.cursor();

queryString = "SELECT ID, GROUP_CONCAT(Name ORDER BY IsPrimary DESC SEPARATOR '; ') FROM wrestlers_temp GROUP BY ID";
#queryString = "SELECT DISTINCT match_2 FROM wwematches2";

#print(queryString)
cur.execute(queryString)
con.commit()
wrestlers = cur.fetchall();

#for wrestler in wrestlers:
#    print(wrestler);

queryString = "SELECT _num, match_link AS Winner, match_2 AS Result, match_3_link AS Loser, titles AS Title, show_name, ppv, epochtime, match_type FROM wwematches2 WHERE show_name LIKE '%Monday Night Raw%' OR show_name LIKE '%SmackDown%' OR ppv = 'yes' ORDER BY epochtime ASC";
#queryString = "SELECT DISTINCT titles FROM wwematches2";
cur.execute(queryString);
con.commit();
matches = cur.fetchall();

queryString = "SELECT * FROM ELO_ratings";
cur.execute(queryString);
con.commit();
existingELO = cur.fetchall();

cur.close();
con.close();

#for match in matches:
#    print(match);
#quit();

# Smackdown, Raw, PPV, WrestleMania
# V1.0 Values: 10, 20, 40, 80
KValues = [15, 40, 80, 160];
print("K Values: " + str(KValues));
currentShowName = "";
currentShowTime = datetime.MINYEAR;
include = True;
currentKValue = 0;

ratings = dict();
databaseEntries = list();
newEntries = list();
winnerScores = list();

wins = 0;
losses = 0;

for match in matches:
    if 'WWE Live' in match[5]:
        continue;
    if 'dark' == match[8].lower():
        continue;
    if (currentShowName != match[5] and currentShowTime != time.localtime(match[7])):
        #print("Show Name: " + match[5]);
        #print("Date: " + time.strftime('%Y-%m-%d', time.localtime(match[7])));
        keypress = 'y';
        #if ('Live' in match[5]):
            #keypress = input("~~~~~~~~~~Include?");
        if ('y' == keypress):
            include = True;
        else:
            include = False;
        currentShowName = match[5];
        currentShowTime = time.localtime(match[7]);
        if ('WrestleMania' in match[5]):
            currentKValue = KValues[3];
        elif ('yes' == match[6]):
            currentKValue = KValues[2];
        elif ('Raw' in match[5]):
            currentKValue = KValues[1];
        else:
            currentKValue = KValues[0];
        #print('K Value: ' + str(currentKValue));
    if (not include):
        continue;
    matchid = match[0];
    #print("Match ID: " + str(matchid));
    winnerScore = 1;
    matchResult = "W";
    loserResult = "L";
    subResult = "pin";
    if "draw" in match[2]:
        winnerScore = 0.5;
        matchResult = "D";
        loserResult = "D";
        subResult = "draw";
    elif "sub" in match[2]:
        winnerScore = 1.2;
        subResult = "sub";
    elif "KO" in match[2]:
        winnerScore = 1.2;
        subResult = "KO";
    elif "DQ" in match[2]:
        winnerScore = 0.8;
        subResult = "DQ";
    #print(" Result weight: " + str(winnerScore));
    winners = match[1].replace('"', '').split('; ');
    losers = match[3].replace('"', '').split('; ');
    winnerRating = 0;
    loserRating = 0;
    for winner in winners:
        id = getWrestlerId(winner);
        if (id not in ratings.keys()):
            ratings[id] = 1500;
        winnerRating += ratings[id];
    for loser in losers:
        id = getWrestlerId(loser);
        if (id not in ratings.keys()):
            ratings[id] = 1500;
        loserRating += ratings[id];
    winnerRating = winnerRating / len(winners);
    loserRating = loserRating / len(losers);
    winnerAdv = (loserRating - winnerRating) / 400.0;
    expectedWinnerScore = 1 / (1 + 10 ** winnerAdv);
    scoreEntry = [expectedWinnerScore];
    if (expectedWinnerScore > 0.5):
        wins = wins + 1;
    else:
        losses = losses + 1;
    winnerScores.append(scoreEntry);
    pointChange = round(currentKValue * (winnerScore - expectedWinnerScore));
    newWinnerRating = winnerRating + pointChange;
    newLoserRating = loserRating - pointChange;
    
    #print(" Winning Team: " + match[1] + ", Average Rating: " + str(winnerRating) + ", Expected Score: " + str(expectedWinnerScore) + ", New Rating: " + str(newWinnerRating));
    #print(" Losing Team: " + match[3] + ", Average Rating: " + str(loserRating) + ", New Rating: " + str(newLoserRating));
    
    for winner in winners:
        id = getWrestlerId(winner);
        #print(" Wrestler: " + winner + " ID: " + str(id));
        #print("  Old Rating: " + str(ratings[id]));
        ratings[id] = ratings[id] + pointChange / len(winners);
        #print("  New Rating: " + str(ratings[id]));
        entry = [matchid, id, match[7], ratings[id], matchResult, subResult];
        #print("  Database entry: " + str(entry));
        databaseEntries.append(entry);
    for loser in losers:
        id = getWrestlerId(loser);
        #print(" Wrestler: " + loser + " ID: " + str(id));
        #print("  Old Rating: " + str(ratings[id]));
        ratings[id] = ratings[id] - pointChange / len(losers);
        #print("  New Rating: " + str(ratings[id]));
        entry = [matchid, id, match[7], ratings[id], loserResult, subResult];
        #print("  Database entry: " + str(entry));
        databaseEntries.append(entry);
        
print("Avg. Elo: " + str(statistics.mean(ratings.values())));

print("Correct Elo predictions: " + str(wins));
print("Incorrect Elo predictions: " + str(losses));

with open('ELO_database.csv', 'w', newline='') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerow(['matchid', 'wrestlerid', 'epochtime', 'rating', 'result', 'subresult']);
    a.writerows(databaseEntries);

with open('winner_scores.csv', 'w', newline='') as fp:
    a = csv.writer(fp, delimiter=',');
    a.writerows(winnerScores);

for w in sorted(ratings, key=ratings.get, reverse=True):
    for wrestler in wrestlers:
        if wrestler[0] == w:
            print(wrestler[1], end=" ");
    print(str(w) + ": " + str(round(ratings[w])));
