from flask import Flask, render_template, request, jsonify
import sqlite3
import json
 
app = Flask(__name__, template_folder='templates')

@app.route('/writejson', methods=['POST'])
def write_json():
    data = request.get_json()
    print("Received JSON data:", data)
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file)

    return "JSON data received and written successfully"

 
 # Ajouter les relevés 

@app.route('/api/releves', methods=['POST'])
def ajouter_releve():
    try:
        data = request.json
        print("Received JSON data:", data)

        humidite = data.get('humidite')
        temperature = data.get('temperature')
        pression = data.get('rression')
        id_sonde = data.get('id_sonde')

        if None in (humidite, temperature, pression, id_sonde):
            return jsonify({"error": "Les données requises sont manquantes ou incorrectes"}), 400

        conn = sqlite3.connect("weather.db")
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Releves (humidite, temperature, pression, id_sonde) VALUES (?,?,?,?)',
                       (humidite, temperature, pression, id_sonde))
        conn.commit()
        conn.close()

        return jsonify({"message": "Relevé ajouté"})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Une erreur s'est produite lors du traitement de la requête"}), 500

 
 
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

# @app.route('/api/utilisateurs', methods=['POST'])
# def ajouter_utilisateurs():
#     identifiant = request.json['identifiant']
#     mot_de_passe = request.json['mot_de_passe']
 
#     conn = sqlite3.connect("weather.db")
#     cursor = conn.cursor()
#     cursor.execute('INSERT INTO Utilisateurs (identiiant_utilisateur, mot_de_passe_utilisateur) VALUES (?,?)', (identifiant,mot_de_passe))
#     conn.commit()
#     conn.close()
 
#     return jsonify({
#          "message": "Utilisateur ajouté"
#       })
 
# Récupérer les utilisateurs 

# @app.route('/api/utilisateurs/', methods=['GET'])
# def recuperer_utilisateurs():
#     conn = sqlite3.connect("weather.db")
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM Utilisateurs')
#     utilisateurs = cursor.fetchall()
#     conn.close()
 
#     liste_utilisateurs = []
 
#     for utilisateur in utilisateurs:
#         dictionnaire_utilisateurs = {'id' : utilisateur[0],
#                                     'identifiant': utilisateur[1],
#                                     'mot_de_passe': utilisateur[2]
#                                     }
#         liste_utilisateurs.append(dictionnaire_utilisateurs)
 
 
#     return jsonify(liste_utilisateurs)



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