
from pydoc import render_doc
from tokenize import Double
from flask import Flask
from flask import render_template, request, redirect
import MySQLdb


app = Flask(__name__)

pas=''
dbName=''

def getLeagues():
    conn = MySQLdb.connect(host='localhost', user='root', passwd=pas, db=dbName)
    cur = conn.cursor()
    cur.execute("select name from leagues")
    res = cur.fetchall()
    l = []
    for line in res:
        for n in line:
            l.append(n)
    cur.close()
    conn.close()
    return l

def getSingleGameTypes():
    conn = MySQLdb.connect(host='localhost', user='root', passwd=pas, db='MJ')
    cur = conn.cursor()
    cur.execute("select name from gameTypes")
    res = cur.fetchall()
    l = []
    for line in res:
        for n in line:
            l.append(n)
    cur.close()
    conn.close()
    return l

def addLeague(name, team1, team2, team3, team4):
    conn = MySQLdb.connect(host='localhost', user='root', passwd=pas, db=dbName)
    cur = conn.cursor()
    cur.execute(f"insert into leagues(name, teamName1, teamName2, teamName3, teamName4) values('{name}','{team1}','{team2}','{team3}','{team4}')")
    conn.commit()
    cur.execute(f"create table {name} (id int auto_increment, num INT, team1 text, player1 text, team2 text, player2 text, team3 text, player3 text, team4 text, player4 text, point1 int, point2 int, point3 int, point4 int, p1 float, p2 float, p3 float, p4 float, primary key (id)) DEFAULT CHARSET=utf8")
    conn.commit()
    cur.close()
    conn.close()

def addTeam(league, name, player1, player2, player3):
    conn = MySQLdb.connect(host='localhost', user='root', passwd=pas, db=dbName)
    cur = conn.cursor()
    cur.execute(f"insert into teams(league, name, playerName1, playerName2, playerName3) values('{league}', '{name}','{player1}','{player2}','{player3}')")
    conn.commit()
    cur.close()
    conn.close()

def addNewGame(leagueName, team1, player1, team2, player2, team3, player3, team4, player4, point1, point2, point3, point4,p1,p2,p3,p4):
    conn = MySQLdb.connect(host='localhost', user='root', passwd=pas, db=dbName)
    cur = conn.cursor()
    cur.execute(f"insert into {leagueName}(team1,player1,team2,player2,team3,player3,team4,player4,point1,point2,point3,point4,p1,p2,p3,p4) values('{team1}','{player1}','{team2}','{player2}','{team3}','{player3}','{team4}','{player4}',{str(point1)},{str(point2)},{str(point3)},{str(point4)},{str(p1)},{str(p2)},{str(p3)},{str(p4)})")
    conn.commit()
    cur.close()
    conn.close()

def addNewGameSingle(type, player1, player2, player3, player4, point1, point2, point3, point4,p1,p2,p3,p4):
    conn = MySQLdb.connect(host='localhost', user='root', passwd=pas, db=dbName)
    cur = conn.cursor()
    cur.execute(f"insert into Single(gameType,player1,player2,player3,player4,point1,point2,point3,point4,p1,p2,p3,p4) values('{type}','{player1}','{player2}','{player3}','{player4}',{str(point1)},{str(point2)},{str(point3)},{str(point4)},{str(p1)},{str(p2)},{str(p3)},{str(p4)})")
    conn.commit()
    cur.close()
    conn.close()

def addNewGameType(name):
    conn = MySQLdb.connect(host='localhost', user='root', passwd=pas, db=dbName)
    cur = conn.cursor()
    cur.execute(f"insert into gameTypes(name) values('{name}')")
    conn.commit()
    cur.close()
    conn.close()

def fixPoint(point, order):
    if order == 1:
        p = point/1000 + 5
    elif order == 2:
        p = point/1000 -15
    elif order == 3:
        p = point/1000 -35
    elif order == 4:
        p = point/1000 -55
    return round(p,1)

def selectLeagueGame(league):
   
    conn = MySQLdb.connect(host='localhost', user='root', passwd=pas, db=dbName)
    cur = conn.cursor()
   
    cur.execute(f"select * from {league}")
    games = cur.fetchall()
    gamesInfo = []
    for g in games:
        i = {
            "name": g[0],
            "team1": g[2],
            "player1": g[3],
            "team2": g[4],
            "player2": g[5],
            "team3": g[6],
            "player3": g[7],
            "team4": g[8],
            "player4": g[9],
            "point1": g[10],
            "point2": g[11],
            "point3": g[12],
            "point4": g[13],
            "p1": g[14],
            "p2": g[15],
            "p3": g[16],
            "p4": g[17],
        }
        gamesInfo.append(i)
   
    cur.close()
    conn.close()
   
    return gamesInfo

