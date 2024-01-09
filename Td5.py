#Importation des librairies
import praw
import pandas as pd
import urllib.request
import xmltodict
import pickle
import datetime
from Document import Document
from Document import RedditDocument
from Document import ArxivDocument
import Author
#Importation des classes
from Document import Document
from Author import Author

#####
# Td3
#####

############################ Partie 1 #############################

#Connexion au reddit
reddit = praw.Reddit(client_id='--T4GQlNeGiymsugkIuEUQ', client_secret='KKnRvqABUY89YtWbILtA5_v0tv341w', user_agent='td3')


## Question 1.1 :

#Tous les champs de praw.Reddit
#print(dir(reddit))

#Accéder au subreddit du mot entre les ()
subreddit = reddit.subreddit('Coronavirus')

# Alimentez la liste docs
docs_reddit = []
collection=[]
# Récupérer le contenu textuel et l'ajouter à la liste 'docs'
for post in subreddit.hot(limit=100):
    text = post.title
    #text = post.selftext
    #text = text.replace("\n", " ")
    docs_reddit.append(text)
    titre = post.title
    classAuteurTest=Author(str(post.author))
    date = datetime.datetime.fromtimestamp(post.created).strftime("%Y/%m/%d")
    url = "https://www.reddit.com/"+post.permalink
    texte = post.selftext.replace("\n", "")

    doc_classe = Document(titre, classAuteurTest, date, url, texte)

    collection.append(doc_classe)

# print(collection)


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
    titre = d["title"].replace('\n', '')  # On enlève les retours à la ligne
    try:
        authors = ", ".join([a["name"] for a in d["author"]])  # On fait une liste d'auteurs, séparés par une virgule
    except:
        authors = d["author"]["name"]  # Si l'auteur est seul, pas besoin de liste
        classAuteurTest=Author(authors)
    summary = d["summary"].replace("\n", "")  # On enlève les retours à la ligne
    date = datetime.datetime.strptime(d["published"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d")  # Formatage de la date en année/mois/jour avec librairie datetime

    coauteurs=len(authors)
    doc_classe = Document(titre, classAuteurTest, date, d["id"], summary)  # Création du Document
    collection.append(doc_classe)  # Ajout du Document à la liste.

#print(docs_arxiv)
    # =============== 2.6 : DICT AUTEURS ===============

authors = {}
aut2id = {}
num_auteurs_vus = 0

# Création de la liste+index des Auteurs
id2doc = {}
for i, doc in enumerate(collection):
    id2doc[i] = doc
    if doc.auteur not in aut2id:
        num_auteurs_vus += 1
        authors[num_auteurs_vus] = Author(doc.auteur)
        aut2id[doc.auteur] = num_auteurs_vus

    authors[aut2id[doc.auteur]].add(doc.texte)
# print(id2doc)
import re
# print(collection)




############################ Partie 2 #############################

## Question 2.1 :

# Concaténation et création des colonnes
# corpus = docs_reddit + docs_arxiv

from Corpus import Corpus
nomCorpus='mon corpus'
corpusClass = Corpus(nomCorpus)

# Construction du corpus à partir des documents
for doc in collection:
    corpusClass.add(doc)

source = ['Reddit'] * len(docs_reddit) + ['Arxiv'] * len(docs_arxiv)
num_id = list(range(1, corpusClass.ndoc + 1))

# Création du DataFrame
data = {'ID': num_id,
        'text': corpusClass,
        'Origine_Site': source}

# Création du DataFrame à partir du dictionnaire 'data'
df = pd.DataFrame(data)
#print(df)

# Une facon de faire les question 2.1 et 2.2 avec pickle :
## Question 2.2 :   
df.to_csv('corpus.csv', sep='\t', index=False)
## Question 2.3 :
df = pd.read_csv('corpus.csv',on_bad_lines='skip')
# print(df)

# print(corpus.show)

############################ Partie 3 #############################

# Question 3.1 :
corpus=collection
taill_corp = len(corpus)
print("Le nombre de documents du corpus est de " + str(taill_corp) + ".")

# Question 3.2 :
Affichage1 = True # Mettre True pour afficher le resultat de la fonction
if Affichage1:
    for i, doc in enumerate(corpus, start=1) :
        print("Document n°" + str(i))
        print("Nombre de mots :" + str(len(doc.texte.split(" ")))) #Nombre de mots en comptant à chaque espace
        print("Nombre de phrases :" + str(len(doc.texte.split("."))) + "\n") #Nombre de phrases en comptant à chaque point
    
## Question 3.3 :
corp_filtre = [doc for doc in corpus if len(doc.texte) >= 100]

Affichage2 = True # Mettre True pour afficher le resultat de la fonction
if Affichage2:
    for i, doc in enumerate(corp_filtre, start=1) :
        print("Document n°" + str(i))
        print("Nombre de mots :" + str(len(doc.texte.split(" ")))) #Nombre de mots en comptant à chaque espace
        print("Nombre de phrases :" + str(len(doc.texte.split("."))) + "\n") #Nombre de phrases en comptant à chaque point

# Question 3.4 :
# Création d'une unique chaine de caractere contenant tous les docs
# chaine_unique = " ".join(corp_filtre)

#supprimer les doublons dans le corpus 
textes_uniques=set()
corpus_sans_doublons=[]
for doc in corp_filtre:
    if doc.titre not in textes_uniques:
        textes_uniques.add(doc.titre)
        corpus_sans_doublons.append(doc)

#TD6 rechercher un mot dans le corpus
target_word =input("Entrez le mot que vous souhaitez rechercher : ")
for doc in corpus_sans_doublons:
    res=doc.search(target_word)
    if res :
        print(res)

#Autre facon de faire les question 2.1 et 2.2 avec pickle :
## Question 2.2
# with open("out.pkl", "wb") as f:
#     pickle.dump(corp_filtre, f)

# ## Question 2.3  
# with open("out.pkl", "rb") as f:
#     corp_filtre = pickle.load(f)

# Mettre une date et une heure au moment de l'execution du code
aujourdhui = datetime.datetime.now()
#print(aujourdhui)

