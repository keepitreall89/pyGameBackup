### Game config backups
import shutil
import os
import datetime
import hashlib
import logging
import pathlib

#Set up initial variables. Users can edit this section
def main(games=[]):
    ### Logging Variables
    #Set to False to Disable log file.
    logging=True
    #Set this variable to True if you want the log file to contain only the most recent program run.
    createNewLogEachRun=True
    #Max log file only applies if createNewLogEachRun is set to False. If the log file reaches the
    #size below (in Bytes), it deletes the log and begins a fresh new one.
    #setting to -1 or 0 will cause the program to NEVER delete the log and start a new one automatically.
    maxLogSize=3000000 #3 MB max size
    #Setting silent to True will cause no output statements to be printed in the console window.
    silent=False
    

    #Recommended to set 'path' to an empty folder that you just created, or at least one without
    #a lot or large zip files already existing in it.
    path = "E:/OneDrive/Game Cfg files/"
    localAppDataPath = os.getenv('LOCALAPPDATA')
    roamingAppDataPath = localAppDataPath[0:len(localAppDataPath)-5]+"Roaming/"
    myDocumentsPath = str(pathlib.Path.home())+"/Documents/"

    #You need to create this folder before running script.
    tempPath = "C:/tempPy/"
    logPath = "C:/tempPy/GameBackups.log"

    #Add all games/folders that you want backed up in the same format as below.
    
    #Append Bioshock
    #games.append(Game("Bioshock 1 CFG", roamingAppDataPath+"BioshockHD/"))
    #games.append(Game("Bioshock 1 MyDocs", myDocumentsPath+"BioshockHD/"))
    #Append Logitech G13 Files
    games.append(Game("LogitechG13", localAppDataPath+"/Logitech/"))
    
    #Append SWTOR
    games.append(Game("SWTOR", localAppDataPath+"/SWTOR/"))

    #Append L.A Noire
    games.append(Game("LA NOIRE", myDocumentsPath+"/Rockstar Games/"))

    #Append C&C Zero Hour
    #games.append(Game("CCGenerals", myDocumentsPath+"/Command and Conquer Generals Data/"))
    #games.append(Game("CCGeneralsZH", myDocumentsPath+"/Command and Conquer Generals Zero Hour Data/"))

    #Append M10 Mouse files
    #games.append(Game("M10Mouse", myDocumentsPath+"/Level 10 M/"))

    #Append Cheat Engine Tables
    #games.append(Game("CheatEngineTables", myDocumentsPath+"/My Cheat Tables/"))

    #NOT RECOMMMENDED TO DO THIS IF YOU HAVE A LOT OF FOLDERS HERE.
    #in that case, take the time to individually add each subfolder, trust me.
    #Append My Games (My Docs) folder
    #games.append(Game("MyGames", myDocumentsPath+"/My Games/"))

    #Append BF1 Configs
    games.append(Game("BF1 Config", myDocumentsPath+"Battlefield 1/settings/"))

    runBackup(silent, logging, logPath, createNewLogEachRun, maxLogSize, path, tempPath, games)



