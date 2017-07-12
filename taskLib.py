import calendar
import time
import authLib
import pushLib
import MySQLdb as mysql

def addTask(dataDict):
    username = dataDict["username"].strip()
    authCode = dataDict["authCode"].strip()
    if(authLib.checkAuthCode({"username":username, "authCode":authCode}) != 1):
        return(0)
    if(dataDict["recurring"] not in ["false", "daily", "weekly", "monthly", "quarterly", "yearly"]):
        return(2)
    if(dataDict["recurring"] != "false" and authLib.checkIfPremium(username) != 1):
        return(3)
    createTime = str(time.time())
    dataDict["createTime"] = createTime
    dueTime = dataDict["dueTime"]
    description = dataDict["description"].strip()
    done = "false"
    title = dataDict["title"].strip()
    tags = dataDict["tags"]
    hoursBefore = int(dataDict["hoursBefore"])
    recurring = dataDict["recurring"]
    if(pushLib.checkPushSubscribed(username) == 1):
        pushable = dataDict["pushable"]
    else:
        pushable = "false"
    tagString = ""
    for tag in tags.split(","):
        if(tag == ""):
            continue
        tagString += tag.strip() + ","
    tagString = tagString[:-1]
    db = authLib.dbCon()
    c = db.cursor()
    command = "INSERT INTO tasks (username, createTime, dueTime, text, done, title, tags, pushScheduled, notificationHours, recurring) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    c.execute(command, [username, createTime, dueTime, description, done, title, tagString, pushable, hoursBefore, recurring])
    db.commit()
    db.close()
    db = authLib.dbCon()
    c = db.cursor()
    command = "SELECT id FROM tasks WHERE BINARY username = %s AND createTime = %s"
    c.execute(command, [username, createTime])
    dataDict["id"] = c.fetchall()[0][0]
    if(pushable == "true" and pushLib.checkPushSubscribed(username) == 1):
        pushLib.schedulePush(dataDict)
    return(1)

def completeTask(dataDict):
    username = dataDict["username"].strip()
    authCode = dataDict["authCode"].strip()
    taskId = dataDict["id"]
    doneFlag = dataDict["done"]
    if(authLib.checkAuthCode({"username":username, "authCode":authCode}) != 1):
        return(0)
    if(authLib.checkIfPremium(username) != 1):
        return(deleteTask(dataDict))
    db = authLib.dbCon()
    c = db.cursor()
    recurring = getRecurring(taskId)
    if(recurring == 0):
        command = "UPDATE tasks SET done = %s, pushScheduled = 'false' WHERE BINARY username = %s AND id = %s"
        c.execute(command, [doneFlag, username, taskId])
    else:
        recurringTime = recurring
        command = "UPDATE tasks SET dueTime = dueTime + %s, pushScheduled = 'false' WHERE BINARY username = %s AND id = %s"
        c.execute(command, [recurringTime, username, taskId])
    db.commit()
    db.close()
    if(doneFlag == "true"):
        pushLib.completePush(username, taskId)
    return(1)

def editTask(dataDict):
    username = dataDict["username"]
    authCode = dataDict["authCode"]
    title = dataDict["title"].strip()
    dueTime = str(dataDict["dueTime"])
    taskId = str(dataDict["id"])
    text = dataDict["description"].strip()
    tags = dataDict["tags"]
    hoursBefore = int(dataDict["hoursBefore"])
    recurring = dataDict["recurring"]
    if(pushLib.checkPushSubscribed(username)):
        pushable = dataDict["pushable"]
    else:
        pushable = "false"
    tagString = ""
    for tag in tags.split(","):
        if(tag == ""):
            continue
        tagString += tag.strip() + ","
    tagString = tagString[:-1]
    if(authLib.checkAuthCode({"username":username, "authCode":authCode}) != 1):
        return(0)
    if(dataDict["recurring"] not in ["false", "daily", "weekly", "monthly", "quarterly", "yearly"]):
        return(2)
    if(dataDict["recurring"] != "false" and authLib.checkIfPremium(username) != 1):
        return(3)
    db = authLib.dbCon()
    c = db.cursor()
    command = "UPDATE tasks SET title = %s, text = %s, dueTime = %s, tags = %s, done = %s, pushScheduled = %s, notificationHours = %s, recurring = %s WHERE BINARY username = %s AND id = %s"
    c.execute(command, [title, text, dueTime, tagString, "false", pushable, hoursBefore, recurring, username, taskId])
    db.commit()
    db.close()
    if(pushable == "true" and pushLib.checkPushSubscribed(username)):
        pushLib.schedulePush(dataDict)
    else:
        pushLib.completePush(username, taskId)
    return(1)

