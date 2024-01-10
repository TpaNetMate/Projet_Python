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

#######TD6 Partie 2####

#TD6 rechercher un mot dans le corpus

###Et TD7 avec l'interface de recherche

import tkinter as tk
from functools import partial
from tkinter import ttk

#initialisation des varibales pour faire un data frame qui comporte le résultat de la recherche avec contexte gauche et contexte droite
contexte_gauche=[]
contexte_droite=[]
mots=[]
def on_search_button_click(query_var):
    query = query_var.get()
#parcourir le corpus sans doublons pour trouver le mot
    for doc in corpus_sans_doublons:
        res=doc.search(query)
        if res :
            print(res)
            for i in res:
                contexte_gauche.append(i['contexte_gauche'])
                mots.append(i['mot_cible'])
                contexte_droite.append(i['contexte_droite'])
#creation du dictionnaire avec le mot trouvé et le contexte gauche et droit
    concorde={
        'contexte gauche':contexte_gauche,
        'mot cible': mots,
        'contexte_droite':contexte_droite
    }
    print(type(concorde))
    # Création du DataFrame à partir du dictionnaire 'concorde'
    df_concorde = pd.DataFrame(concorde)
    df_concorde.to_csv('concorde.csv', sep='\t', index=False)
    df_concorde = pd.read_csv('concorde.csv',on_bad_lines='skip')
    print(df_concorde)
    result_df=df_concorde
    #creation de l'interface lorsque on clic sur 'recherche'
    result_window = tk.Toplevel(root)
    result_window.title("Résultats de la Recherche")

    # Création d'un tableau Pandas dans la nouvelle fenêtre
    treeview = ttk.Treeview(result_window, columns=list(result_df.columns), show="headings")
    for col in result_df.columns:
        treeview.heading(col, text=col)
    for i, row in result_df.iterrows():
        treeview.insert("", "end", values=list(row))

    treeview.pack(padx=10, pady=10, fill="both", expand=True)

# Création de la fenêtre principale
root = tk.Tk()
root.title("Navigateur de Recherche")
# Définir la taille initiale de la fenêtre sur 600x400 pixels
root.geometry('600x400')
# Création de la variable de texte pour le champ de saisie
query_var = tk.StringVar()

# Création des widgets de la page d'accueil
ttk.Label(root, text="Navigateur de Recherche").pack(pady=10)
entry = ttk.Entry(root, textvariable=query_var, width=10)
entry.pack(pady=10)
search_button = ttk.Button(root, text="Rechercher", command=lambda: on_search_button_click(query_var))
search_button.pack(pady=10)
# Ajoutez d'autres widgets selon vos besoins

root.mainloop()

### TD6 nettoyage #####
import string
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
from nltk.stem.snowball import SnowballStemmer
# turn a doc into clean tokens
def clean_doc(doc):
        # split into tokens by white space
        tokens = doc.split() #tokens=word_tokenize(doc)
        #Best way to strip punctuation from a string: prepare regex for char filtering by using regular expressions to search for and to remove punctuation 
        re_punc = re.compile('[%s]' % re.escape(string.punctuation))
        # remove punctuation from each word
        tokens = [re_punc.sub('', w) for w in tokens]
        # remove remaining tokens that are not alphabetic
        tokens = [word for word in tokens if word.isalpha()]
        # filter out stop words
        stop_words = set(stopwords.words('english'))
        tokens = [w for w in tokens if not w in stop_words]
        # filter out short tokens
        tokens = [word for word in tokens if len(word) > 1]
        # apply stemming using snowball
        stemmed = [SnowballStemmer('english').stem(word) for word in tokens]
        # gather each token to form a sentence
        cleaned_doc = ' '.join(word for word in stemmed)
        return cleaned_doc
clean_corpus=[]
for doc in corpus_sans_doublons:
    clean_corpus.append(clean_doc(doc.texte))

print(clean_corpus)

