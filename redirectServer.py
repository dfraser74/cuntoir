import cherrypy

conf = {'server.socket_port':80,
        'server.socket_host':'0.0.0.0'
    }

cherrypy.config.update(conf)

class redirectServer(object):
    @cherrypy.expose()
    def index(self):
        with open("static/redirect.html", "r") as redirectFile:
            returnString = redirectFile.read()
        return(returnString)
cherrypy.quickstart(redirectServer(), "/")
