import MySQLdb as mysql
import time
import hashlib
import authLib

def getAll(dataDict):
    username = dataDict["username"].strip()
    authCode = dataDict["authCode"].strip()
    sort = dataDict["sort"]
    auth = authLib.checkAuthCode(dataDict)
    if(auth != 1):
        print("User Auth Failed and was redirected to login")
        return(0)
    print("User auth succeeded, sending tasks")
    returnString = ""
    db = mysql.connect(host="localhost", db="fin", user="fin", passwd=open("pass.conf","r").read().strip())
    c = db.cursor()
    command = "SELECT * FROM tasks WHERE BINARY username = %s AND BINARY done != %s"
    c.execute(command, [username, "true"])
    tasks = c.fetchall()
    tasks = list(tasks)
    if(len(tasks) == 0):
        return(2)
    print(tasks)
    if(sort == "default"):
        tasks.sort(key = lambda x:x[3])
    for task in tasks:
        username = task[1]
        createTime = float(task[2])
        dueTime = float(task[3])
        text = task[4]
        title = task[6]
        if(task[5] == "true"):
            continue
        returnString += "<div id='task'><h2 id='taskTitle'>" + title + "</h2>"
        returnString += "<span id='taskBody'>" + text + "</span><br>"
        returnString += "<span id='dueTime'>Due: " + time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(dueTime))  + "</span>"
        returnString += "<input type='button' value='Done' onclick='completeTaskPost(\"" + title + "\",\"" + str(createTime) + "\");'>"
        returnString += "</div><br>"
    return(returnString)

def login(dataDict):
    returnString = ""
    with open("static/login.html", "r") as loginFile:
        returnString += loginFile.read()
    return(returnString)

def addTask(dataDict):
    returnString = ""
    with open("static/addTask.html", "r") as addTaskFile:
        returnString += addTaskFile.read()
    return(returnString)
