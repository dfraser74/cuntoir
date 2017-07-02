import cherrypy
import os

conf = {'server.socket_port':80,
        'server.socket_host':'0.0.0.0'
    }

cherrypy.config.update(conf)

class redirectServer(object): pass

config = {
    "/":{
        'tools.response_headers.headers': [('Content-Type', 'text/html')],
        'tools.staticdir.root': os.path.abspath(os.getcwd()),
        'tools.staticdir.on': True,
        'tools.staticdir.dir': "static/",
        'tools.staticdir.index': "redirect.html"
        }
}
cherrypy.quickstart(redirectServer(), "/", config)
