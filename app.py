from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import json
import flask
from datetime import datetime
 
app = Flask(__name__, template_folder='templates')

current_user = None

 # Ajout des relevés dans la table Releves
@app.route('/api/ajout', methods=['POST'])
def ajouter_releves():
    if request.method == 'POST':
        data = request.get_json()
        temperature = data['temperature']
        humidite = data['humidite']
        pression = data['pression']

        connection = sqlite3.connect('weather.db')
        cursor = connection.cursor()

        cursor.execute('INSERT INTO Releves (temperature, humidite, pression) VALUES (?, ?, ?)', (temperature, humidite, pression))
        connection.commit()
        connection.close()

        return "Relevés reçus et importés avec succès"
    
    
#Utilisateurs
def connect_db():
    return sqlite3.connect('weather.db')


def ajouter_utilisateur(nom_utilisateur, mot_de_passe, email):
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute('INSERT INTO utilisateurs (nom_utilisateur, mot_de_passe, email) VALUES (?, ?, ?)', (nom_utilisateur, mot_de_passe, email))
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

# Enregistrement utilisateur 

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nom_utilisateur = request.form['nom_utilisateur']
        mot_de_passe = request.form['mot_de_passe']
        email = request.form['email']

        if not nom_utilisateur or not mot_de_passe or not email:
            return render_template('register.html')
        elif obtenir_utilisateur(nom_utilisateur):
            return render_template('register.html')
        else:
            ajouter_utilisateur(nom_utilisateur, mot_de_passe, email)
            return redirect(url_for('login'))

    return render_template('register.html')

# Connexion utilisateur 

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


@app.route('/home')
def index():
    user_info = get_user_info()
    
    connection = sqlite3.connect('weather.db')
    cursor = connection.cursor()

    cursor.execute('SELECT temperature, humidite, pression FROM Releves ORDER BY id DESC LIMIT 1')
    data = cursor.fetchone()
    connection.close()
    if data:
        temperature, humidite, pression = data
    else:
        temperature, humidite, pression = '', '', ''

    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    return render_template('index.html', temperature=temperature, humidite=humidite,
                            pression=pression, current_time=current_time, user_info=user_info)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)