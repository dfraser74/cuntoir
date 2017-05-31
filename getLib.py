import MySQLdb as mysql
import time
import hashlib
import authLib
from types import *

def getAll(dataDict):
    username = dataDict["username"].strip()
    authCode = dataDict["authCode"].strip()
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
        if(task[5] == "true"):
            continue
        timeString = time.strftime("%d/%m/%Y %H:%M", time.localtime(dueTime))
        returnString += "<div class='task' id='"+title+"'><h2 class='taskTitle' onclick='openEdit(\""+title +"\",\""+text+"\",\""+timeString+"\",\""+str(createTime)+"\",\""+tags+"\");'>" + title + "</h2>"
        if(text != ""):
            returnString += "<div class='taskBody'>" + text + "</div><br>"
        returnString += "<div class='dueTime'>" + timeString + "</div>"
        returnString += "<div class='taskTags'>"
        for tag in tags.split(","):
            if(tag == ""):
                continue
            returnString += "<span class='taskTag' onclick='getTagged(\""+tag+"\");'>"+tag+"</span>"
        returnString += "</div>"
        returnString += "<input type='button' value='Done' onclick='completeTaskPost(\"" + title + "\",\"" + str(createTime) + "\");'>"
        returnString += "</div>"
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
        if(searchTag not in tags.split(",")):
            continue
        if(task[5] == "true"):
            continue
        timeString = time.strftime("%d/%m/%Y %H:%M", time.localtime(dueTime))
        returnString += "<div class='task' id='"+title+"'><h2 class='taskTitle' onclick='openEdit(\""+title +"\",\""+text+"\",\""+timeString+"\",\""+str(createTime)+"\",\""+tags+"\");'>" + title + "</h2>"
        if(text != ""):
            returnString += "<div class='taskBody'>" + text + "</div><br>"
        returnString += "<div class='dueTime'>" + timeString + "</div><br>"
        returnString += "<div class='taskTags'>"
        for tag in tags.split(","):
            if(tag == ""):
                continue
            returnString += "<span class='taskTag' onclick='getTagged(\""+tag+"\");'>"+tag+"</span>"
        returnString += "</div>"
        returnString += "<input type='button' value='Done' onclick='completeTaskPost(\"" + title + "\",\"" + str(createTime) + "\");'>"
        returnString += "</div>"
    if(returnString == ""):
        return(2)
    return(returnString)
