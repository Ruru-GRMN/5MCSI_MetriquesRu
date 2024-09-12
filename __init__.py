from flask import Flask, render_template, jsonify, json
from datetime import datetime
from urllib.request import urlopen
from urllib.error import URLError

app = Flask(__name__)

# Route pour afficher les commits (nécessite une modification dans commits.html pour afficher les données)
@app.route("/commits/")
def commits():
    # Simule des données pour les commits, vous pouvez utiliser l'API GitHub ici
    commit_data = [
        {"date": "2024-02-01T10:23:45Z", "message": "Initial commit"},
        {"date": "2024-02-02T14:33:21Z", "message": "Update README"},
        {"date": "2024-02-03T16:45:30Z", "message": "Fix issue #2"}
    ]
    return render_template('commits.html', commits=commit_data)

# Route pour la page d'accueil
@app.route('/')
def hello_world():
    return render_template('hello.html')  # Assurez-vous que le fichier hello.html existe

# Route pour le formulaire de contact
@app.route("/contact/")
def MaPremiereAPI():
    return render_template('formulaire.html')  # Assurez-vous que formulaire.html existe

# Route pour afficher les données météo de Tawarano
@app.route('/tawarano/')
def meteo():
    try:
        response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx', timeout=10)
        raw_content = response.read()
        json_content = json.loads(raw_content.decode('utf-8'))
        results = []
        for list_element in json_content.get('list', []):
            dt_value = list_element.get('dt')
            temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Conversion de Kelvin en °C
            results.append({'Jour': dt_value, 'temp': temp_day_value})
        return jsonify(results=results)
    except URLError as e:
        return jsonify({"error": str(e)}), 500

# Route pour afficher le graphique
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")  # Assurez-vous que graphique.html existe

if __name__ == "__main__":
    app.run(debug=True)
