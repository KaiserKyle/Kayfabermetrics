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
    #input("Wrestler not found: " + name);
    return 0;

def getELO(wrestlerId):
    ratings = [x[2] for x in currentELO if x[0] == wrestlerId];
    if (len(ratings) != 0):
        return round(ratings[0]);
    else:
        return 1500;

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

queryString = "SELECT * FROM ELO_current";
cur.execute(queryString)
con.commit()
currentELO = cur.fetchall();

matches = [[["The Undertaker"], ["Brock Lesnar"]],
           [["Seth Rollins"],["Kane"]],
           [["Kevin Owens"],["Ryback"]],
           [["Nikki Bella"], ["Charlotte"]],
           [["Dolph Ziggler", "Antonio Cesaro", "Neville"],["Rusev", "Sheamus", "Wade Barrett"]],
           [["Bubba Ray Dudley","D-Von Dudley"],["Big E. Langston", "Kofi Kingston"]],
           [["Roman Reigns"],["Bray Wyatt"]]];

for match in matches:
    teamELOs = list();
    teamQs = list();
    for team in match:
        teamELO = 0;
        for person in team:
            id = getWrestlerId(person);
            elo = getELO(id);
            print (person + "(" + str(id) + "): " + str(elo));
            teamELO += elo;
        #print("Team ELO: " + str(teamELO));
        average = teamELO / len(team);
        Q = math.pow(10.0, (average / 400));
        print(" Average: " + str(average));
        #print(" Q: " + str(Q));
        teamELOs.append(average);
        teamQs.append(Q);
    totalELO = sum(teamELOs);
    totalQ = sum(teamQs);
    #print ("Total ELO: " + str(totalELO));
    #print("Total Q:" + str(totalQ));
    index = 0;
    for eachq in teamQs:
        winchance = eachq / totalQ;
        print(str(match[index]));
        print("Chance of winning: " + str(winchance));
        index += 1;
    print("Average ELO for match: " + str(totalELO / len(match)));
    print("");
    
    print("");
    print("<p style=\"font-size:32px;font-weight:bold;text-align:center\">Matchup</p>");
    print("<p style=\"font-size:28px;font-weight:bold;text-align:center;margin-top:0\">Title</p>");
    print("<p style=\"font-size:24px;padding:10px;margin:0\">Elo Ratings:</p>");
    print("<ul style=\"line-height:90%;margin:0;margin-left:40px;padding:0\">");
    print("<li></li>");
    print("<li><b>Average Match Elo: </b></li>");
    print("</ul>");
    print("<p style=\"font-size:24px;padding:10px;margin-top:40px;margin-bottom:0px\">Elo Breakdown:</p>");
    print("<p style=\"margin-left:40px;margin-bottom:10px\">");
    print("breakdown");
    print("<ul style=\"line-height:90%;margin:0;margin-left:80px;margin-bottom:10px;padding:0\">");
    print("<li></li>");
    print("</ul>");
    print("<strong style=\"font-size:22px;margin-top:10px\">Elo Prediction: </strong></p>");
    print("<p style=\"font-size:24px;padding:10px;margin-top:40px;margin-bottom:0px\">Author Breakdown:</p>");
    print("<p style=\"margin-left:40px;margin-bottom:10px\">");
    print("<strong style=\"font-size:22px;margin-top:10px\">Author's Prediction: </strong>");
    print("</p><hr>");  
    print("");
    print("");
    