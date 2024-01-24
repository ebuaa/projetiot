import flask
import sqlite3
 
app = flask.Flask(__name__, template_folder='templates')
 
 # Ajouter les relevés 

@app.route('/api/releves', methods=['POST'])
def ajouter_releve():
    humidite = flask.request.json['humidite']
    temperature = flask.request.json['temperature']
    pression = flask.request.json['pression']
    horodatage = flask.request.json['horodatage']
    id_sonde = flask.request.json['id_sonde']
 
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Releve (humidite_releve, temperature_releve, pression_releve, horodatage_releve, id_sonde) VALUES (?,?,?,?,?)', (humidite,temperature,pression,horodatage, id_sonde))
    conn.commit()
    conn.close()
 
    return flask.jsonify({
         "message": "Relevé ajouté"
      })
 
 
# Récupérer les relevés
 
@app.route('/api/releves/', methods=['GET'])
def recuperer_releves():
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM releve')
    releves = cursor.fetchall()
    conn.close()
 
    liste_releves = []
 
    for releve in releves:
        dictionnaire_releves = {'id' : releve[0],
                                'humidite': releve[1],
                                'temperature': releve[2],
                                'pression': releve[3],
                                'horodatage': releve[4],
                                'id_sonde' : releve[5]
                                }
        liste_releves.append(dictionnaire_releves)
 
 
    return flask.jsonify(liste_releves)


# Ajouter des utilisateurs 

@app.route('/api/utilisateurs', methods=['POST'])
def ajouter_releve():
    identifiant = flask.request.json['identifiant']
    mot_de_passe = flask.request.json['mot_de_passe']
 
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Utilisateurs (identiiant_utilisateur, mot_de_passe_utilisateur) VALUES (?,?)', (identifiant,mot_de_passe))
    conn.commit()
    conn.close()
 
    return flask.jsonify({
         "message": "Utilisateur ajouté"
      })
 
# Récupérer les utilisateurs 

@app.route('/api/utilisateurs/', methods=['GET'])
def recuperer_utilisateurs():
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Utilisateurs')
    utilisateurs = cursor.fetchall()
    conn.close()
 
    liste_utilisateurs = []
 
    for utilisateur in utilisateurs:
        dictionnaire_utilisateurs = {'id' : utilisateur[0],
                                    'identifiant': utilisateur[1],
                                    'mot_de_passe': utilisateur[2]
                                    }
        liste_utilisateurs.append(dictionnaire_utilisateurs)
 
 
    return flask.jsonify(liste_utilisateurs)


