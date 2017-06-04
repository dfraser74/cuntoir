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
    if(doneFlag == "false"):
        buttonVal = "Complete"
        onClick = "completeTaskPost"
    if(doneFlag == "true"):
        buttonVal = "Restore' id='archiveButton"
        onClick = "restoreTaskPost"
    auth = authLib.checkAuthCode(dataDict)
    if(auth != 1):
        return(0)
    returnString = ""
    db = mysql.connect(host="localhost", db="fin", user="fin", passwd=open("pass.conf","r").read().strip())
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
        returnString += "<div class=task style='height:auto;'><h2 style='margin:auto;'>Archived Tasks:</h2></div><br>"
    for task in tasks:
        username = task[1]
        createTime = float(task[2])
        dueTime = float(task[3])
        text = task[4]
        title = task[6]
        tags = task[7]
        if("'" in title):
            title = title.replace("'", "&apos;")
        if("'" in text):
            text = text.replace("'", "&apos;")
        timeString = time.strftime("%d/%m/%Y %H:%M", time.localtime(dueTime))
        returnString += "<div class='task' id='"+title+"'><h2 class='taskTitle' onclick='openEdit(\""+title +"\",\""+text+"\",\""+timeString+"\",\""+str(createTime)+"\",\""+tags+"\");'>" + title + "</h2>"
        if(text != ""):
            returnString += "<div class='taskBody'>" + text + "</div><br>"
        else:
            returnString += "<div class='taskBody'><span class='italic'>No details</span></div><br>"
        returnString += "<div class='dueTime'>" + timeString + "</div>"
        returnString += "<div class='taskTags'>"
        if(len(tags) < 1):
            returnString += "<span class='noTaskTag'><span class='italic'>No tags</span></span>" 
        for tag in tags.split(","):
            if(tag == ""):
                continue
            returnString += "<span class='taskTag' onclick='getTagged(\""+tag+"\");'>"+tag+"</span>"
        returnString += "</div>"
        returnString += "<input type='button' value='" + buttonVal + "' onclick='" + onClick +"(\"" + title + "\",\"" + str(createTime) + "\");'>"
        if(doneFlag == "true"):
            returnString += "<input type='button' id='archiveButton' value='Delete' onclick='deleteTask(\""+title+"\",\""+str(createTime)+"\");'>"
        returnString += "</div>"
    if(doneFlag == "true"):
        returnString += "<br><div class='task' style='height:auto;'><input type='button' onclick='getAll();' value='Go Back'></div>"
    return(returnString)

def login(dataDict):
    returnString = ""
    with open("static/login.html", "r") as loginFile:
        returnString += loginFile.read()
    return(returnString)

def getTagged(dataDict):
    username = dataDict["username"].strip()
    authCode = dataDict["authCode"].strip()
    searchTag = dataDict["tag"].strip()
    sort = dataDict["sort"]
    auth = authLib.checkAuthCode(dataDict)
    if(auth != 1):
        return(0)
    returnString = ""
    db = mysql.connect(host="localhost", db="fin", user="fin", passwd=open("pass.conf","r").read().strip())
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
        username = task[1]
        createTime = float(task[2])
        dueTime = float(task[3])
        text = task[4]
        title = task[6]
        tags = task[7]
        if("'" in title):
            title = title.replace("'", "&apos;")
        if("'" in text):
            text = text.replace("'", "&apos;")
        if(searchTag not in tags.split(",")):
            continue
        if(task[5] == "true"):
            continue
        timeString = time.strftime("%d/%m/%Y %H:%M", time.localtime(dueTime))
        returnString += "<div class='task' id='"+title+"'><h2 class='taskTitle' onclick='openEdit(\""+title +"\",\""+text+"\",\""+timeString+"\",\""+str(createTime)+"\",\""+tags+"\");'>" + title + "</h2>"
        if(text != ""):
            returnString += "<div class='taskBody'>" + text + "</div><br>"
        else:
            returnString += "<div class='taskBody'><span class='italic'>No details</span></div><br>"
        returnString += "<div class='dueTime'>" + timeString + "</div><br>"
        returnString += "<div class='taskTags'>"
        if(len(tags) < 1):
            returnString += "<span class='noTaskTag'><span class='italic'>No tags</span></span>" 
        for tag in tags.split(","):
            if(tag == ""):
                continue
            returnString += "<span class='taskTag' onclick='getTagged(\""+tag+"\");'>"+tag+"</span>"
        returnString += "</div>"
        returnString += "<input type='button' value='Done' onclick='completeTaskPost(\"" + title + "\",\"" + str(createTime) + "\");'>"
        returnString += "</div>"
    if(returnString == ""):
        return(2)
    returnString += "<br><div class='task' style='height:auto;'><input type='button' onclick='getAll();' value='Go Back'></div>"
    return(returnString)

