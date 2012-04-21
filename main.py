#!/usr/bin/env python

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.websocket import WebSocketHandler
import MySQLdb as mdb
import os, re ,fileinput
from datetime import date
import pexpect,sys,json
import string
from threading import Thread


class Loader(Thread):
    """The Loader class is a derivative of Thread that allows file loading to take place in a
    separate thread from the GUI."""

    def __init__(self, cmd,fileName, monitor, notifyWindow):
        Thread.__init__(self)
        self._notifyWindow = notifyWindow
        self.fileName = fileName
        self.cmd = cmd
        self.monitor = monitor

    def run(self):
        """Required method that is run by Thread.start() calls the function that loads the binary."""
        pexpect.run(cmd+" "+filename)
####

class Main(WebSocketHandler):
	def get(self):
		self.render("login.html");

class create_push:
    
    def __init__(self,fold,uname,bran,tok,desc):
        self.fold=fold
        self.uname=uname
        self.bran=bran
        self.tok=tok
        self.desc=desc
        
        
    def createrepo(self):
                #change directory
        folpath=""
        
        chp="/home/"+os.getlogin()+"/" + self.uname + "/Private"
        os.chdir(chp)
        folpath=" mkdir " + str(self.fold)
        os.system(folpath)
        chp="/home/"+os.getlogin()+"/" + self.uname + "/Private/" + self.fold
        os.chdir(chp)
        os.system(" touch README.md");
        print "\n"
        print os.listdir(os.getcwd())
        self.initgit()         #initgit called


    def initgit(self):
                # only INITIALISE GIT IN FOLDER
        se="curl http://github.com/api/v2/json/user/show/" + self.uname + " > username.txt";
        print se
        os.system(se);
        f = open("username.txt");
        #d = json.load(f);
        #un = "git config --global user.name \"" + str(d['user']['name']) + "\"" 
        #em=  "git config --global user.email \"" + str(d['user']['email']) +"\""
        #os.system(un)
        #os.system(em)
        os.system("git init")
        self.commitlocal(self,"commiting")       #commitlocal called- local repo commited
        self.remotel()       #remotel called - creates new repo on github
        os.system("git remote")
        self.bran="origin";     #select which remote branch you want to go to
        self.remotepush2()    #remotepush2 called - pushes on new repo



    def commitlocal(self,msg):
                #add files for commit
        os.system(" git add .")
        stri=" git commit -m \" " + msg + "\""
        
                #view log of commits
        print "\t\tLocal ->"
        os.system(stri)
        os.system(" git log")
        
                #view status of repository
        print "\t\tStatus ->"
        os.system(" git status")
        
                #view files which have been commited
        print "\t\tCommited Files ->"
        os.system(" git ls-files")




    def remotel(self):    
        #create new repo on github
        print "\t\tRemote ->"
        os.system(" git remote")
        crn="curl -F 'login=" + self.uname + "' -F 'token=" + self.tok + "' https://github.com/api/v2/json/repos/create -F 'name=" + self.fold + "' -F 'description=" + self.desc + "\'"
        print crn
        os.system(crn)
  
  
        
    def remotepush2(self):
        #define remote branch and push
        strr=" git remote add " + self.bran + " git@"+ self.uname + ":" + self.uname + "/" + self.fold + ".git"
        print strr
        os.system(strr)
        strr2="git push " + self.bran + " master"
        print strr2
        os.system(strr2)
     
        
    def pushgithub(self,msg):    #commits on local repo and pushes to remote repo
        chp="/home/"+os.getlogin()+"/" + self.uname + "/Private/" + self.fold
        os.chdir(chp)
        print "\n\n"
        print os.listdir(os.getcwd())   #shifted to local repo
        os.system("git remote")
        self.bran="origin"     #select which remote branch you want to go to
        self.commitlocal(msg)                   #commits on local repo - commitlocal() called
        self.remotepush()     #pushes to remote repo remotepush called
        
        
    #function to push on github  
    def remotepush(self):
    #    strr=" git remote add " + brname + " git@github.com:" + self.uname + "/" + self.fold + ".git"
    #    print strr
    #    os.system(strr)
        strr2="git push " + self.bran + " master"
        print strr2
        os.system(strr2)
