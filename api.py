# Standard Python libraries.
import os
import re
import sys
import uuid
import time
import json
import pickle
import sqlite3
import logging
import datetime
import collections

# Import the Flask web application framework.
import flask

# APScheduler, a task scheduling library for Python.
import apscheduler.schedulers.background

app = flask.Flask(__name__)
app.config['DEBUG'] = False
app.config['TESTING'] = False

# The folder on the server where the application's working data will be kept.
appFolder = "/var/www/api"

# Use Flask's application context to store a database connection. Note that we set the database to return
# sqlite3.Row objects which allow us to index elements by key (x["bananas"]) or by number (x[0]).
def getDB():
    db = getattr(flask.g, '_database', None)
    if db is None:
        db = flask.g._database = sqlite3.connect(appFolder + os.sep + "database" + os.sep + "api.db")
        db.row_factory = sqlite3.Row
    return db

# Query the database - a handy function to send a query to the database, dealing with getting the
# database and a cursor and doing a commit and cursor close at the end. If "one" is set to True then
# only the first result row is returned, otherwise an array of result rows will be returned.
def queryDB(query, args=(), one=False):
    theDB = getDB()
    cur = theDB.execute(query, args)
    theDB.commit()
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# Initialise the application.
@app.before_first_request
def setup():
    # We need to set up logging - trying to debug issues with schedualed tasks is impossible otherwise.
    # Just log errors, otherwise our web logs will fill up with "The schedualed task ran!" messages.
    # See: https://stackoverflow.com/questions/28724459/no-handlers-could-be-found-for-logger-apscheduler-executors-default
    log = logging.getLogger('apscheduler.executors.default')
    log.setLevel(logging.ERROR)
    fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    h = logging.StreamHandler()
    h.setFormatter(fmt)
    log.addHandler(h)
        
# The Flask web server only deals with "/api/..." URLs. Redirect the Flask web server's index page (i.e. "/api/") to the main web server to serve the
# staticlly-generated API HTML documentation - from there we can include graphics and so on if wanted.
@app.route("/")
def root():
    return flask.redirect("/api.html", code=302)

# A function called when the application ends (i.e. in our case, when Apache is stopped / restarted).
# Makes sure the database connection is properly closed.
@app.teardown_appcontext
def teardownApplication(exception):
    db = getattr(flask.g, '_database', None)
    if db is not None:
        db.close()
