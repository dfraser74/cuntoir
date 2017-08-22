# cuntoir
Progressive To-do web app with a vanilla Javascript front-end, a Python back-end and a MySQL database

Usage: 
    -Run setup.py
    -Create a MySQL Database from fin.sql, called 'fin'
    -Create a MySQL user called 'fin' with the password you gave in setup.py,
        and all permissions on the 'fin' database
    -Run 'sudo python server.py' in a screen session
    -Run 'sudo python redirectServer.py' in a screen session
    -If you're using an invite code, do the following in a python REPL:
        -import requests as r
        -r.post("https://localhost", data={
                "method":"createUser", 
                "username":"YOUR_USERNAME_HERE", 
                "userPass":"YOUR_PASS_HERE",
                "inviteCode":"YOUR_INVITECODE_HERE"})

Main items on the to-do list:
    -Remove stripe integration, all feature lockoff
    -Improve setup experience
    -Consolidate config files
    -Re-factor database connection setup, create database connection class
    -Improve templating of getLib.py
    -General re-factoring