class NoReg(WebSocketHandler):
	def open(self):
		print "Not registered user found"
	
	def on_message(self,message):
		option,filename,Type,Param=message.split('$&')
		filepath="/home/"+os.getlogin()+"/Public/"+Type+"/"+filename
		if option=="compile":
			fp=open(filepath,"w")
			fp.write(Param)
			fp.close()
			if Type=="C" :
				filename=filepath[:-2]
				os.system("g++ " + filepath + " -o " + filename+".out 2> " +filename+".err" )
			elif Type=="C++" :
				filename=filepath[:-4]
				os.system("g++ " + filepath + " -o " + filename+".out 2> " +filename+".err" )
			elif Type=="Python":
				filename=filepath[:-3]
				print filepath,filename
				os.system("python "+filepath+" > "+ filename+".out 2>  " + filename+".err")
			elif Type=="Ruby":
				filename=filepath[:-3]
				os.system("ruby "+filepath+" 2>" + filename+".err")
			elif Type=="Java":
				filename=filepath[:-5]
				os.system("javac "+filepath+" 2>" + filename+".err")
			
			fp=open(filename + ".err",'r')
			b=fp.readlines()
			line=""
			for e in b:
				line=line+e;
			fp.close()
	
				
			self.write_message("errors$&"+line)
		elif option=="execute":
			print "filename",filename
			filepath="/home/"+os.getlogin()+"/Public/"+Type+"/"+filename

			global p
			ext=filepath[-2:]
			if ext==".c" :
				filename=filepath[:-2]
				executable=filename+".out"
			elif ext=="pp" :
				
				filename=filepath[:-4]
				executable=filename+".out"
				print "execute",executable
			elif ext=="py":
				filename=filepath[:-3]
				executable="python "+filepath[:-3]+".py"
			elif ext=="rb":
				filename=filepath[:-3]
				executable="ruby "+filename+".rb"
				os.system("ruby "+filepath+" 2>" + filename+".err")
			elif ext=="va":
				filename=filepath[:-5]
				executable=filepath[:-5]
				os.system("java "+executable)
				executable="java "+executable
				
			old_stdout=sys.stdout
			sys.stdout=open(filename + ".output",'w')
			
			p=pexpect.spawn(executable)
			p.logfile_read = sys.stdout
				
			sys.stdout=old_stdout
			i=p.expect(['.*[Input:]',pexpect.EOF])
			global filename			
			fp=open(filename + ".output",'r')
			b=fp.readlines()
			line=""
			for e in b:
				line=line+e;
			fp.close()
	
			i = line.rfind("Input:");
			if len(line) - 6 == i:
				i=0;
			else:
				i=1;
			if i==0:
				self.write_message("output$&"+line)
				self.write_message("enterInput")
			elif i==1:
				self.write_message("output$&"+line)			
				
		elif option=="getParam":
			
			old_stdout=sys.stdout
			
			p.sendline(Param)
			sys.stdout=old_stdout
			
			i=p.expect(['.*[Input:]',pexpect.EOF])
			print i
			global filename
			name,ext=filename.split('.')
			filepath='/home/'+os.getlogin()+'/Public/'+Type+'/'+name + '.output'
			print filepath
			fp=open(filepath,'r')
			b=fp.readlines()
			line=""
			for e in b:
				line=line+e;
			fp.close()

			i = line.rfind("Input:");
			if len(line) - 6 == i:
				i=0;
			else:
				i=1;
			if i==0:
				self.write_message("output$&"+line)
				self.write_message("enterInput")
			elif i==1:
				
				self.write_message("output$&"+line)	
       
