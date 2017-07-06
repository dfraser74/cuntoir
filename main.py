import getLib
import authLib
import taskLib
import pushLib
import thread
import stripeLib

def startThreads():
    thread.start_new_thread(pushLib.pushWatcher, ())
    thread.start_new_thread(stripeLib.customerSubscriptionWatcher, ())
    return(1)

def handlePostRequest(dataDict):
    returnCode = 0
    for key in dataDict:
        dataDict[key] = dataDict[key].encode("utf-8")
    method = dataDict["method"]
    if(method == "login"):
        returnCode = authLib.createAuthCode(dataDict["username"], dataDict["userPass"])
    if(method == "createUser"):
        returnCode = authLib.createUser(dataDict)
    if(method == "authUser"):
        returnCode = authLib.checkAuthCode(dataDict)
    if(method == "addTask"):
        returnCode = taskLib.addTask(dataDict)
    if(method == "completeTask"):
        returnCode = taskLib.completeTask(dataDict)
    if(method == "getAll"):
        returnCode = getLib.getAll(dataDict)
    if(method == "editTask"):
        returnCode = taskLib.editTask(dataDict)
    if(method == "getTagged"):
        returnCode = getLib.getTagged(dataDict)
    if(method == "search"):
        returnCode = getLib.search(dataDict)
    if(method == "dateSearch"):
        returnCode = getLib.dateSearch(dataDict)
    if(method == "getTaskDates"):
        returnCode = getLib.getTaskDates(dataDict)
    if(method == "deleteTask"):
        returnCode = taskLib.deleteTask(dataDict)
    if(method == "changePass"):
        returnCode = authLib.changePass(dataDict)
    if(method == "updateSub"):
        returnCode = pushLib.addSub(dataDict)
    if(method == "createCustomer"):
        returnCode = stripeLib.createCustomer(dataDict)
    if(method == "checkPremium"):
        returnCode = authLib.clientCheckIfPremium(dataDict)
    if(method == "clientDeleteCustomer"):
        returnCode = stripeLib.clientDeleteCustomer(dataDict)
    if(method == "updatePushable"):
        returnCode = taskLib.updatePushable(dataDict)
    return(returnCode)

def handleGetRequest(dataDict):
    returnString = "null"
    method = dataDict["method"]
    for key in dataDict:
        dataDict[key] = dataDict[key].encode("utf-8")
    if(method == "getOne"):
        returnString = getLib.getOne(dataDict)
    return(returnString)
