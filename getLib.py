import MySQLdb as mysql
import time
import hashlib
import authLib
from types import *

def getAll(dataDict):
    username = dataDict["username"].strip()
    authCode = dataDict["authCode"].strip()
    sort = dataDict["sort"]
    doneFlag = dataDict["archived"]
    timeOffset = dataDict["timeOffset"]
    if(doneFlag == "true" and authLib.checkIfPremium(username) == 0):
        return(3)
    if(doneFlag == "false"):
        buttonText = "<i class='fa fa-check-square-o' aria-hidden='true'></i>"
        buttonVal = "class='archiveButton'"
        onClick = "completeTaskPost"
    if(doneFlag == "true"):
        buttonText = "<i class='fa fa-reply' aria-hidden='true'></i>"
        buttonVal = "class='restoreButton'"
        onClick = "restoreTaskPost"
    auth = authLib.checkAuthCode(dataDict)
    if(auth != 1):
        return(0)
    returnString = ""
    db = authLib.dbCon()
    c = db.cursor()
    command = "SELECT * FROM tasks WHERE BINARY username = %s AND BINARY done = %s"
    c.execute(command, [username, doneFlag])
    tasks = c.fetchall()
    tasks = list(tasks)
    if(len(tasks) == 0):
        return(2)
    if(sort == "default"):
        tasks.sort(key = lambda x:x[3])
    if(sort == "createTime"):
        tasks.sort(key = lambda x:x[2], reverse=True)
    if(doneFlag == "true"):
        returnString += "<div class='task' style='height:auto;' id='infoHeader'><h2 style='margin:auto;'>Archived Tasks:</h2></div>"
    for task in tasks:
        print(task)
        taskId = str(task[0])
        username = task[1]
        createTime = float(task[2])
        dueTime = float(task[3])
        text = task[4]
        title = task[6]
        tags = task[7]
        pushable = task[8]
        recurring = task[10]
        if(recurring == "false"):
            recurringString = ""
        else:
            recurringString = " <i class='fa fa-repeat' aria-hidden='true'></i>("+recurring.title()+")"
        if("'" in title):
            title = title.replace("'", "&apos;")
        if("'" in text):
            text = text.replace("'", "&apos;")
        timeString = time.strftime("%d/%m/%Y %H:%M", time.gmtime(dueTime - float(timeOffset)))
        dateSearchList = time.strftime("%d/%m/%Y", time.gmtime(dueTime - float(timeOffset))).split("/")
        dateSearchList[1] = str(int(dateSearchList[1]) - 1)
        returnString += "<div class='task' id='"+taskId+"'><h2 class='taskTitle' onclick='openEdit("+taskId+");'>" + title + "</h2>"
        if(text != ""):
            returnString += "<div class='taskBody'>" + text + "</div>"
        else:
            returnString += "<div class='taskBody'><span class='italic'>No details</span></div>"
        returnString += "<div class='tagAndDueTimeWrapper'><div class='dueTime' onclick='dateSearch("+dateSearchList[0]+","+dateSearchList[1]+","+dateSearchList[2]+");'>" + timeString + recurringString
        returnString += "</div>"
        returnString += "<div class='taskTags'>"
        if(len(tags) < 1):
            returnString += "<span class='noTaskTag'><span class='italic'>No tags</span></span>" 
        for tag in tags.split(","):
            if(tag == ""):
                continue
            returnString += "<span class='taskTag' onclick='getTagged(\""+tag+"\");'>"+tag+"</span>"
        returnString += "</div></div>"
        returnString += "<button type='button' " + buttonVal + " onclick='" + onClick +"(" + taskId + ");'>" + buttonText + "</button>"
        if(doneFlag == "true"):
            returnString += "<button type='button' class='deleteButton' onclick='deleteTask(" + taskId + ");'><i class='fa fa-times' aria-hidden='true'></i></button>"
        else:
            if(pushable == "true"):
                returnString += "<button type='button' class='notificationToggle' onclick='updatePushable("+taskId+",\"true\");'><i class='fa fa-bell' aria-hidden='true'></i></button>"
            else:
                returnString += "<button type='button' class='notificationToggle' onclick='updatePushable(" + taskId + ",\"false\");'><i class='fa fa-bell-o' aria-hidden='true'></i></button>"
        returnString += "</div>"
    if(doneFlag == "true"):
        returnString += "<div class='task' id='infoFooter' style='height:auto;'><input type='button' id='archiveButton' onclick='getAll();' value='Go Back'></div>"
    return(returnString)