#handling file options
filename=""
class File(WebSocketHandler):
	p = ""

	def open(self):
		try:
			global con
			con = mdb.connect('localhost', 'root','amarok18', 'testdb');
			global cur
			cur = con.cursor()

		except mdb.Error, e:
			print "Error %d: %s" % (e.args[0],e.args[1])
			sys.exit(1)
		print "Connection for file handling"
		
	
	def on_message(self,message):
		print message
		option, user, project,Type, param=message.split("$&")
		print option
		if(option=="open"):
			print "opening file"
			fp=open(param,"r")
			lines=fp.readlines()
			line=""
			for l in lines:
				line=line+l
			self.write_message("open$&"+line);
			fp.close()
			
		elif option=="create":
			filepath="/home/"+os.getlogin()+"/"+user+"/"+Type+"/"+project+"/"+param
			fp=open(filepath,"w")
			fp.close()
			print command
			os.system(command)
			self.write_message("File created...")
			
		elif option=="save":
			print "save"
			print param
			filename,content=param.split("/~/")
			fp=open(filename,"w")
			fp.write(content)
			fp.close()
			self.write_message("File saved...")
		elif option=="compile":
			filepath=param
			ext=filepath[-2:]
			print ext
			if ext==".c" :
				global filename
				filename=filepath[:-2]
				os.system("g++ " + filepath + " -o " + filename+".out 2> " +filename+".err" )
			elif ext=="pp" :
				global filename
				filename=filepath[:-4]
				os.system("g++ " + filepath + " -o " + filename+".out 2> " +filename+".err" )
			elif ext=="py":
				global filename
				filename=filepath[:-3]
				pexpect.run("python "+filepath+" > "+ filename+".out 2>" + filename+".err")
			elif ext=="rb":
				global filename
				filename=filepath[:-3]
				os.system("ruby "+filepath+" 2>" + filename+".err")
			elif ext=="va":
				global filename
				filename=filepath[:-5]
				os.system("javac "+filepath+" 2>" + filename+".err")
			
			print "filename:"
			print filename
			fp=open(filename + ".err",'r')
			b=fp.readlines()
			line=""
			for e in b:
				line=line+e;
			fp.close()
	
				
			self.write_message("errors$&"+line)
			
				
		elif option=="execute":
			filepath=param
			global filename
			
			old_stdout=sys.stdout
			sys.stdout=open(filename + ".output",'w')
				
			global p
			global filename
			ext=filepath[-2:]
			if ext==".c" :
				global filename
				executable=filename+".out"
			elif ext=="pp" :
				global filename
				executable=filename+".out"
			elif ext=="py":
				global filename
				executable="python "+filepath[:-3]+".py"
			elif ext=="rb":
				global filename
				executable="ruby "+filepath[:-3]+".rb"
				os.system("ruby "+filepath+" 2>" + filename+".err")
			elif ext=="va":
				global filename
				executable=filepath[:-5]
				os.system("java "+executable)
				executable="java "+executable
				
			
			p=pexpect.spawn(executable)
			p.logfile_read = sys.stdout
				
			sys.stdout=old_stdout
			i=p.expect(['.*[Input:]',pexpect.EOF])
			print i
			print "hello"
			global filename			
			fp=open(filename + ".output",'r')
			b=fp.readlines()
			line=""
			for e in b:
				line=line+e;
			fp.close()
	
			i = line.rfind("Input:");
			if len(line) - 6 == i:
				i=0;
			else:
				i=1;
			if i==0:
				self.write_message("output$&"+line)
				self.write_message("enterInput")
			elif i==1:
				self.write_message("output$&"+line)			
				
		elif option=="getParam":
			filepath,par=param.split("/~/")
			print par
			global p
			
			old_stdout=sys.stdout
			
			p.sendline(par)
			sys.stdout=old_stdout
			
			i=p.expect(['.*[Input:]',pexpect.EOF])
			print i
			print "hello"
			global filename
			fp=open(filename + ".output",'r')
			b=fp.readlines()
			line=""
			for e in b:
				line=line+e;
			fp.close()

			i = line.rfind("Input:");
			if len(line) - 6 == i:
				i=0;
			else:
				i=1;
			if i==0:
				self.write_message("output$&"+line)
				self.write_message("enterInput")
			elif i==1:
				self.write_message("output$&"+line)
 			
		elif option=="debug":
			filepath=param

			ext=filepath[-2:]
			if ext==".c":
				filename=filepath[:-2]
				os.system("g++ " + filepath + " -o " + filename+".out")
				print "Compiling done"
			elif  ext=="pp":
				filename=filepath[:-4]
				os.system("g++ " + filepath + " -o " + filename+".out")
				print "Compiling done"
			elif ext=="py":
				os.system("python "+filepath+" -o "+ filename+".out 2>" + filename+".err")
			elif ext=="rb":
				os.system("ruby "+filepath+" 2>" + filename+".err")
			elif ext=="va":
				os.system("javac "+filepath+" 2>" + filename+".err")
			
				
			global p
		
			p=pexpect.spawn("gdb " + filename + ".out")
			
			p.logfile_read = open(filename + ".output",'w')
			
			i=p.expect(['.*[Input :]','.*[(gdb)]',pexpect.EOF])
			
			fp = open(filename + ".output", "r")
			tot = fp.readlines()
			fp.close()
			
			line = ""
			for eachLine in tot:
				line = line + eachLine
			if i==0 or i==1:
				self.write_message("output$&"+line)
				self.write_message("InputDebug")
			elif i==2:
				self.write_message("output$&"+line)
	
		elif option=="getParamDebug":
			filepath,par=param.split("/~/")
			print par
			global p
			
			p.sendline(par)
			
			i=p.expect(['.*[Input :]','.*[(gdb)]',pexpect.EOF])
			global filename
			fp = open(filename + ".output", "r")
			tot = fp.readlines()
			fp.close()
			
			line = ""
			for eachLine in tot:
				line = line + eachLine
			if i==0 or i==1:
				self.write_message("output$&"+line)
				self.write_message("InputDebug")
			elif i==2:
				self.write_message("output$&"+line)
	def on_close(self):
		print "file connection closed"


