import time
import authLib
import MySQLdb as mysql

def addTask(dataDict):
    username = dataDict["username"].strip()
    authCode = dataDict["authCode"].strip()
    if(authLib.checkAuthCode({"username":username, "authCode":authCode}) != 1):
        return(0)
    createTime = str(time.time())
    dueTime = dataDict["dueTime"]
    description = dataDict["description"]
    done = "false"
    title = dataDict["title"]
    db = mysql.connect(host = "localhost", db = "fin", user = "fin", passwd = open("pass.conf","r").read().strip())
    c = db.cursor()
    command = "INSERT INTO tasks (username, createTime, dueTime, text, done, title) VALUES (%s, %s, %s, %s, %s, %s)"
    c.execute(command, [username, createTime, dueTime, description, done, title])
    db.commit()
    db.close()
    return(1)

def completeTask(dataDict):
    print(dataDict)
    username = dataDict["username"].strip()
    authCode = dataDict["authCode"].strip()
    title = dataDict["title"]
    createTime = dataDict["createTime"]
    if(authLib.checkAuthCode({"username":username, "authCode":authCode}) != 1):
        return(0)
    db = mysql.connect(host = "localhost", db = "fin", user = "fin", passwd = open("pass.conf","r").read().strip())
    c = db.cursor()
    command = "UPDATE tasks SET done = 'true' WHERE BINARY username = %s AND BINARY title = %s AND createTime = %s"
    c.execute(command, [username, title, createTime])
    db.commit()
    db.close()
    return(1)
