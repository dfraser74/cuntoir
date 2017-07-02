import sys
import stripe
import authLib
import taskLib
import pushLib
import time

def getKey():
    with open("stripeKeys/stripe.key", "r") as keyFile:
        return(keyFile.read().strip())

def createCustomer(dataDict):
    username = dataDict["username"]
    if(authLib.checkAuthCode(dataDict) == 0):
        return(0)
    if(authLib.checkIfPremium(username) == 1):
        return(2)
    stripe.api_key = getKey()
    token = dataDict["token"]
    email = dataDict["email"]
    try:
        customer = stripe.Customer.create(
        description = "New Customer",
        email = email,
        source = token)
        customerId = customer["id"]
        subscription = subscribeCustomer(customerId, username)
    except stripe.error.CardError as e:
        body = e.json_body
        err = body["error"]
        print(err)
        print("HTTP status is: " + str(e.http_status))
        print("Type is: " + str(err["type"]))
        print("Code is: " + str(err["code"]))
        print("Message is: " + str(err["message"]))
        print("Param is: " + str(err["param"]))
        print("Attempting to delete unusable customer")
        try:
            customer.delete()
            print("Customer deleted successfully")
        except:
            print("Customer delete failed, as customer creation failed earlier")
        return(err["message"])
    except:
        return(4)
    db = authLib.dbCon()
    c = db.cursor()
    subId = subscription["id"]
    command = "INSERT INTO stripe (stripeId, email, username, subId) VALUES (%s, %s, %s, %s);"
    c.execute(command, [customerId, email, username, subId])
    db.commit()
    db.close()
    authLib.upgradeToPremium(username)
    taskLib.notifyUser(username, "Thanks for Subscribing!", "Premium features like archive and push notifications are now available, look for them in the menu")
    return(1)

def subscribeCustomer(customerId, username):
    stripe.api_key = getKey()
    subscription = stripe.Subscription.create(
        customer = customerId,
        plan = "premiumPlan"
    )
    return(subscription)

def customerSubscriptionWatcher():
    while(1):
        customers = getCustomers()
#        if(len(customers) == 0):
#            print("No customers in database")
        for customer in customers:
            username = customer[1]
            if(customer in authLib.getExemptUsers()):
                continue
            customerInfo = getCustomerInfo(username)
            stripeId = customerInfo[1]
            subId = customerInfo[4]
            try:
                checkSubStatus(username, stripeId, subId)
            except:
                print("Subscription check failed for " + username + ", with subId " + subId)
            time.sleep(30)
        time.sleep(5)

def getCustomers():
    db = authLib.dbCon()
    c = db.cursor()
    command = "SELECT * FROM users WHERE premium = %s"
    c.execute(command, ["true",])
    customers = c.fetchall()
    db.close()
    return(customers)

def getCustomerInfo(username):
    db = authLib.dbCon()
    c = db.cursor()
    command = "SELECT * FROM stripe WHERE BINARY username = %s"
    c.execute(command, [username, ])
    customerInfo = c.fetchall()
    customerInfo = customerInfo[0]
    db.close()
    return(customerInfo)

def checkSubStatus(username, stripeId, subId):
    stripe.api_key = getKey()
    subscription = stripe.Subscription.retrieve(subId)
    status = subscription["status"]
    if(status in ["canceled", "unpaid"]):
        print("Customer " + username + " subscription stale, deleting")
        r = deleteCustomer(username, stripeId, "Subscription Renewal Failed", "Please hit \"Upgrade to Premium\" in the menu to update with new details.")
        if(r == 0):
            print("Failed to delete customer entry for " + username + ", with stripe id " + stripeId)
        if(r == 1):
            print("Deletion of customer records for " + username + " successful")
    else:
        print("Customer " + username + " subscription up to date")

def deleteCustomer(username, stripeId, title, text):
    stripe.api_key = getKey()
    try:
        cu = stripe.Customer.retrieve(stripeId)
        cu.delete()
        db = authLib.dbCon()
        c = db.cursor()
        command = "DELETE FROM stripe WHERE BINARY username = %s"
        c.execute(command, [username, ])
        db.commit()
        db.close()
        authLib.downgradeFromPremium(username)
        pushLib.deleteAllSubs(username)
        taskLib.notifyUser(username, title, text)
        return(1)
    except:
        return(0)

def clientDeleteCustomer(dataDict):
    username = dataDict["username"]
    if(authLib.checkAuthCode(dataDict) == 0):
        return(0)
    if(authLib.checkIfPremium(username) == 0):
        return(2)
    customerInfo = getCustomerInfo(username)
    stripeId = customerInfo[1]
    print(deleteCustomer(username, stripeId, "You're unsubscribed", "Sorry to see you go."))
    return(1)

