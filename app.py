from flask import Flask, render_template, request, jsonify
import sqlite3
import json
import flask
 
app = Flask(__name__, template_folder='templates')


# Récupération fichier JSON 


@app.route('/writejson', methods=['POST'])
def write_json():
    data = request.get_json()
    print("Received JSON data:", data)
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file)

    return "JSON data received and written successfully"

 
 # Ajout des relevés dans la table Releves

@app.route('/api/ajout', methods=['POST'])
def ajouter_releves():

    if flask.request.method == 'POST':
        temperature = flask.request.json['temperature']
        humidite = flask.request.json['humidite']
        pression = flask.request.json['pression']

        connection = sqlite3.connect('weather.db')

        cursor = connection.cursor()

        cursor.execute('INSERT INTO Releves (temperature, humidite, pression) VALUES ("' + temperature + '","' + humidite + '","' + pression + '")')
        connection.commit()
        connection.close()

        return "Relevés reçus et importés avec succès"



# Récupération et affichage des données sur le site 


@app.route('/')
def index():
    try:
        with open('data.json') as f:
            data = json.load(f)
            
        return render_template('index.html', temperature=data.get('temperature', ''), humidite=data.get('humidite', ''),
                               pression=data.get('pression', ''))
    except FileNotFoundError:
        return "No data available."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)