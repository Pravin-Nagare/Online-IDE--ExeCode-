import os
import json


class create_push:
    
    def __init__(self,fold,uname,bran,tok):
        self.fold=fold
        self.uname=uname
        self.bran=bran
        self.tok=tok
        
        
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
        os.system(" git init")
        self.commitlocal()       #commitlocal called- local repo commited
        self.remotel()       #remotel called - creates new repo on github
        os.system("git remote")
        self.bran=raw_input("Enter remote branch ");     #select which remote branch you want to go to
        self.remotepush2()    #remotepush2 called - pushes on new repo



    def commitlocal(self):
                #add files for commit
        os.system(" git add .")
        stri=" git commit -m \" " + (raw_input("Enter message for commit:")) + "\""
        
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
        crn="curl -F 'login=" + self.uname + "' -F 'token=" + self.tok + "' https://github.com/api/v2/json/repos/create -F 'name=" + self.fold + "' -F 'description=" + raw_input("Enter description for project: ") + "\'"
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
     
        
    def pushgithub(self):    #commits on local repo and pushes to remote repo
        chp="/home/"+os.getlogin()+"/" + self.uname + "/Private/" + self.fold
        os.chdir(chp)
        print "\n\n"
        print os.listdir(os.getcwd())   #shifted to local repo
        os.system("git remote")
        self.bran=raw_input("Enter remote branch ");     #select which remote branch you want to go to
        self.commitlocal()                   #commits on local repo - commitlocal() called
        self.remotepush()     #pushes to remote repo remotepush called
        
        
    #function to push on github  
    def remotepush(self):
    #    strr=" git remote add " + brname + " git@github.com:" + self.uname + "/" + self.fold + ".git"
    #    print strr
    #    os.system(strr)
        strr2="git push " + self.bran + " master"
        print strr2
        os.system(strr2)
