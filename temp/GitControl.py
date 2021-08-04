import os
import sre_parse
from tkinter import *
from git import Repo
import time
# import pyyaml module
import yaml
from yaml.loader import SafeLoader

class APP:

    def __init__(self):
        self.root = Tk()
        self.root.geometry("200x100+0+0")
        self.local_repo_directory = os.path.dirname(os.path.dirname(__file__)) #os.getcwd()
        self.destination = ""
        self.UpdateAppIcon = PhotoImage(file='bin/update_app.png')
        self.flag = 0
    def update_label(self,*args):
        if self.flag == 0:
            self.Status.config(text="Checking updates...")
        elif self.flag ==1:
            self.Status.config(text="Checking updates..")
        elif self.flag ==2:
            self.Status.config(text="Checking updates...")

        elif self.flag ==3:
            self.Status.config(text="Done please reset the app.")
        elif self.flag ==4:
            self.Status.config(text="No changesw where detected.")
        self.flag +=1
        if self.flag >=3:
            self.flag = 0
        self.Job = self.root.after(200, self.update_label)
    def download_changes(self):
        print("Downloading new version please wait..")
        self.flag = 3
        origin = self.repo.remotes.origin
        origin.pull(self.destination)
        print("Done")
        self.Status.config(text="Done please restart the app.")
        self.root.after_cancel(self.Job)
    def Update_App(self):
        print("Update app")
        self.repo = Repo(self.local_repo_directory)
        git = self.repo.git
        self.update_label()
        RETURN = git.status()
        print("RETURN STATUS :",RETURN)
        if re.search(r"Untracked files",RETURN):
            f = open("temp.txt", "w")
            f.write(RETURN)
            f.close()
            file = open('temp.txt', 'r')
            Lines = file.readlines()
            flag = False
            file.close()


            for line in Lines:
                # Strips the newline character
                Value = line.strip()
                #print(Value)
                if re.search(r"to include in what will be committed",line):
                    flag = True
                elif flag and Value is not "":
                    os.remove(line.strip())
                elif flag and  Value == "":
                    break
            os.remove("temp.txt")
            git.checkout("-f")# Remove local changes
            self.download_changes()
        elif re.search(r"Changes not staged for commit",RETURN):
            git.checkout("-f")# Remove local changes
            print("Removing local changes...")
            self.download_changes()
        elif re.search(r"Your branch is behind",RETURN):
            print("Downloading remote changes...")
            self.download_changes()

        else:
            self.flag = 5
            self.root.after_cancel(self.Job)
            self.Status.config(text="No updates detected")

        self.ReadYaml()

    def ReadYaml(self):
        # Open the file and load the file
        print("Reading requirement.yaml file ............................")
        with open('Requirement.yaml') as f:
            data = yaml.load(f, Loader=SafeLoader)
            #print(data["PLC"])
            DATA = data["PLC"]
            print(DATA["imge_name"])
            print(DATA["version"])
            print(DATA["path"])
            print(DATA["description"])

    def Run(self):
        self.Label = Label(self.root,text="Check for updates")
        self.Label.grid(row=0,column=0)
        self.Status = Label(self.root,text="  ")
        self.Status.grid(row=1,column=0)
        if os.path.exists(self.local_repo_directory):
            print("Running app..")
            self.BtnUpdate = Button(self.root, text="None",image=self.UpdateAppIcon,command =self.Update_App)
            self.BtnUpdate.grid(row=3,column=0)
        #If the ropo does not exists the clone from GitHub
        '''else:
            print("Directory does no exists ...")
            Repo.clone_from("https://github.com/InteractiveToysComp/plc_farstation.git",
                            self.local_repo_directory,branch=self.destination)'''

    def add_and_commit_changes(self,repo):
        print("Commiting chanfes..")
        self.repo.git.add(update=True)
        self.repo.git.commit("-m","Adding new features to existing code...")

    def push_changes(self,repo):
        print("Push changes...")
        repo.git.push("--set-upstream","origin",self.destination)


App = APP()
App.Run()
App.root.mainloop()
