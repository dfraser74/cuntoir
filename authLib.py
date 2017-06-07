import hashlib, time, random
import MySQLdb as mysql

def dbCon():
    db = mysql.connect(host="localhost", db="fin", user="fin", passwd=open("pass.conf","r").read().strip())
    return(db)

def hasher(string):
    i = 0;
    while(i < 64000):
        string = str(hashlib.sha512(string).hexdigest())
        i += 1
    return(string)

def checkAuthCode(dataDict):
    username = dataDict["username"].strip()
    authCode = dataDict["authCode"].strip()
    db = mysql.connect(host="localhost", db="fin", user="fin", passwd=open("pass.conf","r").read().strip())
    c = db.cursor()
    command = "SELECT username, authCode, createTime FROM authCodes;"
    c.execute(command)
    authCodeTuples = c.fetchall()
    for authCodeTuple in authCodeTuples:
        if(str(authCodeTuple[0]) == str(username) and str(authCodeTuple[1]) == str(authCode) and (abs(time.time() - float(authCodeTuple[2]))) < 60*60*24):
            db.close()
            return(1)
    db.close()
    return(0)

def authUser(username, userPass):
    username = username.strip()
    userPass = hasher(userPass.strip())
    db = mysql.connect(host="localhost", db="fin", user="fin", passwd=open("pass.conf","r").read().strip())
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
    username = username.strip()
    userPass = userPass.strip()
    if(authUser(username, userPass) == 0):
        return(0)
    db = mysql.connect(host="localhost", db="fin", user="fin", passwd=open("pass.conf","r").read().strip())
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
    with open("invite.conf", "r") as inviteFile:
        invite = inviteFile.read().strip()
    if(invite != "" and inviteCode != invite):
        return(0)
    db = mysql.connect(host="localhost", db="fin", user="fin", passwd=open("pass.conf","r").read().strip())
    c = db.cursor()
    command = "SELECT username FROM users;"
    c.execute(command)
    userList = c.fetchall()
    for user in userList:
        user = user[0]
        if(username == user):
            db.close()
            return(2)
    command = "INSERT INTO users (username, pass, sendPushes) VALUES (%s, %s, 'false');"
    c.execute(command, [username, userPass])
    db.commit()
    db.close()
    return(1)

def changePass(dataDict):
    username = dataDict["username"].strip()
    oldPass = dataDict["oldPass"].strip()
    newPass = hasher(dataDict["newPass"].strip())
    if(authUser(username, oldPass) == 0):
        return(0)
    db = mysql.connect(host="localhost", db="fin", user="fin", passwd=open("pass.conf","r").read().strip())
    c = db.cursor()
    print(username + " : " + newPass)
    command = "UPDATE users SET pass = %s WHERE BINARY username = %s"
    c.execute(command, [newPass, username])
    db.commit()
    db.close()
    return(1)