def selectSingleGame(type):
   
    conn = MySQLdb.connect(host='localhost', user='root', passwd=pas, db=dbName)
    cur = conn.cursor()
   
    cur.execute(f"select * from Single where gameType = '{type}'")
    games = cur.fetchall()
    gamesInfo = []
    j = 1
    for g in games:
        i = {
            "name": j,
            "type": g[1],
            "player1": g[2],
            "player2": g[3],
            "player3": g[4],
            "player4": g[5],
            "point1": g[6],
            "point2": g[7],
            "point3": g[8],
            "point4": g[9],
            "p1": g[10],
            "p2": g[11],
            "p3": g[12],
            "p4": g[13],
        }
        j += 1
        gamesInfo.append(i)
   
    cur.close()
    conn.close()
   
    return gamesInfo

def playerScore(player, league):
    conn = MySQLdb.connect(host='localhost', user='root', passwd=pas, db=dbName)
    cur = conn.cursor()
    s = 0
    for i in range(1,5):
        cur.execute(f"select sum(p{str(i)}) from {league} where player{str(i)} = '{player}'")
        score = cur.fetchall()[0][0]
        if score != None:
            s += score
    sFix = round(s,1)
    cur.close()
    conn.close()
    return sFix

def teamScore(team,league):
    conn = MySQLdb.connect(host='localhost', user='root', passwd=pas, db=dbName)
    cur = conn.cursor()
    s = 0
    for i in range(1,5):
        cur.execute(f"select sum(p{str(i)}) from {league} where team{str(i)} = '{team}'")
        score = cur.fetchall()[0][0]
        if score != None:
            s += score
    sFix = round(s,1)
    cur.close()
    conn.close()
    return sFix

def playerTeam(player, league):
    conn = MySQLdb.connect(host='localhost', user='root', passwd=pas, db=dbName)
    cur = conn.cursor()
    for i in range(1,4):
        cur.execute(f"select name from teams where  playerName{i} = '{player}' and league = '{league}'")
        team = cur.fetchall()
        if len(team) != 0:
            t = (team[0][0])
            break
    cur.close()
    conn.close()
    return t

def getPlayers(league):
    conn = MySQLdb.connect(host='localhost', user='root', passwd=pas, db=dbName)
    cur = conn.cursor()
    pList = []
    cur.execute(f"select playerName1, playerName2, playerName3 from teams where league = '{league}'")
    player = cur.fetchall()
    for i in player:
        for x in i:
            pList.append(x)
    cur.close()
    conn.close()
    return pList

def getPlayersSingle(type):
    conn = MySQLdb.connect(host='localhost', user='root', passwd=pas, db=dbName)
    cur = conn.cursor()
    pList = []
    for j in range(1,5):
        cur.execute(f"select distinct(player{j}) from Single where gameType = '{type}'")
        player1 = cur.fetchall()
        for i in player1:
            for x in i:
                pList.append(x)
    s = set(pList)
    cur.close()
    conn.close()
    return list(s)

def getTeams(league):
    conn = MySQLdb.connect(host='localhost', user='root', passwd=pas, db=dbName)
    cur = conn.cursor()
    teams = []
    cur.execute(f"select name from teams where league = '{league}'")
    res = cur.fetchall()
    for i in res:
        for x in i:
            teams.append(x)
    cur.close()
    conn.close()
    return teams

def playersOfATeam(team, league):
    conn = MySQLdb.connect(host='localhost', user='root', passwd=pas, db=dbName)
    cur = conn.cursor()
    p = []
    cur.execute(f"select playerName1, playerName2, playerName3 from teams where name  = '{team}' and league = '{league}'")
    player1 = cur.fetchall()
    for i in player1:
        for x in i:
            p.append(x)
    cur.close()
    conn.close()
    return p

def numOfOrder(player, league):
    conn = MySQLdb.connect(host='localhost', user='root', passwd=pas, db=dbName)
    cur = conn.cursor()
    orders=[]
    for i in range(1,5):
        cur.execute(f"select point{i} from {league} where player{i} = '{player}'")
        res = cur.fetchall()
        orders.append(len(res))
    cur.close()
    conn.close()
    return orders

def maxPoint(player, league):
    conn = MySQLdb.connect(host='localhost', user='root', passwd=pas, db=dbName)
    cur = conn.cursor()
    for i in range(1,5):
        cur.execute(f"select max(point{i}) from {league} where player{i} = '{player}'")
        res = cur.fetchall()
        if res[0][0] != None:
            break
    cur.close()
    conn.close()
    return res[0][0]

def minPoint(player, league):
    conn = MySQLdb.connect(host='localhost', user='root', passwd=pas, db=dbName)
    cur = conn.cursor()
    for i in range(4,0,-1):
        cur.execute(f"select min(point{i}) from {league} where player{i} = '{player}'")
        res = cur.fetchall()
        if res[0][0] != None:
            break
    cur.close()
    conn.close()
    return res[0][0]