def search(dataDict):
    username = dataDict["username"].strip()
    authCode = dataDict["authCode"].strip()
    searchString = dataDict["searchString"].strip().lower()
    sort = dataDict["sort"]
    auth = authLib.checkAuthCode(dataDict)
    if(auth != 1):
        return(0)
    returnString = ""
    db = mysql.connect(host="localhost", db="fin", user="fin", passwd=open("pass.conf","r").read().strip())
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
        username = task[1]
        createTime = float(task[2])
        dueTime = float(task[3])
        text = task[4]
        title = task[6]
        tags = task[7]
        if("'" in title):
            title = title.replace("'", "&apos;")
        if("'" in text):
            text = text.replace("'", "&apos;")
        if(searchString not in tags.lower().split(",") and searchString not in title.lower() and searchString not in text.lower() and task[5] != "true"):
            continue
        timeString = time.strftime("%d/%m/%Y %H:%M", time.localtime(dueTime))
        returnString += "<div class='task' id='"+title+"'><h2 class='taskTitle' onclick='openEdit(\""+title +"\",\""+text+"\",\""+timeString+"\",\""+str(createTime)+"\",\""+tags+"\");'>" + title + "</h2>"
        if(text != ""):
            returnString += "<div class='taskBody'>" + text + "</div><br>"
        else:
            returnString += "<div class='taskBody'><span class='italic'>No details</span></div><br>"
        returnString += "<div class='dueTime'>" + timeString + "</div><br>"
        returnString += "<div class='taskTags'>"
        if(len(tags) < 1):
            returnString += "<span class='noTaskTag'><span class='italic'>No tags<span></span>" 
        for tag in tags.split(","):
            if(tag == ""):
                continue
            returnString += "<span class='taskTag' onclick='getTagged(\""+tag+"\");'>"+tag+"</span>"
        returnString += "</div>"
        returnString += "<input type='button' value='Done' onclick='completeTaskPost(\"" + title + "\",\"" + str(createTime) + "\");'>"
        returnString += "</div>"
    if(returnString == ""):
        return(2)
    returnString += "<br><div class='task' style='height:auto;'><input type='button' onclick='getAll();' value='Go Back'></div>"
    return(returnString)

def dateSearch(dataDict):
    username = dataDict["username"].strip()
    authCode = dataDict["authCode"].strip()
    sort = dataDict["sort"]
    lowerTime = float(dataDict["lowerTime"])
    upperTime = float(dataDict["upperTime"])
    auth = authLib.checkAuthCode(dataDict)
    if(auth != 1):
        return(0)
    infoString = "<div class='task' style='height:auto;width:auto;'><h2 class='taskTitle'>Tasks on " + time.strftime("%d/%m/%Y", time.localtime(lowerTime)) + ":</h2></div><br>"
    returnString = ""
    returnString += infoString
    db = mysql.connect(host="localhost", db="fin", user="fin", passwd=open("pass.conf","r").read().strip())
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
        db.close()
        return(2)
    if(sort == "default"):
        tasks.sort(key = lambda x:x[3])
    for task in tasks:
        username = task[1]
        createTime = float(task[2])
        dueTime = float(task[3])
        text = task[4]
        title = task[6]
        tags = task[7]
        if("'" in title):
            title = title.replace("'", "&apos;")
        if("'" in text):
            text = text.replace("'", "&apos;")
        if(lowerTime > dueTime or upperTime < dueTime):
            continue
        timeString = time.strftime("%d/%m/%Y %H:%M", time.localtime(dueTime))
        returnString += "<div class='task' id='"+title+"'><h2 class='taskTitle' onclick='openEdit(\""+title +"\",\""+text+"\",\""+timeString+"\",\""+str(createTime)+"\",\""+tags+"\");'>" + title + "</h2>"
        if(text != ""):
            returnString += "<div class='taskBody'>" + text + "</div><br>"
        else:
            returnString += "<div class='taskBody'><span class='italic'>No details</span></div><br>"
        returnString += "<div class='dueTime'>" + timeString + "</div><br>"
        returnString += "<div class='taskTags'>"
        if(len(tags) < 1):
            returnString += "<span class='noTaskTag'><span class='italic'>No tags<span></span>" 
        for tag in tags.split(","):
            if(tag == ""):
                continue
            returnString += "<span class='taskTag' onclick='getTagged(\""+tag+"\");'>"+tag+"</span>"
        returnString += "</div>"
        returnString += "<input type='button' value='Done' onclick='completeTaskPost(\"" + title + "\",\"" + str(createTime) + "\");'>"
        returnString += "</div>"
    if(returnString == infoString):
        returnString += "<div class='task' style='height:auto;'><h2 class='taskTitle'>No tasks</h2><input type='button' onclick='getAll();' value='Go Back'></div>"
        db.close()
        return(returnString)
    returnString += "<br><div class='task' style='height:auto;'><input type='button' onclick='getAll();' value='Go Back'></div>"
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
    db = mysql.connect(host="localhost", db="fin", user="fin", passwd=open("pass.conf","r").read().strip())
    c = db.cursor()
    command = "SELECT dueTime FROM tasks WHERE BINARY username = %s AND BINARY done != %s"
    c.execute(command, [username, "true"])
    tasks = c.fetchall()
    tasks = list(tasks)
    returnString = str(month) + ";"
    for task in tasks:
        dueTime = task[0]
        dueTimeString = time.strftime("%d/%m/%Y", time.localtime(dueTime))
        returnString += (dueTimeString + ",")
    db.close()
    returnString += ";"+str(year)
    print(returnString)
    return(returnString)
