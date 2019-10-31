# Standard Python libraries.
import os
import re
import cgi
import hashlib

# The Flask library.
import flask

app = flask.Flask(__name__)

def getFile(theFilename):
    fileDataHandle = open(theFilename, encoding="latin-1")
    fileData = fileDataHandle.read()
    fileDataHandle.close()
    return(fileData)

def putFile(theFilename, theData):
    fileDataHandle = open(theFilename, encoding="latin-1", "w")
    fileDataHandle.write(fileData)
    fileDataHandle.close()

def runCommand(theCommand):
    commandHandle = os.popen(theCommand)
    result = commandHandle.read()
    commandHandle.close()
    return(result)

@app.route("/")
def api():
    return "Hello world!"

@app.route("/build")
def build():
    processRunning = False
    for psLine in runCommand("ps ax").split("\n"):
        if not psLine.find("build.sh") == -1:
            processRunning = True

    if flask.request.args.get("action") == "run":
        correctPasswordHash = getFile("/var/local/buildPassword.txt")
        passedPasswordHash = hashlib.sha256(flask.request.args.get("password")).hexdigest()        
        if passedPasswordHash == correctPasswordHash:
            if not processRunning:
                os.system("bash /usr/local/bin/build.sh &")
            return "RUNNING"
        return "WRONGPASSWORD"
    elif flask.request.args.get("action") == "getStatus":
        if processRunning:
            return "RUNNING"
        else:
            return "NOTRUNNING"
    elif flask.request.args.get("action") == "getLogs":
        return re.sub(".\[\d*?m", "", getFile("/var/log/build.log"))
    else:
        return getFile("/var/www/api/build.html")
    
if __name__ == "__main__":
    app.run()