def getTagged(dataDict):
    username = dataDict["username"].strip()
    authCode = dataDict["authCode"].strip()
    searchTag = dataDict["tag"].strip()
    sort = dataDict["sort"]
    auth = authLib.checkAuthCode(dataDict)
    timeOffset = float(dataDict["timeOffset"])
    if(auth != 1):
        return(0)
    returnString = ""
    db = authLib.dbCon()
    c = db.cursor()
    command = "SELECT * FROM tasks WHERE BINARY username = %s AND BINARY done != %s"
    c.execute(command, [username, "true"])
    tasks = c.fetchall()
    tasks = list(tasks)
    for task in tasks:
        for item in task:
            if(type(item) == StringType):
                item = item.decode("utf-8")
    if(len(tasks) == 0):
        return(2)
    if(sort == "default"):
        tasks.sort(key = lambda x:x[3])
    infoString = "<div class='task' id='infoHeader' style='height:auto;width:auto;'><h2 class='taskTitle'>Tasks tagged with \"" + searchTag + "\" :</h2></div>"
    returnString += infoString
    for task in tasks:
        taskId = str(task[0])
        username = task[1]
        createTime = float(task[2])
        dueTime = float(task[3])
        text = task[4]
        title = task[6]
        tags = task[7]
        pushable = task[8]
        recurring = task[10]
        if(recurring == "false"):
            recurringString = ""
        else:
            recurringString = " <i class='fa fa-repeat' aria-hidden='true'></i>("+recurring.title()+")"
        if("'" in title):
            title = title.replace("'", "&apos;")
        if("'" in text):
            text = text.replace("'", "&apos;")
        if(searchTag not in tags.split(",")):
            continue
        if(task[5] == "true"):
            continue
        timeString = time.strftime("%d/%m/%Y %H:%M", time.gmtime(dueTime - timeOffset))
        dateSearchList = time.strftime("%d/%m/%Y", time.gmtime(dueTime - float(timeOffset))).split("/")
        dateSearchList[1] = str(int(dateSearchList[1]) - 1)
        returnString += "<div class='task' id='" + taskId + "'><h2 class='taskTitle' onclick='openEdit(" + taskId + ");'>" + title + "</h2>"
        if(text != ""):
            returnString += "<div class='taskBody'>" + text + "</div>"
        else:
            returnString += "<div class='taskBody'><span class='italic'>No details</span></div>"
        returnString += "<div class='tagAndDueTimeWrapper'><div class='dueTime' onclick='dateSearch("+dateSearchList[0]+","+dateSearchList[1]+","+dateSearchList[2]+");'>" + timeString + recurringString
        returnString += "</div>"
        returnString += "<div class='taskTags'>"
        if(len(tags) < 1):
            returnString += "<span class='noTaskTag'><span class='italic'>No tags</span></span>" 
        for tag in tags.split(","):
            if(tag == ""):
                continue
            returnString += "<span class='taskTag' onclick='getTagged(\""+tag+"\");'>"+tag+"</span>"
        returnString += "</div></div>"
        if(pushable == "true"):
            returnString += "<button type='button' class='notificationToggle' onclick='updatePushable("+taskId+",\"true\");'><i class='fa fa-bell' aria-hidden='true'></i></button>"
        else:
            returnString += "<button type='button' class='notificationToggle' onclick='updatePushable(" + taskId + ",\"false\");'><i class='fa fa-bell-o' aria-hidden='true'></i></button>"
        returnString += "<button type='button' class='archiveButton' onclick='completeTaskPost(" + taskId + ");'><i class='fa fa-check-square-o' aria-hidden='true'></i></button>"
        returnString += "</div>"
    if(returnString == infoString):
        return(2)
    returnString += "<div class='task' id='infoFooter' style='height:auto;'><input type='button' id='archiveButton' onclick='getAll();' value='Go Back'></div>"
    return(returnString)

