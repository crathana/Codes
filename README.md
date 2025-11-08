# Dépôt de mes scripts Python

Vous trouverez ici différents scripts que j’ai développés au fil du temps.  
J’ajouterai de nouveaux projets au fur et à mesure de leur création.  


## Liste des codes

### **`delaunay.py`**
Ce script crée une triangulation de Delaunay initiale en plaçant trois points aléatoires sur un plan.  
Vous pouvez ensuite cliquer sur le plan pour ajouter de nouveaux points, et la triangulation se mettra automatiquement à jour.


### **`secret_santa.py`** *(dans le dossier `secret_santa/`)*
Ce programme génère un **tirage au sort de Secret Santa** à partir d’un fichier CSV contenant les noms et adresses e-mail des participants.  
Il envoie ensuite automatiquement un e-mail personnalisé à chaque personne pour lui indiquer **qui elle doit gâter**.

#### Préparation

1. **Remplissez le fichier `adresses_mail.csv`**  
   Il doit contenir deux colonnes :  
   - `Nom` : le nom du participant  
   - `Adresse mail` : l’adresse e-mail correspondante  

2. **Créez un mot de passe d’application** pour votre adresse e-mail  
   - Cela se fait depuis les paramètres de votre fournisseur de messagerie (Gmail, Outlook, Orange, etc.)  
   - Vous trouverez facilement des tutoriels en ligne expliquant la marche à suivre.

3. **Créez un fichier `.env`** dans le même dossier que le script, contenant vos identifiants sous la forme suivante :

   ```env
   EMAIL="votre_adresse@mail.com"
   EMAIL_PASSWORD="votre_mot_de_passe_d_application"
   ```

*Assurez-vous de ne **jamais publier** votre fichier `.env` sur GitHub (grâce à votre `.gitignore`).*
