import tkinter as tk
import mysql.connector

def afficher_details_match(event):
    # Récupérer l'index du match sélectionné
    selected_item = match_listbox.curselection()
    match_id = match_ids[selected_item[0]]

    # Établir la connexion à la base de données
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='super_bowl'
    )
    cursor = cnx.cursor()

    # Récupérer les détails du match à partir de la base de données
    query = "SELECT equipe1.nom_equipe, equipe2.nom_equipe, matchs.heur_debut, matchs.heur_fin, " \
            "cote.valeur, COUNT(DISTINCT cote.utilisateur_id), commentaire.commentaire, matchs.score " \
            "FROM matchs " \
            "INNER JOIN equipe AS equipe1 ON matchs.equipe1_id = equipe1.id_equipe " \
            "INNER JOIN equipe AS equipe2 ON matchs.equipe2_id = equipe2.id_equipe " \
            "LEFT JOIN cote ON matchs.id_match = cote.match_id " \
            "LEFT JOIN commentaire ON matchs.id_match = commentaire.match_id " \
            "WHERE matchs.id_match = %s " \
            "GROUP BY matchs.id_match"
    cursor.execute(query, (match_id,))
    result = cursor.fetchone()

    # Fermer le curseur et la connexion
    cursor.close()
    cnx.close()

    # Afficher les détails du match dans une nouvelle fenêtre
    if result:
        equipe1_nom = result[0]
        equipe2_nom = result[1]
        heure_debut = result[2]
        heure_fin = result[3]
        cote_valeur = result[4]
        nb_utilisateurs_parie = result[5]
        commentaire = result[6]
        score = result[7]

        details_window = tk.Toplevel(root)
        details_window.title("Détails du match")

        details_label = tk.Label(details_window, text=f"Équipe 1: {equipe1_nom}\n"
                                                       f"Équipe 2: {equipe2_nom}\n"
                                                       f"Heure de début: {heure_debut}\n"
                                                       f"Heure de fin: {heure_fin}\n"
                                                       f"Montant des cotes: {cote_valeur}\n"
                                                       f"Nombre d'utilisateurs ayant parié: {nb_utilisateurs_parie}\n"
                                                       f"Commentaire: {commentaire}\n"
                                                       f"Score: {score}")
        details_label.pack(padx=50, pady=50)
    else:
        # Aucun détail disponible pour le match sélectionné
        pass

# Établir la connexion à la base de données
cnx = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
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

# Créer un Listbox pour afficher les matchs
match_listbox = tk.Listbox(root, width=90)
match_listbox.pack(pady=40)

# Créer une liste pour stocker les identifiants des matchs
match_ids = []

# Ajouter les matchs au Listbox
for match in matches:
    match_id = match[0]
    equipe1_nom = match[1]
    equipe2_nom = match[2]
    match_listbox.insert(tk.END, f"Match ID: {match_id} - Équipe 1: {equipe1_nom} - Équipe 2: {equipe2_nom}")
    match_ids.append(match_id)

# Ajouter un événement de clic pour afficher les détails du match sélectionné
match_listbox.bind("<<ListboxSelect>>", afficher_details_match)

# Lancer la boucle principale de l'application
root.mainloop()