def search(dataDict):
    username = dataDict["username"].strip()
    authCode = dataDict["authCode"].strip()
    searchString = dataDict["searchString"].strip().lower()
    sort = dataDict["sort"]
    timeOffset = float(dataDict["timeOffset"])
    searchTags = dataDict["searchTags"]
    searchTitle = dataDict["searchTitle"]
    searchBody = dataDict["searchBody"]
    auth = authLib.checkAuthCode(dataDict)
    if(auth != 1):
        return(0)
    returnString = ""
    infoString = "<div class='task' id='infoHeader' style='height:auto;width:auto;'><h2 class='taskTitle'>Tasks matching \"" + searchString + "\" :</h2></div>"
    returnString += infoString
    db = authLib.dbCon()
    c = db.cursor()
    command = "SELECT * FROM tasks WHERE BINARY username = %s AND BINARY done != %s"
    c.execute(command, [username, "true"])
    tasks = c.fetchall()
    tasks = list(tasks)
    for task in tasks:
        for item in task:
            if(type(item) == StringType):
                item = item.decode("utf-8")
    if(len(tasks) == 0):
        return(2)
    if(sort == "default"):
        tasks.sort(key = lambda x:x[3])
    for task in tasks:
        taskId = str(task[0])
        username = task[1]
        createTime = float(task[2])
        dueTime = float(task[3])
        text = task[4]
        title = task[6]
        tags = task[7]
        tagsToCompare = tags
        titleToCompare = title
        textToCompare = text
        pushable = task[8]
        recurring = task[10]
        if(recurring == "false"):
            recurringString = ""
        else:
            recurringString = " <i class='fa fa-repeat' aria-hidden='true'></i>("+recurring.title()+")"
        if("'" in title):
            title = title.replace("'", "&apos;")
        if("'" in text):
            text = text.replace("'", "&apos;")
        #Re-write compared things to null if they shouldn't be searched
        if(searchTitle == "false"):
            titleToCompare = ""
        if(searchBody == "false"):
            textToCompare = ""
        if(searchTags == "false"):
            tagsToCompare = ""
        if(searchString not in tagsToCompare.lower().split(",") and searchString not in titleToCompare.lower() and searchString not in textToCompare.lower()):
            continue
        timeString = time.strftime("%d/%m/%Y %H:%M", time.gmtime(dueTime - timeOffset))
        dateSearchList = time.strftime("%d/%m/%Y", time.gmtime(dueTime - float(timeOffset))).split("/")
        dateSearchList[1] = str(int(dateSearchList[1]) - 1)
        returnString += "<div class='task' id='" + taskId + "'><h2 class='taskTitle' onclick='openEdit(" + taskId + ");'>" + title + "</h2>"
        if(text != ""):
            returnString += "<div class='taskBody'>" + text + "</div>"
        else:
            returnString += "<div class='taskBody'><span class='italic'>No details</span></div>"
        returnString += "<div class='tagAndDueTimeWrapper'><div class='dueTime' onclick='dateSearch("+dateSearchList[0]+","+dateSearchList[1]+","+dateSearchList[2]+");'>" + timeString + recurringString
        returnString += "</div>"
        returnString += "<div class='taskTags'>"
        if(len(tags) < 1):
            returnString += "<span class='noTaskTag'><span class='italic'>No tags<span></span>" 
        for tag in tags.split(","):
            if(tag == ""):
                continue
            returnString += "<span class='taskTag' onclick='getTagged(\""+tag+"\");'>"+tag+"</span>"
        returnString += "</div></div>"
        if(pushable == "true"):
            returnString += "<button type='button' class='notificationToggle' onclick='updatePushable("+taskId+",\"true\");'><i class='fa fa-bell' aria-hidden='true'></i></button>"
        else:
            returnString += "<button type='button' class='notificationToggle' onclick='updatePushable(" + taskId + ",\"false\");'><i class='fa fa-bell-o' aria-hidden='true'></i></button>"
        returnString += "<button type='button' class='archiveButton' onclick='completeTaskPost(" + taskId + ");'><i class='fa fa-check-square-o' aria-hidden='true'></i></button>"
        returnString += "</div>"
    if(returnString == infoString):
        return(2)
    returnString += "<div class='task' id='infoFooter' style='height:auto;'><input type='button' id='archiveButton' onclick='getAll();' value='Go Back'></div>"
    return(returnString)

