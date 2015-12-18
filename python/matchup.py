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

matches = [[["Big E. Langston", "Xavier Woods", "Kofi Kingston"],["Kalisto", "Sin Cara"],["Jimmy Uso", "Jey Uso"]],
           [["Charlotte"], ["Paige"]],
           [["Jack Swagger"], ["Alberto Del Rio"]],
           [["Dean Ambrose"], ["Kevin Owens"]],
           [["Bubba Ray Dudley", "D-Von Dudley", "Tommy Dreamer", "Rhyno"],["Bray Wyatt", "Luke Harper", "Braun Strowman", "Erick Rowan"]],
           [["Ryback"],["Rusev"]],
           [["Sheamus"], ["Roman Reigns"]]];

f = open('preview.txt', 'w');

for match in matches:
    teamELOs = list();
    teamQs = list();
    teamNames = list();
    for team in match:
        name = "";
        members = len(team);
        index = 0;
        teamELO = 0;
        for person in team:
            id = getWrestlerId(person);
            elo = getELO(id);
            print (person + "(" + str(id) + "): " + str(elo));
            teamELO += elo;
            name += person;
            if members == 2:
                if index == 0:
                    name += " and ";
            if members > 2:
                if index < members - 2:
                    name += ", ";
                if index == members - 2:
                    name += ", and ";
            index += 1;
        #print("Team ELO: " + str(teamELO));
        average = teamELO / len(team);
        Q = math.pow(10.0, (average / 400));
        print(" Average: " + str(average));
        #print(" Q: " + str(Q));
        teamELOs.append(average);
        teamQs.append(Q);
        teamNames.append(name);
    totalELO = sum(teamELOs);
    totalQ = sum(teamQs);
    #print ("Total ELO: " + str(totalELO));
    #print("Total Q:" + str(totalQ));
    index = 0;
    winningIndex = 0;
    winningPercent = 0;
    for eachq in teamQs:
        winchance = eachq / totalQ;
        print(str(match[index]));
        print("Chance of winning: " + str(winchance));
        if winchance > winningPercent:
            winningIndex = index;
            winningPercent = winchance;
        index += 1;
    print("Average ELO for match: " + str(totalELO / len(match)));
    print("");
    
    print("<p style=\"font-size:32px;font-weight:bold;text-align:center\">", end="", file=f);
    print(' vs. '.join(teamNames), end="", file=f);
    print("</p>", file=f);
    print("<p style=\"font-size:28px;font-weight:bold;text-align:center;margin-top:0\">Title</p>", file=f);
    print("<p style=\"font-size:24px;padding:10px;margin:0\">Elo Ratings:</p>", file=f);
    print("<ul style=\"line-height:90%;margin:0;margin-left:40px;padding:0\">", file=f);
    for x in range(0, len(teamNames)):
        print("<li>" + teamNames[x] + ": " + str(round(teamELOs[x])) + "</li>", file=f);
    print("<li><b>Average Match Elo: " + str(round(totalELO / len(match))) + "</b></li>", file=f);
    print("</ul>", file=f);
    print("<p style=\"font-size:24px;padding:10px;margin-top:40px;margin-bottom:0px\">Elo Breakdown:</p>", file=f);
    print("<p style=\"margin-left:40px;margin-bottom:10px\">", file=f);
    print("breakdown", file=f);
    print("<ul style=\"line-height:90%;margin:0;margin-left:80px;margin-bottom:10px;padding:0\">", file=f);
    print("<li></li>", file=f);
    print("</ul>", file=f);
    print("<strong style=\"font-size:22px;margin-top:10px\">Elo Prediction: ", end="", file=f);
    print(teamNames[winningIndex] + " (" + str(round(winningPercent * 100)) + "% chance of winning)", end="", file=f);
    print("</strong></p>", file=f);
    print("<p style=\"font-size:24px;padding:10px;margin-top:40px;margin-bottom:0px\">Author Breakdown:</p>", file=f);
    print("<p style=\"margin-left:40px;margin-bottom:10px\">", file=f);
    print("<strong style=\"font-size:22px;margin-top:10px\">Author's Prediction: </strong>", file=f);
    print("</p><hr>", file=f);  
    print("", file=f);
    
f.close();