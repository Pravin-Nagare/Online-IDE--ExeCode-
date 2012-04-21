import tornado.httpserver
import tornado.ioloop
import tornado.web
import os

class Main(tornado.web.RequestHandler):
	def get(self):
		Folders=[]
		Files=[]
		path=[]
		path.append(os.getcwd())
		for dirname, dirnames, filenames in os.walk(path[0]):
		    for subdirname in dirnames:
		        Folders.append(os.path.join(dirname, subdirname))
		    for filename in filenames:
		        Files.append(os.path.join(dirname, filename))
		self.render('home.html',dirList=Folders,fileList=Files,fpath=path)
   # 	for filename in filenames:
   # 	    print os.path.join(dirname, filename)"""

if __name__ == "__main__":
	settings = {
    	"static_path": os.path.join(os.path.dirname(__file__), "static"),
    	}
	application = tornado.web.Application([
		(r"/",Main),
		],debug=True,
		**settings)
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(8888)
	tornado.ioloop.IOLoop.instance().start()
