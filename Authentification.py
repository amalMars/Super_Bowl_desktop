import tkinter as tk
from tkinter import messagebox
import mysql.connector
from Accueil_com import acceuil_commentateur

def on_button_connect_click():
    root = tk.Tk()
    accueil = acceuil_commentateur(root)
    root.mainloop()

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
    query = "SELECT id_utilisateur, est_commentateur FROM utilisateur WHERE email = %s AND mot_passe = %s "
    cursor.execute(query, (email, mot_de_passe))
    result = cursor.fetchone()
    # Fermer le curseur et la connexion à la base de données
    cursor.close()
    cnx.close()

    if result:
        utilisateur_id = int(result[0])
        est_commentateur = int(result[1])

        if est_commentateur == 1:
            global root
            root.destroy()
            root1 = tk.Tk()
            Accueil_com = acceuil_commentateur(root1)
            Accueil_com.afficher(utilisateur_id)
            Accueil_com.afficher_matchs()
            root1.mainloop()
            # Créer une nouvelle fenêtre Toplevel
            #nouvelle_fenetre = tk.Toplevel(root)
            #nouvelle_fenetre.title("Accueil Commentateur")

            # Appeler la fonction pour afficher la première page



        else:
            messagebox.showerror("Erreur", "Vous n'êtes pas autorisé à accéder en tant que commentateur.")
    else:
        messagebox.showerror("Erreur", "Identifiant ou mot de passe incorrect.")

# Créer la fenêtre d'authentification
root = tk.Tk()
root.title("Authentification")

# Créer les widgets de saisie d'informations
email_label = tk.Label(root, text="Email:",width=50)
email_label.pack()
email_entry = tk.Entry(root,width=50)
email_entry.pack()

mot_de_passe_label = tk.Label(root, text="Mot de passe:",width=80)
mot_de_passe_label.pack()
mot_de_passe_entry = tk.Entry(root, show="*",width=50)
mot_de_passe_entry.pack()

# Créer le bouton de connexion
connexion_button = tk.Button(root, text="Se connecter", command=verifier_identifiant)
connexion_button.pack()

# Lancer la boucle principale de l'application
root.mainloop()
