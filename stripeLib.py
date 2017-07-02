import sys
import stripe
import authLib
import taskLib

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


