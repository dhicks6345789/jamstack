# Standard Python libraries.
import os
import cgi

# The Flask library.
import flask

app = flask.Flask(__name__)

@app.route("/")
def api():
    return "Hello world!"

def runCommand(theCommand):
    commandHandle = os.popen(theCommand)
    result = commandHandle.read()
    commandHandle.close()
    return(result)

@app.route("/build")
def build():
    output = "OK"
    status = "200 OK"

    processRunning = False
    for psLine in runCommand("ps ax").split("\n"):
        if not psLine.find("build.sh") == -1:
            processRunning = True
        if not psLine.find("jekyll") == -1:
            processRunning = True

    if request.args.get("action") == "run":
        if not processRunning:
            os.system("bash /usr/local/bin/build.sh &")
        else:
            output = "ALREADYRUNNING"
    else:
        output = "NOT"
        if processRunning:
            output = "RUNNING"

    response_headers = [('Content-type', 'text/plain'), ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [output]

if __name__ == "__main__":
    app.run()