class sshkey:

    def __init__(self,email,uname,passwd):
        self.email=email
        self.uname=uname
        self.passwd=passwd
        
        
    def addkey(self):
        os.chdir('/home/'+os.getlogin()+'/.ssh')
        print os.listdir(os.getcwd())
        
        #key generate   
        keyg="ssh-keygen -t rsa -f ~/.ssh/" + self.uname + " -C \"" + email + "\" -P \"\""
        os.system(keyg)
        
        #add ssh key on github
        filen='/home/'+os.getlogin()+'/.ssh/'+ self.uname +'.pub'
        f=open(filen,'r')
        rsakey=f.read()
        stradd="curl -u \"" + self.uname + ":" + self.passwd + "\" http://github.com/api/v2/json/user/key/add -F \"title=ExeCode\" -F \"key=" + rsakey + "\""
        print "\n" + stradd +"\n"
        os.system(stradd)

    def editconf(self):
        stri = "\nHost " + self.uname + "\nHostname github.com\nUser git\nIdentityFile ~/.ssh/" + self.uname 
        print stri
        fout = open("config", "a")
        fout.write(stri)
        fout.close()


#handling user options
class User(WebSocketHandler):
        def open(self):
            print "New connection opened."

        def on_message(self, message):
			uname,email,pwd,token=message.split(",")
			print message
			try:
				global con
				con = mdb.connect('localhost', 'root','amarok18', 'testdb');
				global cur
				cur = con.cursor()

			except mdb.Error, e:
				print "Error %d: %s" % (e.args[0],e.args[1])
				sys.exit(1)
			validGit=False
			if(token!=""):
			#get registration info
				os.system("sudo curl -i http://github.com/api/v2/xml/user/email/"+email+" > tempAcc.txt")
				os.system("./uname tempAcc.txt > tmpAcc.txt")
				fp=open("tmpAcc.txt","r")
		
				Actual=str(fp.readline())
				fp.close()
			#check validity
				if uname==str(Actual):
					validGit=True
					usr=sshkey(email,uname,pwd)
				    #usr.addkey()
				    #usr.editconf()
					print "validGit"

			#insert into database
				
			query="select * from user where user='"+uname+"';"
			cur.execute(query)
			if(cur.rowcount==0):
				valid=True
			if validGit==True or valid==True:
				print token
				query="insert into user values('"+uname+"','"+email+"','"+pwd+"','"+token+"')"
				print query
				cur.execute(query)
				print "query executed"
				#check insertion status
				self.write_message("Registered")
			else:
				self.write_message("Account Already Exists...")

        def on_close(self):
                print "Connection closed."


