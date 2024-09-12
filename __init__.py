from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm2
  
@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def mon_histogramme():
    return render_template("histogramme.html")

import requests
from datetime import datetime
from flask import jsonify

@app.route("/commits/")
def get_commits():
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = requests.get(url)
    commits_data = response.json()

    # Extraire les minutes de chaque commit
    commit_minutes = []
    for commit in commits_data:
        date_str = commit['commit']['author']['date']
        date_object = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
        commit_minutes.append(date_object.minute)

    # Compter le nombre de commits pour chaque minute
    minute_count = {}
    for minute in commit_minutes:
        minute_count[minute] = minute_count.get(minute, 0) + 1

    # Préparer les données pour l'affichage du graphique
    results = [{"minute": minute, "count": count} for minute, count in minute_count.items()]
    return jsonify(results=results)

@app.route("/commits_graph/")
def commits_graph():
    return render_template("commits.html")


if __name__ == "__main__":
  app.run(debug=True)
