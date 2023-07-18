import tkinter as tk
import tkinter.messagebox as messagebox
import mysql.connector

class acceuil_commentateur:
    def __init__(self, root):
        self.root = root
        self.root.title("Application du commentateur")
        self.create_widgets()
        # Établir la connexion à la base de données
        self.cnx = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='super_bowl'
        )
        self.cursor = self.cnx.cursor()


    def create_widgets(self):
        # Créer un bouton pour afficher les détails d'un match
        self.detail_button = tk.Button(self.root, text="Afficher les détails", command=self.afficher_detail_match)
        self.detail_button.pack(pady=10)

        # Créer un bouton pour clore un match
        self.clore_button = tk.Button(self.root, text="Clore le match", command=self.clore_match)
        self.clore_button.pack(pady=10)

        self.match_listbox = tk.Listbox(self.root, width=100)
        self.match_listbox.pack(pady=40)

        # Créer une liste pour stocker les identifiants des matchs
        self.match_ids = []


    def afficher_matchs(self):
        # Effacer le contenu actuel du Listbox
        self.match_listbox.delete(0, tk.END)

        # Récupérer tous les matchs du jour à partir de la base de données
        query = "SELECT id_match, equipe1_id, equipe2_id, heur_debut, heur_fin FROM matchs WHERE DATE(heur_debut) = CURDATE()"
        self.cursor.execute(query)
        matchs = self.cursor.fetchall()

        # Ajouter les matchs au Listbox et à la liste des identifiants
        for match in matchs:
            match_id = match[0]
            equipe1_id = match[1]
            equipe2_id = match[2]
            heure_debut = match[3]
            heure_fin = match[4]

            equipe1_nom = self.obtenir_nom_equipe(equipe1_id)
            equipe2_nom = self.obtenir_nom_equipe(equipe2_id)

            self.match_listbox.insert(tk.END, f"Match ID: {match_id} - Équipe 1: {equipe1_nom} - Équipe 2: {equipe2_nom} - Heure début: {heure_debut} - Heure fin: {heure_fin}")
            self.match_ids.append(match_id)

    def obtenir_nom_equipe(self,equipe_id):
        # Récupérer le nom de l'équipe à partir de son ID
        query = "SELECT nom_equipe FROM equipe WHERE id_equipe = %s"
        self.cursor.execute(query, (equipe_id,))
        result = self.cursor.fetchone()

        if result:
            return result[0]
        else:
            return ""

    def afficher_detail_match(self):
        # Vérifier si un match est sélectionné
        if not self.match_listbox.curselection():
            messagebox.showerror("Erreur", "Veuillez sélectionner un match.")
            return

        # Récupérer l'index du match sélectionné
        selected_item = self.match_listbox.curselection()
        match_id = self.match_ids[selected_item[0]]
        print (match_id)

        # Récupérer les détails du match
        query = "SELECT equipe1_id, equipe2_id, heur_debut, heur_fin, score FROM matchs WHERE id_match = %s"
        self.cursor.execute(query, (match_id,))
        match_details = self.cursor.fetchone()

        if match_details:
            equipe1_id = match_details[0]
            equipe2_id = match_details[1]
            heure_debut = match_details[2]
            heure_fin = match_details[3]
            score = match_details[4]

            equipe1_nom = self.obtenir_nom_equipe(equipe1_id)
            equipe2_nom = self.obtenir_nom_equipe(equipe2_id)

            messagebox.showinfo("Détail du match", f"Équipe 1: {equipe1_nom}\nÉquipe 2: {equipe2_nom}\nHeure début: {heure_debut}\nHeure fin: {heure_fin}\nScore: {score}")
        else:
            messagebox.showerror("Erreur", "Impossible de trouver les détails du match.")

    def clore_match(self):
        # Vérifier si un match est sélectionné
        if not self.match_listbox.curselection():
            messagebox.showerror("Erreur", "Veuillez sélectionner un match.")
            return

        # Récupérer l'index du match sélectionné
        selected_item = self.match_listbox.curselection()
        match_id = self.match_ids[selected_item[0]]

        # Récupérer les détails du match
        query = "SELECT equipe1_id, equipe2_id, heur_debut, heur_fin FROM matchs WHERE id_match = %s"
        self.cursor.execute(query, (match_id,))
        match_details = self.cursor.fetchone()

        if match_details:
            equipe1_id = match_details[0]
            equipe2_id = match_details[1]
            heure_debut = match_details[2]
            heure_fin = match_details[3]

            # Vérifier si le match a dépassé l'heure de fin prévue
            if heure_fin > heure_debut:
                # Match prolongé, mettre à jour l'heure de fin du match
                query = "UPDATE matchs SET heur_fin = %s WHERE id_match = %s"
                self.cursor.execute(query, (heure_fin, match_id))

            # Calculer le montant gagné ou perdu par chaque utilisateur en fonction de son pari
            query = "SELECT utilisateur_id, equipe_id, montant FROM mise WHERE match_id = %s"
            self.cursor.execute(query, (match_id,))
            mises = self.cursor.fetchall()

            for mise in mises:
                utilisateur_id = mise[0]
                equipe_id = mise[1]
                montant = mise[2]

                # Récupérer la valeur de la cote pour l'équipe sélectionnée par l'utilisateur
                query = "SELECT valeur FROM cote WHERE match_id = %s AND equipe_id = %s"
                self.cursor.execute(query, (match_id, equipe_id))
                cote = self.cursor.fetchone()

                if cote:
                    valeur_cote = cote[0]

                    if valeur_cote > 1:
                        # L'équipe est gagnante, calculer le montant gagné
                        montant_gagne = montant * valeur_cote

                        # Mettre à jour le montant gagné pour l'utilisateur
                        query = "UPDATE mise SET montant_gagner = %s WHERE utilisateur_id = %s AND match_id = %s"
                        self.cursor.execute(query, (montant_gagne, utilisateur_id, match_id))
                    else:
                        # L'équipe est perdante, définir le montant perdu pour l'utilisateur
                        montant_perdu = montant

                        # Mettre à jour le montant perdu pour l'utilisateur
                        query = "UPDATE mise SET montant_perdu = %s WHERE utilisateur_id = %s AND match_id = %s"
                        self.cursor.execute(query, (montant_perdu, utilisateur_id, match_id))

            # Marquer le match comme étant clos
            query = "UPDATE matchs SET statut = 'clos' WHERE id_match = %s"
            self.cursor.execute(query, (match_id,))

            # Confirmer les modifications dans la base de données
            self.cnx.commit()

            messagebox.showinfo("Confirmation", "Le match a été clos avec succès.")
        else:
            messagebox.showerror("Erreur", "Impossible de trouver les détails du match.")



    def afficher(self,id):
        # Code pour afficher la première page de l'application pour le commentateur
        print("Affichage de la première page pour l'utilisateur", id)

    # Fermer le curseur et la connexion à la base de données
    #cursor.close()
    #cnx.close()

if __name__ == "main":
        root = tk.Tk()
        accueil = acceuil_commentateur(root)
        root.mainloop()