class player:
    def __init__(self, name, team, point, pointMax, pointMin, num1, num2, num3, num4):
        self.name = name
        self.team = team
        self.point = point
        self.pointMax = pointMax
        self.pointMin = pointMin
        self.num1 = num1
        self.num2 = num2
        self.num3 = num3
        self.num4 = num4

    def timesOfGame(self):
        return self.num1+self.num2+self.num3+self.num4

    def averageOrder(self):
        n1 = self.num1
        n2 = self.num2
        n3 = self.num3
        n4 = self.num4
        sum = (n1+n2*2+n3*3+n4*4)/(n1+n2+n3+n4)
        return round(sum,2)

    def portionOfOrder(self, i):
        n1 = self.num1
        n2 = self.num2
        n3 = self.num3
        n4 = self.num4
        if i == 1:
            target = n1
        elif i == 2:
            target = n2
        elif i == 3:
            target = n3
        elif i == 4:
            target = n4
        ans = target/(n1+n2+n3+n4)*100
        return round(ans,1)

    def averagePoint(self):
        n1 = self.num1
        n2 = self.num2
        n3 = self.num3
        n4 = self.num4
        sum = self.point/(n1+n2+n3+n4)
        return round(sum,1)

class team:
    def __init__(self, name, p1, p2, p3, point):
        self.name = name
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.point = point

    

def sortBy(arr, type):
    change = True
    while change:
        change = False
        if type == "point":
            for i in range(len(arr) - 1):
                if arr[i].point < arr[i + 1].point:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    change = True
        elif type == "max":
            for i in range(len(arr) - 1):
                if arr[i].pointMax < arr[i + 1].pointMax:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    change = True
        elif type == "min":
            for i in range(len(arr) - 1):
                if arr[i].pointMin > arr[i + 1].pointMin:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    change = True
        elif type == "ave":
            for i in range(len(arr) - 1):
                if arr[i].averageOrder() > arr[i + 1].averageOrder():
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    change = True
        elif type == "aveP":
            for i in range(len(arr) - 1):
                if arr[i].averagePoint() < arr[i + 1].averagePoint():
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    change = True

    return arr

def createPObjects(list, league, type):
    playerObjects = []
    for p in list:
        orders = numOfOrder(p,league)
        playerx = player(p,playerTeam(p,league), playerScore(p,league), maxPoint(p,league), minPoint(p,league), orders[0], orders[1], orders[2], orders[3])
        if playerx.timesOfGame() != 0:
            playerObjects.append(playerx)
    return sortBy(playerObjects, type)

def createPObjectsSingle(list, type):
    playerObjects = []
    for p in list:
        orders = numOfOrder(p,"Single")
        playerx = player(p,None, playerScore(p,"Single"), maxPoint(p,"Single"), minPoint(p,"Single"), orders[0], orders[1], orders[2], orders[3])
        playerObjects.append(playerx)
    return sortBy(playerObjects, type)

def createTObjects(list, league):
    teamObjects = []
    for t in list:
        p = playersOfATeam(t,league)
        teamx = team(t,p[0],p[1],p[2],teamScore(t,league))
        if teamx.point != None:
            teamObjects.append(teamx)
    return teamObjects



@app.route("/")
def hello():
    leagueList = getLeagues()
    singleList = getSingleGameTypes()
    return render_template('hello.html', leagueList=leagueList, singleList=singleList)

@app.route("/games/<leagueName>")
def games(leagueName):
    gamesInfo = selectLeagueGame(leagueName)
    playersList = getPlayers(leagueName)
    return render_template('games.html', gamesInfo=gamesInfo, leagueName=leagueName, playersList=playersList)

@app.route("/score/<leagueName>")
def score(leagueName):
    playersList = getPlayers(leagueName)
    teamsList = getTeams(leagueName)
    players = createPObjects(playersList,leagueName,"point")
    playersMax = createPObjects(playersList,leagueName,"max")
    playersAve = createPObjects(playersList,leagueName,"min")
    teams = createTObjects(teamsList,leagueName)
    teams = sortBy(teams, "point")
    return render_template('score.html', players=players, teams=teams, leagueName=leagueName, playersMax=playersMax, playersAve=playersAve)

@app.route("/games/<leagueName>/<playerName>")
def gamesSelected(leagueName,playerName):
    playersList = getPlayers(leagueName)
    gamesInfo = selectLeagueGame(leagueName)
    return render_template('games_selected.html', playerName=playerName, gamesInfo=gamesInfo, leagueName=leagueName, playersList=playersList)