def calculateKLOC(current):
	num=0;
	for top, dirs, files in os.walk(current):
		for nm in files:       
		    currentFile = os.path.join(top, nm)

		    n=0;
		    if re.search("c\Z",currentFile) or  re.search("cpp\Z",currentFile) or re.search("rb\Z",currentFile) or re.search("py\Z",currentFile) or re.search("java\Z",currentFile):
	   		        
		            for line in fileinput.input(currentFile):
		                n+=1;
		                num+=1;
		            print currentFile
		            print "\t No.of lines: " + currentFile +" has " + str(n) + "\n"
		        
	print "\n\nTotal Lines of code in folder is:" + str(num) + "\n"
	
	return str(num)
	
#handling project options
class Project(WebSocketHandler):
	def open(self):
		try:
			global con
			con = mdb.connect('localhost', 'root','amarok18', 'testdb');
			global cur
			cur = con.cursor()

		except mdb.Error, e:
			print "Error %d: %s" % (e.args[0],e.args[1])
			sys.exit(1)
		
		print "Project creation"
	
	def on_message(self,message):

		option,user,name, param=message.split(",")
		print option, user, name, param
		if(option=="create"): 
		#create new project
			desc, Type,members =param.split("$")
			print desc, Type
			
		
			if Type=="Circle":
				id1,id2,id3=members.split("&") #limited members ====> change here
				print id1, id2
				today=str(date.today())
				try: #decide if public project's entry is to be saved in db or not
					query="insert into invitations values('"+user+"','"+name+"','"+id1+"','"+today+"','Pending')"
					cur.execute(query)
					query="insert into invitations values('"+user+"','"+name+"','"+id2+"','"+today+"','Pending')"
					cur.execute(query)
				except mdb.Error, e:
					self.write_message("Error in creation"+e.args[0])
			
			try: #decide if public project's entry is to be saved in db or not
				query="insert into project values('"+name+"','"+desc+"','"+user+"')"
				cur.execute(query)

				query="select token from user where user='"+user+"';"
				cur.execute(query)
				row=cur.fetchone()
				#global repo				
				#repo=create_push(name,user,"origin",row[0],desc) #get tok from database
				#repo.createrepo()
			except mdb.Error, e:
				self.write_message("Error in creation"+str(e.args[0]))
			
			if Type!="Public":
				os.mkdir("/home/"+os.getlogin()+"/"+user+"/"+Type+"/"+name)
			else:
				print "making public repo"
				os.mkdir("/home/"+os.getlogin()+"/"+Type+"/"+name)
			
			self.write_message("Project Created...")
		elif(option=="update"):	#update project
			if(param=="GET"):
				query="select descr from project where name='"+name+"';"
				cur.execute(query)
				total=int(cur.rowcount)
				print total
				if(total==1):
					row=cur.fetchone()
					query="select * from invitations where sender='"+user+"' and project='"+name+"';"
					cur.execute(query)
					if(cur.rowcount):
						Type="circle"
					else:
						Type="private"
					self.write_message("update,SET,"+row[0]+","+Type)
				else: #if user is not owner of the project
					self.write_message("update,ERROR, ")
			else:
				#param="SET"..updating database
				pass
			print "update project"
		elif(option=="cocomo"):	# find the cocomo estimates
			#calculate the project estimate by passing the username and project name avail in user and name resp
			#find KLOC first
			path="/home/"+os.getlogin()+"/"+user+"/Circle/"+name
			print path
			KLOC=4 #float(calculateKLOC(path))
			ab=3.0
			bb=1.12
			cb=2.5
			db=0.35
			efforts=ab*pow(KLOC,bb)
			devTime=cb*pow(efforts,db)
			persons=int(efforts/devTime)
			message="cocomo,<b><h2> Estimates for Project : </b>"+name +"</h2>"+\
				"<table>"+\
				"<tr><td><b> Efforts in Person-Month : </b></td><td>"+str(efforts)+" Month/s </td></tr><br>" + \
				"<tr><td><b> Development Time (in Months) :</b></td><td>"+str(devTime)+"</td></tr><br> "+\
				"<tr><td><b> Persons Required : </b></td><td>"+str(persons)+"</td></tr><br><br>"+\
				"<tr align='center'><td><input type='button' value='Ok' class='buttonCancel'/><td></tr></table>"
					
			self.write_message(message)
					
		elif(option=="respondInvite"):
			print user +" "+ param + "ed invitation for " +name
			query="update invitations set status='"+param+"ed' where receiver in (select email from user where user='"+user+"') and project='"+name+"';"
			cur.execute(query);
			self.write_message(param);
		
		elif option=="commit":
			#global repo
			#repo.pushgithub(param)
			pass
		else:
			#save changes
			print "save changes here"
		
		

