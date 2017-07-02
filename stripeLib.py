import stripe
import authLib

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
    customer = stripe.Customer.create(
        description = "New Customer",
        email = email,
        source = token)
    customerId = customer["id"]
    db = authLib.dbCon()
    c = db.cursor()
    subscription = subscribeCustomer(customerId, username)
    subId = subscription["id"]
    command = "INSERT INTO stripe (stripeId, email, username, subId) VALUES (%s, %s, %s, %s);"
    c.execute(command, [customerId, email, username, subId])
    db.commit()
    db.close()
    authLib.upgradeToPremium(username)
    return(1)

def subscribeCustomer(customerId, username):
    stripe.api_key = getKey()
    subscription = stripe.Subscription.create(
        customer = customerId,
        plan = "premiumPlan"
    )
    return(subscription)