def deleteTask(dataDict):
    username = dataDict["username"].strip()
    authCode = dataDict["authCode"].strip()
    taskId = dataDict["id"]
    if(authLib.checkAuthCode(dataDict) != 1):
        return(0)
    db = authLib.dbCon()
    c = db.cursor()
    command = "DELETE FROM tasks WHERE BINARY username = %s AND id = %s"
    c.execute(command, [username, taskId])
    db.commit()
    db.close()
    pushLib.completePush(username, taskId)
    return(1)

def notifyUser(username, title, text):
    db = authLib.dbCon()
    c = db.cursor()
    command = "INSERT INTO tasks (username, createTime, dueTime, text, done, title, tags, pushScheduled, notificationHours, recurring) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    c.execute(command, [username, time.time(), 0, text, "false", title, "", "false", 2, "false"])
    db.commit()
    db.close()
    return(1)

def updatePushable(dataDict):
    username = dataDict["username"]
    taskId = dataDict["id"]
    pushable = "true"
    if(dataDict["pushable"] == "true"):
        pushable = "false"
    if(authLib.checkAuthCode(dataDict) != 1):
        return 0
    if(pushLib.checkPushSubscribed(username) != 1):
        return 2
    db = authLib.dbCon()
    c = db.cursor()
    command = "UPDATE tasks SET pushScheduled = %s WHERE BINARY username = %s AND id = %s"
    c.execute(command, [pushable, username, taskId])
    db.commit()
    db.close()
    if(pushable == "true"):
        db = authLib.dbCon()
        c = db.cursor()
        command = "SELECT title, dueTime FROM tasks WHERE BINARY username = %s AND id = %s"
        c.execute(command, [username, taskId])
        taskInfo = c.fetchall()[0]
        pushLib.schedulePush({"username":username, "id":taskId, "title":taskInfo[0], "dueTime":taskInfo[1]})
        return 1
    else:
        pushLib.completePush(username, taskId)
        return 1

def getRecurring(taskId):
    db = authLib.dbCon()
    c = db.cursor()
    command = "SELECT recurring, dueTime FROM tasks WHERE id = %s"
    c.execute(command, [taskId, ])
    recurringString, dueTime = c.fetchall()[0]
    dueStruct = list(time.gmtime(dueTime))
    if(recurringString == "false"):
        return(0)
    #daily
    if(recurringString == "daily"):
        dueStruct[2] += 1
    #weekly
    if(recurringString == "weekly"):
        dueStruct[2] += 7
    #monthly
    if(recurringString == "monthly"):
        dueStruct[1] += 1
    #quarterly
    if(recurringString == "quarterly"):
        dueStruct[1] += 3
    #yearly
    if(recurringString == "yearly"):
        dueStruct[0] += 1
    #check days
    if(dueStruct[2] > 31):
        dueStruct[2] -= 31
        dueStruct[1] += 1
    #check months
    if(dueStruct[1] > 12):
        dueStruct[1] -= 12
        dueStruct[0] += 1
    dueTime = calendar.timegm(tuple(dueStruct)) - dueTime
    return(dueTime)