#handling tree view
class TreeView(WebSocketHandler):
	def open(self):
		print "Request for tree view"
		
	def on_message(self,message):
		print "user:",message
		Folders=[]
		Files=[]
		path=[]
		ulist=[]
		print message
		ulist.append(message)	#message is the username
		route="/home/"+os.getlogin()+"/"+ulist[0]
		path.append(route)
		for dirname, dirnames, filenames in os.walk(path[0]):
		    for subdirname in dirnames:
		        Folders.append(os.path.join(dirname, subdirname))
		    for filename in filenames:
		    	ext = os.path.splitext(filename)[-1][1:]
		    	Files.append(os.path.join(dirname, filename))
		#self.write_message("initializeDocument("+Folders+","+Files+","+path+")")
		

#showing invitations
class Invitations(WebSocketHandler):
	def open(self):
		print "Showing invitations"
		try:
			global con
			con = mdb.connect('localhost', 'root','amarok18', 'testdb');
			global cur
			cur = con.cursor()

		except mdb.Error, e:
			print "Error %d: %s" % (e.args[0],e.args[1])
			sys.exit(1)
	
	def on_message(self,message):
		print message
		query="select count(*) from invitations where receiver = (select email from user where user='"+message+"');"
		print query
		cur.execute(query)
		row = cur.fetchone()
		
		total=int(row[0])
		#self.write_message(total+" invitations")
		#self.write_message(str(row[0]))
		#query="select sender, project, senton,status from invitations where receiver = (select email from user where user='"+message+"');"
		query="select i.sender,i.project,p.descr,i.senton,i.status from invitations i, project p where p.name=i.project and receiver in (select email from user where user='"+message+"');"

		cur.execute(query)
		i=1
		if(total>0):
			row=cur.fetchone()
			message=str(total)+"$"+str(row[0])+" invited you for \
			<br> <b> Project: </b>"+ str(row[1])+\
			"<br> <b>Project Description  : </b>"+row[2]+\
			"<br><b>On</b>:" + row[3]+" <b>Status</b> : <span id='span"+row[1]+"'>"+row[4]+"</span><br>\
			<input type='button' value='Accept' id='"+row[1]+"' onclick='javascript:acceptInvite(this.id)' />" +\
			"<input type='button' value='Reject' id='"+row[1]+"' onclick='javascript:rejectInvite(this.id)' /><br>"
			print message
			while i< total:
				row=cur.fetchone()
				message=message+"&"+row[0]+" invited you for \
				<br><b> Project </b>: "+row[1]+\
				"<br><b>Project Description : </b>  "+row[2]+ \
				"<br><b>On: </b>"+ row[3]+"  <b>Status : </b>""<span id='span"+row[1]+"'>"+row[4]+"</span><br>\
				<input type='button' value='Accept' id='"+str(row[1])+"' onclick='javascript:acceptInvite(this.id)' />"+\
				"<input type='button' value='Reject' id='"+row[1]+"' onclick='javascript:rejectInvite(this.id)' /><br>"
				i=i+1
				print message
				
		self.write_message(str(message))		
		
print "Web socket server started."
HTTPServer(Application([(r"/register", User),(r"/file",File),(r"/project",Project),(r"/tree",TreeView),(r"/invitations",Invitations),(r"/noreg",NoReg)],debug=True)).listen(7777)
IOLoop.instance().start()
