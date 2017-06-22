import random
import string
import cherrypy
import main
import os
import time

cherrypy.config.update({"server.socket_port" : 80, "server.socket_host" : "0.0.0.0"})
@cherrypy.expose()
class finServer(object):
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, **params):
        if(len(params) == 0):
            return(file("static/index.html"))
        else:
            print(params)
            returnString = main.handleGetRequest(params)
            return(str(returnString))
    def POST(self, **params):
        startTime = time.time()
        print(params)
        returnCode = main.handlePostRequest(params)
        totalTime = time.time() - startTime
        print("User served in " + str(totalTime) + " seconds")
        return(str(returnCode))



if __name__ == '__main__' :
    main.startPushWatcher()
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/html')],
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
            'tools.staticdir.on': True,
            'tools.staticdir.dir': "static/",
            'tools.expires.on'    : True,
            'tools.expires.secs'  : 60
#            'tools.proxy.on': True,
#            'tools.proxy.base': 'http://pihome.zapto.org/dev/'
        }
    }
    cherrypy.quickstart(finServer(), "/", conf)