@app.route("/create/<leagueName>", methods = ["GET", "POST"])
def create(leagueName):
    error = 0
    teamList = getTeams(leagueName)
    teams = createTObjects(teamList, leagueName)
    players =  getPlayers(leagueName)
    if request.method == "POST":
        team1 = request.form.get("team1")
        player1 = request.form.get("player1")
        team2 = request.form.get("team2")
        player2 = request.form.get("player2")
        team3 = request.form.get("team3")
        player3 = request.form.get("player3")
        team4 = request.form.get("team4")
        player4 = request.form.get("player4")
        point1 = request.form.get("point1")
        point2 = request.form.get("point2")
        point3 = request.form.get("point3")
        point4 = request.form.get("point4")
        p1 = fixPoint(int(point1),1)
        p2 = fixPoint(int(point2),2)
        p3 = fixPoint(int(point3),3)
        p4 = fixPoint(int(point4),4)
        if p1+p2+p3+p4 == 0:
            addNewGame(leagueName,team1,player1,team2,player2,team3,player3,team4,player4,point1,point2,point3,point4,p1,p2,p3,p4)
            return redirect(f"/score/{leagueName}")
        else:
            error = 1
            return render_template('create.html', leagueName=leagueName, error=error, teams=teams, players=players)
    else:
        return render_template('create.html', leagueName=leagueName, error=error, teams=teams, players=players)

@app.route("/create/newLeague", methods = ["GET", "POST"])
def createLeague():
    if request.method == "POST":
        league = request.form.get("league")
        team1 = request.form.get("team1")
        team2 = request.form.get("team2")
        team3 = request.form.get("team3")
        team4 = request.form.get("team4")
        player1_1 = request.form.get("t1player1")
        player1_2 = request.form.get("t1player2")
        player1_3 = request.form.get("t1player3")
        player2_1 = request.form.get("t2player1")
        player2_2 = request.form.get("t2player2")
        player2_3 = request.form.get("t2player3")
        player3_1 = request.form.get("t3player1")
        player3_2 = request.form.get("t3player2")
        player3_3 = request.form.get("t3player3")
        player4_1 = request.form.get("t4player1")
        player4_2 = request.form.get("t4player2")
        player4_3 = request.form.get("t4player3")
        addLeague(league,team1,team2,team3,team4)
        addTeam(league, team1, player1_1,player1_2,player1_3)
        addTeam(league, team2, player2_1,player2_2,player2_3)
        addTeam(league, team3, player3_1,player3_2,player3_3)
        addTeam(league, team4, player4_1,player4_2,player4_3)
        return redirect("/")
    else:
        return render_template('create_league.html')

@app.route("/games/single/<gameType>")
def gamesSingle(gameType):
    playersList = getPlayersSingle(gameType)
    gamesInfo = selectSingleGame(gameType)
    return render_template('games_single.html', gamesInfo=gamesInfo, gameType=gameType, playersList=playersList)

@app.route("/games/single/<gameType>/<playerName>")
def gamesSingleSelected(gameType, playerName):
    playersList = getPlayersSingle(gameType)
    gamesInfo = selectSingleGame(gameType)
    return render_template('games_single_selected.html', gamesInfo=gamesInfo, gameType=gameType, playerName=playerName, playersList=playersList)

@app.route("/score/single/<gameType>")
def scoreSingle(gameType):
    playersList = getPlayersSingle(gameType)
    players = createPObjectsSingle(playersList,"point")
    playersMax = createPObjectsSingle(playersList,"max")
    playersAveP = createPObjectsSingle(playersList,"aveP")
    return render_template('score_single.html', players=players, gameType=gameType, playersMax=playersMax, playersAveP=playersAveP)

@app.route("/create/newSingle", methods = ["GET", "POST"])
def createGameType():
    if request.method == "POST":
        name = request.form.get("name")
        addNewGameType(name)
        return redirect("/")
    else:
        return render_template('create_gameType.html')

@app.route("/create/single/<gameType>", methods = ["GET", "POST"])
def creatSingle(gameType):
    error = 0
    if request.method == "POST":
        player1 = request.form.get("player1")
        player2 = request.form.get("player2")
        player3 = request.form.get("player3")
        player4 = request.form.get("player4")
        point1 = request.form.get("point1")
        point2 = request.form.get("point2")
        point3 = request.form.get("point3")
        point4 = request.form.get("point4")
        p1 = fixPoint(int(point1),1)
        p2 = fixPoint(int(point2),2)
        p3 = fixPoint(int(point3),3)
        p4 = fixPoint(int(point4),4)
        if p1+p2+p3+p4 == 0:
            addNewGameSingle(gameType,player1,player2,player3,player4,point1,point2,point3,point4,p1,p2,p3,p4)
            return redirect(f"/score/single/{gameType}")
        else:
            error = 1
            return render_template('create_single.html', gameType=gameType, error=error)
    else:
        return render_template('create_single.html', gameType=gameType, error=error)

