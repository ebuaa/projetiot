import sqlite3

# Établir une connexion à la base de données ou la créer si elle n'existe pas
connection = sqlite3.connect("weather.db")

cursor = connection.cursor()

# Définir la table Utilisateurs
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Utilisateurs
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_utilisateur TEXT NOT NULL,
        mot_de_passe TEXT NOT NULL,
        email TEXT NOT NULL
    )
''')

# Définir la table Sonde
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Sonde
    (
        id_sonde INTEGER PRIMARY KEY AUTOINCREMENT,
        active BOOL NOT NULL
    )
''')

# Définir la table Releves
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Releves
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_sonde INTEGER,
        humidite INT NOT NULL,
        temperature FLOAT NOT NULL,
        pression FLOAT NOT NULL,
        FOREIGN KEY (id_sonde) REFERENCES Sonde(id_sonde)
    )
''')
cursor.execute('INSERT INTO Sonde (id_sonde, active) VALUES (?, ?)', (1, 1))


# Valider les insertions dans la base de données
connection.commit()

# Fermer la connexion à la base de données
connection.close()