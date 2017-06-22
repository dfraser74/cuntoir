import time, json
import MySQLdb as mysql
import authLib
from pywebpush import webpush

def addSub(dataDict):
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


def checkPushSubscribed(username):
    db = authLib.dbCon()
    c = db.cursor()
    command = "SELECT * FROM pushInfo WHERE username = %s"
    c.execute(command, [username,])
    if(len(c.fetchall()) == 0):
        db.close()
        return 0
    else:
        db.close()
        return 1

def sendPush(username, title, text):
    with open("private_key.pem", "r") as privKeyFile:
        privKey = privKeyFile.read().strip()
    db = authLib.dbCon()
    c = db.cursor()
    command = "SELECT subString FROM pushInfo WHERE BINARY username = %s"
    c.execute(command, [username,])
    subs = c.fetchall()
    returnCode = 0
    for sub in subs:
        subInfo = sub[0]
        aud = "https://"+subInfo.split("/")[2]
        claim = {"sub":"mailto:oliverbrowne627@gmail.com", "aud":aud}
        data = text + ";" + text + ";" + "images/icon512-Rounded-Gray.png;" + title
        try:
            print(webpush(json.loads(subInfo), data, vapid_private_key=privKey, vapid_claims=claim))
            updateSub(subInfo, "201")
            returnCode = 1
        except:
            print("I'm sorry dave, I can't let you do that")
            updateSub(subInfo, "400")
    return(returnCode)

def deleteSub(subString):
    db = authLib.dbCon()
    c = db.cursor()
    command = "DELETE FROM pushInfo WHERE BINARY subString = %s"
    c.execute(command, [subString,])
    db.commit()
    db.close()

def updateSub(subString, returnCode):
    db = authLib.dbCon()
    c = db.cursor()
    command = "SELECT lastReturn FROM pushInfo WHERE BINARY subString = %s"
    c.execute(command, [subString,])
    commandReturn = c.fetchall()
    lastReturn = commandReturn[0][0]
    if(lastReturn != "201" and lastReturn == returnCode):
        deleteSub(subString)
        return
    if(returnCode == "429"):
        #add to try-later list..... @FIXME add way of scheduling tasks for later
        return
    command = "UPDATE pushInfo SET lastReturn = %s WHERE BINARY subString = %s"
    c.execute(command, [returnCode,subString])
    db.commit()
    db.close()

def pushWatcher():
    while(1):
        doDuePushes()
        time.sleep(5)

def doDuePushes():
    db = authLib.dbCon()
    c = db.cursor()
    t = time.time() + 30.0
    command = "SELECT * FROM duePushes WHERE pushTime < %s"
    c.execute(command, [t,])
    duePushes = c.fetchall()
    if(len(duePushes) == 0):
        return 0
    for duePush in duePushes:
        title = duePush[1]
        username = duePush[2]
        pushTime = float(duePush[3])
        text = duePush[4]
        createTime = float(duePush[5])
        returnCode = sendPush(username, title, text)
        if(returnCode == 0):
            print("Failed to notifiy user " + username + " of task " + title)
        else:
            completePush(username,createTime)

def schedulePush(dataDict):
    username = dataDict["username"]
    title = dataDict["title"]
    text = "This task is due soon"
    dueTime = float(dataDict["dueTime"])
    createTime = float(dataDict["createTime"])
#TODO set up users picking time of notification
    #hoursBefore = dataDict["hoursBefore"]
    hoursBefore = 2.0
    pushTime = dueTime - hoursBefore*60.0*60.0
    if(checkPushSubscribed(username) == 0):
        return(2)
    completePush(username, createTime)
    db = authLib.dbCon()
    c = db.cursor()
    command = "INSERT INTO duePushes (title, username, pushTime, text, createTime) VALUES (%s, %s, %s, %s, %s)"
    c.execute(command, [title, username, pushTime, text, createTime])
    db.commit()
    db.close()
    return(1)

def completePush(username, createTime):
    db = authLib.dbCon()
    c = db.cursor()
    command = "DELETE FROM duePushes WHERE username = %s AND createTime = %s"
    c.execute(command, [username, float(createTime)])
    db.commit()
    db.close()
    return 0
