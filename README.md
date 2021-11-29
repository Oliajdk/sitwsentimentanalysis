# sitwsentimentanalysis
miniprojet
Miniprojet en Python, sentiment analysis

Dossier templates contient les pages html qui seront retournés à l'utilisateur.
Dossier fichiers contient les txt qui servent pour le traitement (liste stopwords, mots positifs négatifs ...)

zemmour.html et zemmmournegation.html sont les pages générés sur le dataset de tweets après application de l'algo, car l'option n'est pas exécutable hors local
(herokuapp limite la durée d'une requète à 30secs alors que le traitement peut prendre plusieurs minutes, + de 120k tweets..)
app.py sert à lancer le serveur FLASK.
sentiment.py contient les méthodes pour le traitement.
Procfile et requirements.txt sont spécifiques pour la mise en service de l'application sur herokuapp
a_file.txt est le résultat de scrapping de "Zemmour since:2021-11-20 lang:fr" jusqu'au 27 novembre inclus.
