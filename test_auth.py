import tkinter as tk
from tkinter import messagebox
import mysql.connector
import Accueil_com

def verifier_identifiant():
    email = email_entry.get()
    mot_de_passe = mot_de_passe_entry.get()

    # Établir la connexion à la base de données
    cnx = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='super_bowl'
    )
    cursor = cnx.cursor()

    # Vérifier les informations d'identification dans la base de données
    query = "SELECT id_utilisateur, est_commentateur FROM utilisateur WHERE email = %s AND mot_passe = %s"
    cursor.execute(query, (email, mot_de_passe))
    result = cursor.fetchone()

    # Fermer le curseur et la connexion à la base de données
    cursor.close()
    cnx.close()

    if result:
        utilisateur_id = result[0]
        est_commentateur = result[1]

        if est_commentateur==1:
            # Créer une nouvelle fenêtre pour la première page (Accueil_com.py)
            nouvelle_fenetre = tk.Toplevel(root)
            nouvelle_fenetre.Accueil_com
           # nouvelle_fenetre.title("Accueil Commentateur")

            # Afficher le contenu de la première page
            label = tk.Label(nouvelle_fenetre, text="Bienvenue dans l'accueil commentateur!")
            label.pack()
        else:
            messagebox.showerror("Erreur", "Vous n'êtes pas autorisé à accéder en tant que commentateur.")
    else:
        messagebox.showerror("Erreur", "Identifiant ou mot de passe incorrect.")

# Créer la fenêtre d'authentification
root = tk.Tk()
root.title("Authentification")

# Créer les widgets de saisie d'informations
email_label = tk.Label(root, text="Email:")
email_label.pack()
email_entry = tk.Entry(root)
email_entry.pack()

mot_de_passe_label = tk.Label(root, text="Mot de passe:")
mot_de_passe_label.pack()
mot_de_passe_entry = tk.Entry(root, show="*")
mot_de_passe_entry.pack()

# Créer le bouton de connexion
connexion_button = tk.Button(root, text="Se connecter", command=verifier_identifiant)
connexion_button.pack()

# Lancer la boucle principale de l'application
root.mainloop()