def dateSearch(dataDict):
    username = dataDict["username"].strip()
    authCode = dataDict["authCode"].strip()
    sort = dataDict["sort"]
    lowerTime = float(dataDict["lowerTime"])
    upperTime = float(dataDict["upperTime"])
    timeOffset = float(dataDict["timeOffset"])
    auth = authLib.checkAuthCode(dataDict)
    if(auth != 1):
        return(0)
    infoString = "<div class='task' id='infoHeader' style='height:auto;width:auto;'><h2 class='taskTitle'>Tasks on " + time.strftime("%d/%m/%Y", time.gmtime(lowerTime - timeOffset)) + ":</h2></div>"
    returnString = ""
    returnString += infoString
    db = authLib.dbCon()
    c = db.cursor()
    command = "SELECT * FROM tasks WHERE BINARY username = %s AND BINARY done != %s"
    c.execute(command, [username, "true"])
    tasks = c.fetchall()
    tasks = list(tasks)
    for task in tasks:
        for item in task:
            if(type(item) == StringType):
                item = item.decode("utf-8")
    if(sort == "default"):
        tasks.sort(key = lambda x:x[3])
    for task in tasks:
        taskId = str(task[0])
        username = task[1]
        createTime = float(task[2])
        dueTime = float(task[3])
        text = task[4]
        title = task[6]
        tags = task[7]
        pushable = task[8]
        recurring = task[10]
        if(recurring == "false"):
            recurringString = ""
        else:
            recurringString = " <i class='fa fa-repeat' aria-hidden='true'></i>("+recurring.title()+")"
        if("'" in title):
            title = title.replace("'", "&apos;")
        if("'" in text):
            text = text.replace("'", "&apos;")
        if(lowerTime > dueTime or upperTime < dueTime):
            continue
        dueTime = dueTime
        timeString = time.strftime("%d/%m/%Y %H:%M", time.gmtime(dueTime - timeOffset))
        dateSearchList = time.strftime("%d/%m/%Y", time.gmtime(dueTime - float(timeOffset))).split("/")
        dateSearchList[1] = str(int(dateSearchList[1]) - 1)
        returnString += "<div class='task' id='" + taskId + "'><h2 class='taskTitle' onclick='openEdit(" + taskId + ");'>" + title + "</h2>"
        if(text != ""):
            returnString += "<div class='taskBody'>" + text + "</div>"
        else:
            returnString += "<div class='taskBody'><span class='italic'>No details</span></div>"
        returnString += "<div class='tagAndDueTimeWrapper'><div class='dueTime' onclick='dateSearch("+dateSearchList[0]+","+dateSearchList[1]+","+dateSearchList[2]+");'>" + timeString + recurringString
        returnString += "</div>"
        returnString += "<div class='taskTags'>"
        if(len(tags) < 1):
            returnString += "<span class='noTaskTag'><span class='italic'>No tags<span></span>" 
        for tag in tags.split(","):
            if(tag == ""):
                continue
            returnString += "<span class='taskTag' onclick='getTagged(\""+tag+"\");'>"+tag+"</span>"
        returnString += "</div></div>"
        if(pushable == "true"):
            returnString += "<button type='button' class='notificationToggle' onclick='updatePushable("+taskId+",\"true\");'><i class='fa fa-bell' aria-hidden='true'></i></button>"
        else:
            returnString += "<button type='button' class='notificationToggle' onclick='updatePushable(" + taskId + ",\"false\");'><i class='fa fa-bell-o' aria-hidden='true'></i></button>"
        returnString += "<button type='button' class='archiveButton' onclick='completeTaskPost(" + taskId + ");'><i class='fa fa-check-square-o' aria-hidden='true'></i></button>"
        returnString += "</div>"
    if(returnString == infoString):
        returnString += "<div class='task' id='infoFooter' style='height:auto;'><h2 class='taskTitle'>No tasks</h2><input type='button' id='archiveButton' onclick='getAll();' value='Go Back'></div>"
        db.close()
        return(returnString)
    returnString += "<div class='task' id='infoFooter' style='height:auto;'><input type='button' id='archiveButton' onclick='getAll();' value='Go Back'></div>"
    db.close()
    return(returnString)

def getTaskDates(dataDict):
    username = dataDict["username"].strip()
    authCode = dataDict["authCode"].strip()
    sort = dataDict["sort"]
    month = int(dataDict["month"])
    year = int(dataDict["year"])
    auth = authLib.checkAuthCode(dataDict)
    if(auth != 1):
        return(0)
    db = authLib.dbCon()
    c = db.cursor()
    command = "SELECT dueTime FROM tasks WHERE BINARY username = %s AND BINARY done != %s"
    c.execute(command, [username, "true"])
    tasks = c.fetchall()
    tasks = list(tasks)
    returnString = str(month) + ";"
    for task in tasks:
        dueTime = task[0]
        dueTimeString = time.strftime("%d/%m/%Y", time.gmtime(dueTime))
        returnString += (dueTimeString + ",")
    db.close()
    returnString += ";"+str(year)
    return(returnString)
