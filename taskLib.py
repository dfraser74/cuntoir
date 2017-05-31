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
    tags = dataDict["tags"]
    tagString = ""
    for tag in tags.split(","):
        if(tag == ""):
            continue
        tagString += tag.strip() + ","
    tagString = tagString[:-1]
    db = mysql.connect(host = "localhost", db = "fin", user = "fin", passwd = open("pass.conf","r").read().strip())
    c = db.cursor()
    command = "INSERT INTO tasks (username, createTime, dueTime, text, done, title, tags) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    c.execute(command, [username, createTime, dueTime, description, done, title, tagString])
    db.commit()
    db.close()
    return(1)

def completeTask(dataDict):
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

def editTask(dataDict):
    username = dataDict["username"]
    authCode = dataDict["authCode"]
    title = dataDict["title"]
    dueTime = str(dataDict["dueTime"])
    createTime = str(dataDict["createTime"])
    text = dataDict["description"]
    tags = dataDict["tags"]
    tagString = ""
    for tag in tags.split(","):
        if(tag == ""):
            continue
        tagString += tag.strip() + ","
    tagString = tagString[:-1]
    if(authLib.checkAuthCode({"username":username, "authCode":authCode}) != 1):
        return(0)
    db = mysql.connect(host = "localhost", db = "fin", user = "fin", passwd = open("pass.conf","r").read().strip())
    c = db.cursor()
    command = "UPDATE tasks SET title = %s, text = %s, dueTime = %s, tags = %s WHERE BINARY username = %s AND createTime = %s"
    c.execute(command, [title, text, dueTime, tagString, username, createTime])
    db.commit()
    db.close()
    return(1)
    