#Do not mess with anything below this.
def runBackup(silent, logging, logPath, createNewLog, maxLogSize, path, tempPath, games):
    log = []
    backupsMd5s = []
    duplicateDeleted=0
    newCreated=0
    #Create time string for current time that program was started, down to seconds.
    dateObj = datetime.datetime.today()
    date = dateObj.strftime("%y%m%d%H%M%S")
    if not silent:
        print("Starting at:\t%s" % dateObj)
        print("Backup Path:\t%s" % path)
        print("Temporary path for Zipping:\t%s" % tempPath)
        print("Log file path:\t%s" % logPath)
        print("Logging:\t%s" % logging)
        print("Create New Log Each Run:\t%s" % createNewLog)
        print("Max log size:\t%s" % maxLogSize)

    #logging setup
    if logging:
        if createNewLog:
            flog = open(logPath, 'w')
        else:
            #Test all cases for variable log sizing
            if maxLogSize!=0 or maxLogSize!=-1:
                try:
                    logSize=os.path.getsize(logPath)
                    if logSize>maxLogSize:
                        flog=open(logPath, 'w')
                    else:
                        flog=open(logPath, 'a')
                        log.append("\n\n\n")
                except IOError:
                    if not silent:
                        print("Log file error while checking size: "+IOError)
                    flog=open(logPath, 'w')
            else:
                flog=open(logPath, 'a')
                log.append("\n\n\n")
        log.append("Starting:\t"+str(dateObj))
        log.append("\tBackup Path:\t"+path)
        log.append("\tTemporary Path:\t"+tempPath)
        log.append("\tLog Path (this file dumbass):\t"+logPath)
        clearLogBuffer(flog, log, silent)
        log = []

    #Create list of zip files already in backup folder
    backups = findFiles(path, ".zip")
    #Get MD5 for each backup already there
    for b in backups:
        backupsMd5s.append(getMd5(silent, b))

    if logging:
        log.append("\tExisting ZIP files in Backup location")
        if len(backups)==len(backupsMd5s):
            x=0
            for b in backups:
                log.append("\t\t"+str(x)+".\t"+b+"\tMD5: \t"+backupsMd5s[x])
                x+=1
        elif len(backups)==0:
            log.append("\t\tNo Existing ZIP files! Congrats noob")
        else:
            log.append("\t\t\tDifferent number of ZIPs vs MD5s... Maybe an error occured calculating MD5s")
            log.append("\t\t\tFiles:")
            x=0
            for b in backups:
                log.append("\t\t\t\t"+str(x)+".\t"+b)
                x+=1
            x=0
            log.append("\t\t\tMD5s:")
            for b in backupsMd5s:
                log.append("\t\t\t\t"+str(x)+".\t"+b)
                x+=1
        clearLogBuffer(flog, log, silent)
        log=[]
        
    for g in games:
        if not silent:
            print("\tTitle:\t%s" %g.title)
        shutil.make_archive(tempPath+g.title+"."+date, "zip" , g.path)
        if not silent:
            print("\t\tCreated: "+tempPath+g.title+"."+date+".zip")
        if logging:
            log.append("\t\tCreated: "+tempPath+g.title+"."+date+".zip")
        duplicate, olderBackup = checkDuplicates(backupsMd5s, getMd5(silent,tempPath+g.title+"."+date+".zip"))
        if duplicate:
            if not silent:
                print("\t\t\tArchive is duplicate of: "+backups[olderBackup])
            if logging:
                log.append("\t\t\tArchive is duplicate of: "+backups[olderBackup])
                log.append("\t\t\tDeleting:\t"+tempPath+g.title+"."+date+".zip")
            os.remove(tempPath+g.title+"."+date+".zip")
            duplicateDeleted+=1
        else:
            if logging:
                log.append("\t\t\tNo Duplicate")
            shutil.move(tempPath+g.title+"."+date+".zip", path+g.title+"."+date+".zip")
            if not silent:
                print("\t\t\tMoved to: "+path)
            if logging:
                log.append("\t\t\tMoved to:/t"+path)
            newCreated+=1
        if logging:
            clearLogBuffer(flog, log, silent)
            log=[]
    endDateObj=datetime.datetime.today()
    if not silent:
        print("Summary")
        print("\tNew backups created:\t%d" % newCreated)
        print("\tBackups not created, already up to date:\t%d" % duplicateDeleted)
        print("\tEnding:\t%s" % endDateObj)
        print("\tTime Taken:\t%s" %(endDateObj-dateObj))
    if logging:
        log.append("\n\nSummary")
        log.append("\tNew backups created:\t%d" % newCreated)
        log.append("\tBackups not created, already up to date:\t%d" % duplicateDeleted)
        log.append("\tEnding:\t%s" % endDateObj)
        log.append("\tTime Taken:\t%s" % (endDateObj-dateObj))
        if len(log)>0:
            clearLogBuffer(flog, log, silent)
            log=[]
        flog.close()



class Game:
    def __init__(self, title, path):
        self.title=title
        self.path=path

def findFiles(path, ext):
    files = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            if ext in filename:
                files.append(dirpath+filename)
    return files

def getMd5(silent,path):
    mash = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            mash.update(chunk)
    text=mash.hexdigest()
    if not silent:
        print("\tFile: %s \thas MD5: %s" % (path, text))
    return text

def checkDuplicates(targetList, item):
    x = 0
    for i in targetList:
        if item==i:
            return True, x
        x+=1
    return False, -1

def clearLogBuffer(f, l, silent=False):
    try:
        for item in l:
            f.write(item+"\n")
        f.write("\n")
        print("Wrote %d log lines." % len(l))
        return True
    except:
        return False




main()
        

    
#todo
#check if game dir exists
#check if temp dir exists; if not, try to create.
#restore function? or include in ZIP where to extract.
    
