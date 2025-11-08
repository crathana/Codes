import smtplib
from email.mime.text import MIMEText
import csv
import os
import random
from dotenv import load_dotenv

load_dotenv()  # charge le fichier .env contenant l'email et le mot de passe application de la personne faisant tourner le code

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD")


def chargement_participants(csv_fourni):
    """ 
    Charge le CSV avec le nom des participants et leurs email dans un dictionnaire
    In: csv avec Colonne 1: nom_participant et Colonne 2: adresse_mail
    Out: dictionnaire: {numero_participant:[nom_participant, adresse_mail]}
    """

    participants = {}

    with open(csv_fourni, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)  # lit chaque ligne comme un dict {nom: ..., email: ...}
        i = 1
        for row in reader:
            participants[i] = [row["Nom"],row["Adresse mail"]]
            i+=1
    return participants

def attribution_participants(participants):
    """
    Réalise le tirage aléatoire des participants de telle sorte à ce que personne ne soit tiré plus d'une fois
    et que personne ne se tire soit même.
    In: dictionnaire: {numero_participant:[nom_participant, adresse_mail]}
    Out: dictionnaire: {numero_participant:[nom_participant, adresse_mail,tirage]}
    """
    nb_participants = max(participants)
    liste_tirages = []
    for participant in participants:
        tirage = random.randint(1,nb_participants)
        while tirage == participant or tirage in liste_tirages:
           tirage = random.randint(1,nb_participants)
        liste_tirages.append(tirage)
        participants[participant].append(tirage)
    return participants
    
def envoi_mail(participants, test=True):
    """
    Envoie pour chaque participant d'un mail contenant l'information de la personne tirée si test est True
    sinon, renvoie un apperçu du mail à envoyer pour valider
    In: dictionnaire : {numero_participant:[nom_participant, adresse_mail, tirage]}
        test: bool
    """
    for participant in participants:
        nom = participants[participant][0]
        mail = participants[participant][1]
        tirage = participants[participant][2]
        nom_tirage = participants[tirage][0]


        # Personnalisez le message ci-dessous selon vos besoins, au format html. 
        html = f"""
        <h1>Ho ho ho 🎅</h1>
        <p>Bonjour {nom},</p>
        <p>Pour le Secret Santa de la famille <b>Hergé</b> de l'année 2025, tu dois offrir un cadeau à <b>{nom_tirage}</b>.</p>
        <p>En te souhaitant de joyeuses fêtes,</p>
        <p>Le père Noël secret 🎅</p>

        <p>PS: ceci est un mail automatique, merci de ne pas répondre.</p>
        """

        msg = MIMEText(html, "html")
        msg["Subject"] = "Secret Santa — Qui tu dois gâter 🎄"
        msg["From"] = EMAIL
        msg["To"] = mail

        # Permet de tester pour voir à quoi ressemblent les mails
        if test and participant ==1:
            print("MAIL PRET (test)")
            print(f"A: {mail}")
            print(f"Sujet: {msg['Subject']}")
            print(html)
            print("=============================\n")
        
        # Si on met test à "False", les mails s'envoient
        if not test:
            #Test si jamais le .env n'est pas bien chargé 
            if not EMAIL or not PASSWORD:
                raise RuntimeError("EMAIL ou EMAIL_PASSWORD non définis dans l'environnement.")
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL, PASSWORD)
                smtp.send_message(msg)



if __name__ == "__main__":

    #On charge les participants
    liste_participants = chargement_participants("adresses_mail.csv")
    print(liste_participants)

    #On réalise les tirages aléatoires
    participants_tirage = attribution_participants(liste_participants)
    print(participants_tirage)

    #On teste la forme du mail
    envoi_mail(participants_tirage)

    #On envoie les mails (commenter la ligne du ci-dessus et décommenter la ligne en ci-dessous)
    #envoi_mail(participants_tirage, False)