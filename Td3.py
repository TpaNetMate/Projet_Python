#Importation des librairies
import praw
import pandas as pd
import urllib.request
import xmltodict
import pickle
import datetime

#Importation des classes
from Document import Document
from Author import Author

#####
# Td3
#####

############################ Partie 1 #############################

#Connexion au reddit
reddit = praw.Reddit(client_id='KYd1KpbtKE0641XSBs8JZw', client_secret='3ZiJlII7ACTQur4rt5oU4CBjdveqCA', user_agent='mateo')


## Question 1.1 :

#Tous les champs de praw.Reddit
#print(dir(reddit))

#Accéder au subreddit du mot entre les ()
subreddit = reddit.subreddit('Coronavirus')

# Alimentez la liste docs
docs_reddit = []

# Récupérer le contenu textuel et l'ajouter à la liste 'docs'
for post in subreddit.hot(limit=100):
    text = post.title
    #text = post.selftext
    #text = text.replace("\n", " ")
    docs_reddit.append(text)

#print(docs_reddit)

##Question 1.2 :

#Tous les champs de xmltodict
#print(dir(xmltodict))

# Alimentez la liste docs
docs_arxiv = []

#Mot à rechercher entre ""
mot_recherche = "covid"

# URL de l'API Arxiv
url = 'http://export.arxiv.org/api/query?search_query=all:' + mot_recherche + '&start=0&max_results=100'

# Données récupérées sont dans un format binaire
url_read = urllib.request.urlopen(url).read()

# url_read doit donc être décodé
data =  url_read.decode()

dico = xmltodict.parse(data) #champ contenant le contenu textuel
docs = dico['feed']['entry']
for d in docs:
    text = d['title']+ ". " + d['summary']
    text = text.replace("\n", " ")
    docs_arxiv.append(text)

#print(docs_arxiv)


############################ Partie 2 #############################

## Question 2.1 :

# Concaténation et création des colonnes
corpus = docs_reddit + docs_arxiv
source = ['Reddit'] * len(docs_reddit) + ['Arxiv'] * len(docs_arxiv)
num_id = list(range(1, len(corpus) + 1))

# Création du DataFrame
data = {'ID': num_id,
        'text': corpus,
        'Origine_Site': source}

# Création du DataFrame à partir du dictionnaire 'data'
df = pd.DataFrame(data)
#print(df)

# Une facon de faire les question 2.1 et 2.2 avec pickle :
## Question 2.2 :   
#df.to_csv('fichier.csv', sep='\t', index=False)
## Question 2.3 :
#df = pd.read_csv('fichier.csv', sep='\t')
#print(df)


############################ Partie 3 #############################

## Question 3.1 :
taill_corp = len(corpus)
#print("Le nombre de documents du corpus est de " + str(taill_corp) + ".")

## Question 3.2 :
Affichage1 = True # Mettre True pour afficher le resultat de la fonction
if Affichage1:
    for i, doc in enumerate(corpus, start=1) :
        print("Document n°" + str(i))
        print("Nombre de mots :" + str(len(doc.split(" ")))) #Nombre de mots en comptant à chaque espace
        print("Nombre de phrases :" + str(len(doc.split("."))) + "\n") #Nombre de phrases en comptant à chaque point
    
## Question 3.3 :
corp_filtre = [doc for doc in corpus if len(doc) >= 100]

Affichage2 = True # Mettre True pour afficher le resultat de la fonction
if Affichage2:
    for i, doc in enumerate(corp_filtre, start=1) :
        print("Document n°" + str(i))
        print("Nombre de mots :" + str(len(doc.split(" ")))) #Nombre de mots en comptant à chaque espace
        print("Nombre de phrases :" + str(len(doc.split("."))) + "\n") #Nombre de phrases en comptant à chaque point

## Question 3.4 :
#Création d'une unique chaine de caractere contenant tous les docs
chaine_unique = " ".join(corp_filtre)

#Autre facon de faire les question 2.1 et 2.2 avec pickle :
## Question 2.2
with open("out.pkl", "wb") as f:
    pickle.dump(corp_filtre, f)

## Question 2.3  
with open("out.pkl", "rb") as f:
    corp_filtre = pickle.load(f)

# Mettre une date et une heure au moment de l'execution du code
aujourdhui = datetime.datetime.now()
#print(aujourdhui)


#####
# Td4
#####


collection = []

# Reddit

# Arxiv