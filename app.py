from flask import Flask, jsonify, request, redirect, g, render_template, session
from flask_cors import CORS
from api import league


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'super secret key'

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route("/table/", methods=['GET'])
def table():
    live_table = league.getLiveLeagueTable()
    return jsonify(live_table)

@app.route("/history/", methods=['GET'])
def history():
    teams_history = league.getTeamsData()
    return jsonify(teams_history)

@app.route("/fixtures/<id>/", methods=['GET'])
def fixtures(id):
    fixtures = league.getFixtures(id)
    return jsonify(fixtures)

@app.route("/current/", methods=['GET'])
def current():
    gw = league.getCurrent()
    return jsonify(gw)

@app.route("/owner/<id>/", methods=['GET'])
def owner(id):
    owner = league.getOwner(id)
    return jsonify(owner)

if __name__ == '__main__':
    app.run(host='192.168.1.142')