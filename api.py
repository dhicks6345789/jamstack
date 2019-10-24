# The Flask library.
import flask

app = flask.Flask(__name__)

@app.route("/")
def api():
    return "Hello world!"

@app.route("/build")
def build():
    return "Build..."

if __name__ == "__main__":
    app.run()
