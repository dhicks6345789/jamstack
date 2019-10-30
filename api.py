# Standard Python libraries.
import os
import cgi

# The Flask library.
import flask

app = flask.Flask(__name__)

def getFile(theFilename):
    fileDataHandle = open(theFilename)
    fileData = fileDataHandle.read()
    fileDataHandle.close()
    return(fileData)

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
        if not processRunning:
            os.system("bash /usr/local/bin/build.sh &")
        return "RUNNING"
    elif flask.request.args.get("action") == "query":
        if processRunning:
            return "RUNNING"
        else:
            return "NOTRUNNING"
    else:
        return getFile("/var/www/api/build.html")
    
if __name__ == "__main__":
    app.run()
