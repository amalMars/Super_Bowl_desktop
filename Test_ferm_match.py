import tkinter as tk
import tkinter.messagebox as messagebox
import mysql.connector

def clore_match():
    # Vérifier si un match est sélectionné
    if not match_listbox.curselection():
        tk.messagebox.showerror("Erreur", "Veuillez sélectionner un match.")
        return

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

    # Vérifier si le match a déjà été clos
    query = "SELECT statut, heur_fin FROM matchs WHERE id_match = %s"
    cursor.execute(query, (match_id,))
    result = cursor.fetchone()

    if result:
        statut = result[0]
        heure_fin = result[1]

        if statut == "affecté":
            tk.messagebox.showinfo("Information", "Ce match a déjà été clos.")
        else:
            # Récupérer les détails du match
            query = "SELECT equipe1_id, equipe2_id, heur_debut FROM matchs WHERE id_match = %s"
            cursor.execute(query, (match_id,))
            match_details = cursor.fetchone()

            if match_details:
                equipe1_id = match_details[0]
                equipe2_id = match_details[1]
                heure_debut = match_details[2]

                # Vérifier si le match a dépassé l'heure de fin prévue
                if heure_fin > heure_debut:
                    # Match prolongé, mettre à jour l'heure de fin du match
                    query = "UPDATE matchs SET heur_fin = %s WHERE id_match = %s"
                    cursor.execute(query, (heure_fin, match_id))

                # Calculer le montant gagné ou perdu par chaque utilisateur en fonction de son pari
                query = "SELECT utilisateur_id, equipe_id, montant FROM mise WHERE match_id = %s"
                cursor.execute(query, (match_id,))
                mises = cursor.fetchall()

                for mise in mises:
                    utilisateur_id = mise[0]
                    equipe_id = mise[1]
                    montant = mise[2]

                    # Récupérer la valeur de la cote pour l'équipe sélectionnée par l'utilisateur
                    query = "SELECT valeur FROM cote WHERE match_id = %s AND equipe_id = %s"
                    cursor.execute(query, (match_id, equipe_id))
                    cote = cursor.fetchone()

                    if cote:
                        valeur_cote = cote[0]

                        if valeur_cote > 1:
                            # L'équipe est gagnante, calculer le montant gagné
                            montant_gagne = montant * valeur_cote

                            # Mettre à jour le montant gagné pour l'utilisateur
                            query = "UPDATE mise SET montant_gagner = %s WHERE utilisateur_id = %s AND match_id = %s"
                            cursor.execute(query, (montant_gagne, utilisateur_id, match_id))
                        else:
                            # L'équipe est perdante, définir le montant perdu pour l'utilisateur
                            montant_perdu = montant

                            # Mettre à jour le montant perdu pour l'utilisateur
                            query = "UPDATE mise SET montant_perdu = %s WHERE utilisateur_id = %s AND match_id = %s"
                            cursor.execute(query, (montant_perdu, utilisateur_id, match_id))

                # Marquer le match comme étant clos
                query = "UPDATE matchs SET statut = 'clos' WHERE id_match = %s"
                cursor.execute(query, (match_id,))

                # Confirmer les modifications dans la base de données
                cnx.commit()

                # Actualiser l'affichage des matchs
                afficher_matchs()

                tk.messagebox.showinfo("Confirmation", "Le match a été clos avec succès.")
            else:
                tk.messagebox.showerror("Erreur", "Impossible de trouver les détails du match.")

    # Fermer le curseur et la connexion
    cursor.close()
    cnx.close()

# Fonction pour afficher les matchs
def afficher_matchs():
    # Effacer le contenu actuel du Listbox
    match_listbox.delete(0, tk.END)

    # Établir la connexion à la base de données
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='super_bowl'
    )
    cursor = cnx.cursor()

    # Récupérer tous les matchs du jour à partir de la base de données
    query = "SELECT id_match, equipe1_id, equipe2_id FROM matchs WHERE statut != 'clos' AND CURDATE() = DATE(heur_debut)"
    cursor.execute(query)
    matches = cursor.fetchall()

    # Fermer le curseur et la connexion
    cursor.close()
    cnx.close()

    # Ajouter les matchs au Listbox et à la liste des identifiants
    for match in matches:
        match_id = match[0]
        equipe1_id = match[1]
        equipe2_id = match[2]

        # Récupérer les noms des équipes
        equipe1_nom = obtenir_nom_equipe(equipe1_id)
        equipe2_nom = obtenir_nom_equipe(equipe2_id)

        match_listbox.insert(tk.END, f"Match ID: {match_id} - Équipe 1: {equipe1_nom} - Équipe 2: {equipe2_nom}")
        match_ids.append(match_id)

# Fonction pour obtenir le nom d'une équipe à partir de son ID
def obtenir_nom_equipe(equipe_id):
    # Établir la connexion à la base de données
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='super_bowl'
    )
    cursor = cnx.cursor()

    # Récupérer le nom de l'équipe à partir de son ID
    query = "SELECT nom_equipe FROM equipe WHERE id_equipe = %s"
    cursor.execute(query, (equipe_id,))
    result = cursor.fetchone()

    # Fermer le curseur et la connexion
    cursor.close()
    cnx.close()

    if result:
        return result[0]
    else:
        return ""

# Créer la fenêtre principale
root = tk.Tk()
root.title("Visualisation des matchs")

# Créer un Listbox pour afficher les matchs
match_listbox = tk.Listbox(root, width=50)
match_listbox.pack(pady=10)

# Créer un bouton pour clore un match
clore_button = tk.Button(root, text="Clore le match", command=clore_match)
clore_button.pack(pady=10)

# Créer une liste pour stocker les identifiants des matchs
match_ids = []

# Afficher les matchs du jour
afficher_matchs()

# Lancer la boucle principale de l'application
root.mainloop()