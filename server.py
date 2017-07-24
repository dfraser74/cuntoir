import random
import string
import cherrypy
import main
import os
import time
import sys

sslConf = {
    'server.ssl_module':'pyopenssl',
    'server.ssl_certificate':'ssl/cert.pem',
    'server.ssl_private_key':'ssl/priv.key',
    'cherrypy.server.ssl_certificate_chain':'ssl/chain.pem',
    'server.socket_port':443,
    'server.socket_host':'0.0.0.0'
}
cherrypy.config.update(sslConf)

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

@cherrypy.expose
class playServer(object):
    @cherrypy.tools.accept(media="text/plain")
    def GET(self, **params):
        print("Get request on play server")
        return("This is not where you belong friend")
   
    def POST(self, **params):
        print("Post requests on play server")
        return("This is not where you belong friend")


if __name__ == '__main__' :
    main.startThreads()
    finConf = {
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
    playConf = {
        "/": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
            "tools.sessions.on": True
        }
    }

    cherrypy.tree.mount(finServer(), "/", finConf)
    cherrypy.tree.mount(playServer(), "/play", playConf)
    cherrypy.engine.start()
    cherrypy.engine.block()
