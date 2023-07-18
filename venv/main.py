import tkinter as tk
import mysql.connector
from tkinter import ttk



def afficher_details_match(event):
    # Récupérer l'identifiant du match sélectionné
    selected_match = treeview.focus()
    match_id = treeview.item(selected_match)['values'][0]

    # Établir la connexion à la base de données
    cnx = mysql.connector.connect(
        user='root',
        password='',
        host='localhost',
        database='super_bowl'
    )
    cursor = cnx.cursor()

    # Récupérer les détails du match à partir de la base de données
    query = "SELECT equipe1.nom_equipe, equipe2.nom_equipe, matchs.heur_debut, matchs.heur_fin FROM matchs " \
            "INNER JOIN equipe AS equipe1 ON matchs.equipe1_id = equipe1.id_equipe " \
            "INNER JOIN equipe AS equipe2 ON matchs.equipe2_id = equipe2.id_equipe " \
            "WHERE matchs.id_match = %s"
    cursor.execute(query, (match_id,))
    result = cursor.fetchone()

    # Afficher les détails du match
    if result:
        equipe1_nom = result[0]
        equipe2_nom = result[1]
        heure_debut = result[2]
        heure_fin = result[3]

        details_label.config(text=f"Équipe 1: {equipe1_nom}\n"
                                  f"Équipe 2: {equipe2_nom}\n"
                                  f"Heure de début: {heure_debut}\n"
                                  f"Heure de fin: {heure_fin}")
    else:
        details_label.config(text="Détails non disponibles pour ce match.")

    cursor.close()
    cnx.close()

# Établir la connexion à la base de données
cnx = mysql.connector.connect(
    user='root',
    password='',
    host='localhost',
    database='super_bowl'
)
cursor = cnx.cursor()

# Récupérer tous les matchs du jour à partir de la base de données
query = "SELECT matchs.id_match, equipe1.nom_equipe, equipe2.nom_equipe FROM matchs " \
        "INNER JOIN equipe AS equipe1 ON matchs.equipe1_id = equipe1.id_equipe " \
        "INNER JOIN equipe AS equipe2 ON matchs.equipe2_id = equipe2.id_equipe " \
        "WHERE CURDATE() = DATE(matchs.heur_debut)"
cursor.execute(query)
matches = cursor.fetchall()

# Fermer le curseur et la connexion
cursor.close()
cnx.close()

# Créer la fenêtre principale
root = tk.Tk()
root.title("Visualisation des matchs")

# Créer un Treeview pour afficher la liste des matchs
treeview = ttk.Treeview(root, columns=("ID", "Équipe 1", "Équipe 2"), show="headings")
treeview.heading("ID", text="ID")
treeview.heading("Équipe 1", text="Équipe 1")
treeview.heading("Équipe 2", text="Équipe 2")

# Ajouter les matchs au Treeview
for match in matches:
    treeview.insert("", "end", values=match)

# Ajouter un événement de clic pour afficher les détails du match sélectionné
treeview.bind("<<TreeviewSelect>>", afficher_details_match)

# Créer une étiquette pour afficher les détails du match sélectionné
details_label = tk.Label(root, text="Sélectionnez un match pour afficher les détails.")

# Placer les widgets dans la fenêtre principale
treeview.pack(pady=10)
details_label.pack()

# Lancer la boucle principale de l'application
root.mainloop()