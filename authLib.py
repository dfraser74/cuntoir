import hashlib, time, random
import MySQLdb as mysql
import taskLib

def dbCon():
    with open("dbHosts.conf") as dbHostsFile:
        dbHosts = dbHostsFile.readlines()
    for host in dbHosts:
        if(host[0] == "#"):
            continue
        try:
            host = host.strip()
            db = mysql.connect(host=host, db="fin", user="fin", passwd=open("pass.conf","r").read().strip())
            return(db)
        except:
            print("Connection to " + host + " failed")

def hasher(string):
    i = 0;
    while(i < 64000):
        string = str(hashlib.sha512(string).hexdigest())
        i += 1
    return(string)

def checkAuthCode(dataDict):
#    startTime = time.time()
    timeOut = 60*60*24
    username = dataDict["username"].strip()
    authCode = dataDict["authCode"].strip()
    db = dbCon()
    c = db.cursor()
    command = "SELECT username, authCode, createTime FROM authCodes;"
    c.execute(command)
    authCodeTuples = c.fetchall()
    for authCodeTuple in authCodeTuples:
        if(str(authCodeTuple[0]) == str(username) and str(authCodeTuple[1]) == str(authCode) and (abs(time.time() - float(authCodeTuple[2]))) < timeOut):
            db.close()
            return(1)
    db.close()
    return(0)

def authUser(username, userPass):
    username = username.strip()
    userPass = hasher(userPass.strip())
    db = dbCon()
    c = db.cursor()
    command = "SELECT username, pass FROM users;"
    c.execute(command)
    users = c.fetchall()
    for user in users:
        if(username == user[0] and userPass == user[1]):
            db.close()
            return(1)
    db.close()
    return(0)

def createAuthCode(username, userPass):
    timeout = 60*60*12
    username = username.strip()
    userPass = userPass.strip()
    if(authUser(username, userPass) == 0):
        return(0)
    db = dbCon()
    c = db.cursor()
    command = "DELETE FROM authCodes WHERE username = %s AND  createTime < %s"
    c.execute(command, [username, time.time()-timeout])
    c = db.cursor()
    command = "INSERT INTO authCodes (username, authCode, createTime) VALUES (%s, %s, %s);"
    authCode = str(hashlib.sha256(str(time.time) + str(random.uniform(1,100))).hexdigest())
    c.execute(command, [username, authCode, time.time()])
    db.commit()
    db.close()
    return(authCode)

def createUser(dataDict):
    username = dataDict["username"].strip()
    userPass = hasher(dataDict["userPass"].strip())
    inviteCode = dataDict["inviteCode"]
    if(len(userPass) < 8):
        return(3)
    if(len(username) < 4):
        return(4)
    with open("invite.conf", "r") as inviteFile:
        invite = inviteFile.read().strip()
    if(invite != "" and inviteCode != invite):
        return(0)
    db = dbCon()
    c = db.cursor()
    command = "SELECT username FROM users;"
    c.execute(command)
    userList = c.fetchall()
    for user in userList:
        user = user[0]
        if(username == user):
            db.close()
            return(2)
    command = "INSERT INTO users (username, pass, sendPushes, premium) VALUES (%s, %s, %s, %s);"
    c.execute(command, [username, userPass, "false", "true"])
    db.commit()
    db.close()
    taskLib.notifyUser(username, "Hey There! Click this to edit!", "Things with a border are clickable, and so are icons (p.s. try swiping ;) )")
    return(1)

def changePass(dataDict):
    username = dataDict["username"].strip()
    oldPass = dataDict["oldPass"].strip()
    newPass = hasher(dataDict["newPass"].strip())
    if(authUser(username, oldPass) == 0):
        return(0)
    db = dbCon()
    c = db.cursor()
    command = "UPDATE users SET pass = %s WHERE BINARY username = %s"
    c.execute(command, [newPass, username])
    db.commit()
    db.close()
    return(1)

def checkIfPremium(username):
    return(1)
    username = username.strip()
    db = dbCon()
    c = db.cursor()
    command = "SELECT premium FROM users WHERE BINARY username = %s;"
    c.execute(command, [username, ])
    users = c.fetchall()
    if(len(users) < 1):
        return(0)
    premium = users[0][0]
    if(premium == "false"):
        db.close()
        return(0)
    db.close()
    return(1)

def upgradeToPremium(username):
    username = username.strip()
    db = dbCon()
    c = db.cursor()
    command = "UPDATE users SET premium = %s WHERE BINARY username = %s;"
    c.execute(command, ["true", username])
    db.commit()
    db.close()
    return(1)

def downgradeFromPremium(username):
    if(checkIfPremium(username) == 0):
        return(0)#user is already not premium
    username = username.strip()
    db = dbCon()
    c = db.cursor()
    command = "UPDATE users SET premium = %s WHERE BINARY username = %s;"
    c.execute(command, ["false", username])
    db.commit()
    db.close()
    return(1)

def clientCheckIfPremium(dataDict):
    if(checkAuthCode(dataDict) == 0):
        return(2)
    return(checkIfPremium(dataDict["username"]))

def getExemptUsers():
    return(["Oliver", "wired", "arsTech", "androidRun"])
