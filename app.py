from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import json
import flask
 
app = Flask(__name__, template_folder='templates')

current_user = None


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
    
    
#Utilisateurs
def connect_db():
    return sqlite3.connect('weather.db')


def ajouter_utilisateur(nom_utilisateur, mot_de_passe):
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute('INSERT INTO utilisateurs (nom_utilisateur, mot_de_passe) VALUES (?, ?)', (nom_utilisateur, mot_de_passe))
        db.commit()

def obtenir_utilisateur(nom_utilisateur):
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM utilisateurs WHERE nom_utilisateur = ?', (nom_utilisateur,))
        return cursor.fetchone()

def login_user(user_info):
    global current_user
    current_user = user_info

def get_user_info():
    global current_user
    return current_user

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nom_utilisateur = request.form['nom_utilisateur']
        mot_de_passe = request.form['mot_de_passe']

        if not nom_utilisateur or not mot_de_passe:
            return render_template('register.html')
        elif obtenir_utilisateur(nom_utilisateur):
            return render_template('register.html')
        else:
            ajouter_utilisateur(nom_utilisateur, mot_de_passe)
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nom_utilisateur = request.form['nom_utilisateur']
        mot_de_passe = request.form['mot_de_passe']

        utilisateur = obtenir_utilisateur(nom_utilisateur)

        if utilisateur and utilisateur[2] == mot_de_passe:
            login_user({'username': nom_utilisateur})
            return redirect(url_for('index'))
        else:
            return render_template('login.html')

    return render_template('login.html')




# Récupération et affichage des données sur le site 


@app.route('/')
def index():
    user_info = get_user_info
    try:
        with open('data.json') as f:
            data = json.load(f)
            
        return render_template('index.html', user_info=user_info,temperature=data.get('temperature', ''), humidite=data.get('humidite', ''),
                               pression=data.get('pression', ''))
    except FileNotFoundError:
        return "No data available."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)