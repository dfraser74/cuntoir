import os
#import OpenSSL

def createConfigs():
    #create dbHosts.conf
    with open("dbHosts.conf", "w") as hostsFile:
        dbHosts = []
        host = raw_input("Enter the primary database hostname (e.g. localhost), or nothing to only use localhost: ")
        while(host):
            dbHosts.append(host)
            host = raw_input("Enter another fallback host, or nothing to continue: ")
        if(not dbHosts):
            dbHosts.append("localhost")
        for host in dbHosts:
            hostsFile.write(host+"\n")
    #create invite.conf
    with open("invite.conf", "w") as inviteFile:
        print("Please note, right now invite codes aren't fully supported,")
        print("so if you use them you'll need to use the custom requests code given in the readme file to set up users, sorry.")
        invite = raw_input("Enter the invite code you wish to use, or nothing to leave signup open (recommended): ")
        if(invite):
            inviteFile.write(invite+"\n")
    #create pass.conf
    with open("pass.conf", "w") as passFile:
        dbPass = raw_input("Enter the password you gave to the MySQL user 'fin': ")
        while(not dbPass):
            print("You need to specify a databae password")
            dbPass = raw_input("Enter the password you gave to the MySQL user 'fin': ")
        passFile.write(dbPass+"\n")
    print("Config Files Created")
    #config file creation complete

def createSSLKeys():
    #either copy or create ssl certs
    if(not os.path.exists("ssl")):
        os.makedirs("ssl")
    with open("ssl/cert.pem", "w") as certFile:
        certFileLoc = raw_input("Enter the location of your ssl 'fullchain.pem' file, or nothing to generate one (future feature, on the todo list): ")
        if(certFileLoc):
            with open(certFileLoc, "r") as oldCertFile:
                certFile.write(oldCertFile.read())
                with open("ssl/chain.pem", "w") as chainFile:
                    chainFile.write(oldCertFile.read())
        else:
            raise Exception("You need to specify an already generated ssl full chain file, sorry. It's on the todo list")
            #TODO code to generate an ssl cert file and ssl chain file
    with open("ssl/priv.key", "w") as keyFile:
        keyFileLoc = raw_input("Enter the location of your ssl 'privkey.pem' file, or nothing to generate one: ")
        if(keyFileLoc):
             with open(keyFileLoc, "r") as oldKeyFile:
                keyFile.write(oldKeyFile.read())
        else:
            raise Exception("You need to specify an already generated ssl private key file, sorry. It's on the todo list")
            #TODO generate a key file - this will probably be done when the cert file  location is blank

def createPushKeys():
    #NOTE this is extremely weird, I'll need to figure out a better way to do it, becuase right now the push public key is hard coded into
    #the script.js file. Hmmmmmmmmmm :/
    print("Time to generate some web push notification keys, wooooooo")
    raw_input("Please visit https://web-push-codelab.appspot.com/ and generate a public and private key pair before continuing")
    pubKey = raw_input("Enter the public key: ").strip()
    privKey = raw_input("Enter the private key: ").strip()
    if(not os.path.exists("pushKeys")):
        os.makedirs("pushKeys")
    with open("private_key.pem", "w") as privFile:
        privFile.write(privKey)
    with open("public_key.pem", "w") as pubFile:
        pubFile.write(pubKey)
    #Re-write the public key stored in scripts.js to the new one..... this is gonna be nasty
    with open("static/scripts.js", "r") as scriptsFile:
        scriptsText = scriptsFile.read()
    #pattern match my old public key with the newly generated one, and replace it
    scriptsText.replace("BIceeej1Sv37OVW0Ey4miAkZ4ZYxEQOwp4iNJa6s-MjdvjMJjV6Z9XVZ2i0eRscywzDhDSWgf-3i974Y4qAnpKs", pubKey)
    with open("static/scripts.js", "w") as scriptsFile:
        scriptsFile.write(scriptsText)
    #Told you it would be nasty - TODO - Sort this shit out god damn

if __name__ == "__main__":
    print("We're gonna make some config files, then some ssl certs, then some web push certs.")
    print("Database stuff will come later, for now you need to set that up yourself, sorry.")
    createConfigs()
    createSSLKeys()
    createPushKeys()
    print("Everything should be set up now, config file wise.")
    print("You still need to set up the database, and run 'sudo python server.py' and 'sudo python redirectServer.py', and then it should work, hopefully.")

