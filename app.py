from flask import Flask, render_template, request, jsonify
import sqlite3
import json
 
app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['POST'])
def write_json():
    data = request.get_json()
    print("Received JSON data:", data)
    modified_str =''
    for char in str(data):
        if char == "'":
            modified_str += '"'
        else:
            modified_str += char
    with open('data.json', 'w') as json_file:
        json_file.write(str(modified_str))

    return render_template('index.html', temperature=data['Temperature'], humidite=data['Humidite'], pression=data['Pression'])
 
 # Ajouter les relevés 

@app.route('/api/releves', methods=['POST'])
def ajouter_releve():
    humidite = request.json['humidite']
    temperature = request.json['temperature']
    pression = request.json['pression']
    id_sonde = request.json['id_sonde']
 
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Releves (humidite, temperature, pression, id_sonde) VALUES (?,?,?,?)', (humidite, temperature, pression, id_sonde))
    conn.commit()
    conn.close()
 
    return jsonify({
         "message": "Relevé ajouté"
      })
 
 
# Récupérer les relevés
 
@app.route('/api/releves/', methods=['GET'])
def recuperer_releves():
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Releves')
    releves = cursor.fetchall()
    conn.close()
 
    liste_releves = []
 
    for releve in releves:
        dictionnaire_releves = {'id' : releve[0],
                                'humidite': releve[1],
                                'temperature': releve[2],
                                'pression': releve[3],
                                'id_sonde' : releve[4]
                                }
        liste_releves.append(dictionnaire_releves)
        
    return render_template('index.html', releves=liste_releves)


# Ajouter des utilisateurs 

@app.route('/api/utilisateurs', methods=['POST'])
def ajouter_utilisateurs():
    identifiant = request.json['identifiant']
    mot_de_passe = request.json['mot_de_passe']
 
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Utilisateurs (identiiant_utilisateur, mot_de_passe_utilisateur) VALUES (?,?)', (identifiant,mot_de_passe))
    conn.commit()
    conn.close()
 
    return jsonify({
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
 
 
    return jsonify(liste_utilisateurs)




    return render_template('index.html', temperature=data['Temperature'], humidite=data['Humidite'], pression=data['Pression'])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)