import time, json
import MySQLdb as mysql
import authLib
from pywebpush import webpush

def updateSub(dataDict):
    username = dataDict["username"].strip()
    authCode = dataDict["authCode"].strip()
    if(authLib.checkAuthCode(dataDict) != 1):
        return(0)
    subInfo = dataDict["subInfo"]
    db = authLib.dbCon()
    c = db.cursor()
    command = "INSERT INTO pushInfo (username, subString, lastReturn) VALUES (%s, %s, %s);"
    c.execute(command, [username, subInfo, "201"])
    command = "UPDATE users SET sendPushes = %s WHERE BINARY username = %s;"
    c.execute(command, ["true", username])
    db.commit()
    db.close()
    return(1)


def sendPush(username, title, text, dueTime):
    print(title)
    with open("private_key.pem", "r") as privKeyFile:
        privKey = privKeyFile.read().strip()
    db = authLib.dbCon()
    c = db.cursor()
    command = "SELECT subString FROM pushInfo WHERE BINARY username = %s"
    c.execute(command, [username,])
    subs = c.fetchall()
    for sub in subs:
        subInfo = sub[0]
        aud = "https://"+subInfo.split("/")[2]
        claim = {"sub":"mailto:oliverbrowne627@gmail.com", "aud":aud}
        data = title + ";" + text + ";" + "images/icon512-Rounded-Gray.png"
        try:
            print(webpush(json.loads(subInfo), data, vapid_private_key=privKey, vapid_claims=claim))
        except:
            print("I'm sorry dave, I can't let you do that")
            deleteSub(subInfo)

def pushDueTasks(userList):
    db = authLib.dbCon()
    for username in userList:
        c = db.cursor()
        command = "SELECT title, text, dueTime FROM tasks WHERE BINARY username = %s AND BINARY done != %s;"
        c.execute(command, [username,"true"])
        tasks = c.fetchall()
        for task in tasks:
            title = task[0]
            text = task[1]
            dueTime = task[2]
            if(float(dueTime) < time.time()+60*60*24):
                sendPush(username, title, text, dueTime)
        c.close()
    db.close()

def deleteSub(subString):
    db = authLib.dbCon()
    c = db.cursor()
    command = "DELETE FROM pushInfo WHERE BINARY subString = %s"
    c.execute(command, [subString,])
    db.commit()
    db.close()
