import tornado.httpserver
import tornado.ioloop
import tornado.web
import getpass
import tornado.ioloop
import string
import MySQLdb as mdb
import os,pexpect


uname=""

#login handling
class Login(tornado.web.RequestHandler):
	con = None
	cur=None
	
	def post(self,op):
		try:
			con = mdb.connect('localhost', 'root','amarok18', 'testdb');
			global cur
			cur = con.cursor()

		except mdb.Error, e:
			print "Error %d: %s" % (e.args[0],e.args[1])
			sys.exit(1)
		global uname
		uname=self.get_argument('uname')
		pwd=self.get_argument('pwd')
		query="SELECT pwd,token FROM user where user='"+uname+"'"
		cur.execute(query)
		numrows = int(cur.rowcount)
		if numrows==0 :
			self.write("<html><body><h3>Not registered :-( </h3></body></html>")
		else:
			row = cur.fetchone()
			if pwd==row[0]:
				#set cookie
				me=os.getlogin()
				print me
				
				#get the repo's here
				
				try:
					os.makedirs("/home/"+me+"/"+uname)
					os.makedirs("/home/"+me+"/"+uname+"/Private")
					os.makedirs("/home/"+me+"/"+uname+"/Circle")
				except:
					pass
				
				token=str(row[1])
				if(token!=""):
					cmd="sudo curl http://github.com/api/v2/json/repos/show/"+uname+ " > repo.txt"
					os.system(cmd)
					os.system("./repoDown "+uname+" "+me)	#make this a daemon process	===> downloads private projects only
				
				#---cloning into Circles Folder of user=uname
				query="select sender, project from invitations where status='Accepted' and receiver in(select email from user where user='"+uname+"');"
				cur.execute(query)
				numrows=cur.rowcount
				i=0
				while(i<numrows):
					row=cur.fetchone()
					i+=1
					cmd="git clone http://github.com/"+str(row[0])+"/"+str(row[1])+".git  /home/"+os.getlogin()+"/"+uname+"/Circle/"+str(row[1])+".git"
					if(token!=""):
						os.system(cmd)
				self.redirect("/home/file=""&project=""&total=5&inv=false&msg=10")
			else:
				self.write("Password mis-match")

class Home(tornado.web.RequestHandler):
	def get(self,url=None):
		Folders=[]
		Files=[]
		path=[]
		ulist=[]

		global uname
		print 'username in Home class : %s' %(uname)
		route="/home/"+os.getlogin()+"/"+str(uname)
		print "route",route
		path.append(route)
				
		for dirname, dirnames, filenames in os.walk(path[0]):
		    for subdirname in dirnames:
		        Folders.append(os.path.join(dirname, subdirname))
		    for filename in filenames:
		    	ext = os.path.splitext(filename)[-1][1:]
		    	Files.append(os.path.join(dirname, filename))
		self.render('home.html',dirList=Folders,fileList=Files,path=path)
		"""print path[1]	    	
		for dirname, dirnames, filenames in os.walk(path[1]):
		    for subdirname in dirnames:
		        Folders.append(os.path.join(dirname, subdirname))
		    for filename in filenames:
		    	ext = os.path.splitext(filename)[-1][1:]
		    	Files.append(os.path.join(dirname, filename)) 
			    	      
		self.render('home.html',dirList=Folders,fileList=Files,path=path)"""

class Main(tornado.web.RequestHandler):
	def get(self):
		os.system("mkdir /home/"+os.getlogin()+"/Public/C")
		os.system("mkdir /home/"+os.getlogin()+"/Public/C++")
		os.system("mkdir /home/"+os.getlogin()+"/Public/Java")
		os.system("mkdir /home/"+os.getlogin()+"/Public/Ruby")
		os.system("mkdir /home/"+os.getlogin()+"/Public/Python")								
		self.render("login.html");

if __name__ == "__main__":
	settings = {
    	"static_path": os.path.join(os.path.dirname(__file__), "static"),
    	}
	application = tornado.web.Application([
		(r"/",Main),
		(r"/(login)",Login),
		(r"/home[a-zA-Z\/\=\"\&0-9]*",Home)
		],debug=True,
		**settings)
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(8888)
	tornado.ioloop.IOLoop.instance().start()
