############################ Partie 1 #############################
## Question 1.1 et 1.2:
import re
class Document:
    def __init__(self, titre, auteur, date, url, texte):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
   
    def __repr__(self):
        return f"\nTitre : {self.titre}\nAuteur : {self.auteur}\nDate : {self.date}\nURL : {self.url}\nTexte : {self.texte}\n"

    def __str__(self):
        return f"Titre : {self.titre}"
    def search(self,mot ):
        # Utiliser une expression régulière pour trouver le mot dans le texte
        pattern = re.compile(r'\b' + re.escape(mot) + r'\b', re.IGNORECASE)
        matches = re.finditer(pattern, self.texte)
        taille_contexte=10
        resultats = []
        # Parcourir les occurrences et récupérer les indices de début et de fin
        for match in matches:
            debut = match.start()
            fin = match.end()
            texte_doc=self.texte
            # Ajouter les informations à la liste des résultats
            contexte_gauche = self.texte[max(0, debut - taille_contexte):debut]
            contexte_droite = self.texte[fin:min(fin + taille_contexte, len(self.texte))]

            resultats.append({
                'mot_cible': mot,
                # 'debut': debut,
                # 'fin': fin,
                # 'occurrence': self.texte[debut:fin],
                'contexte_gauche': contexte_gauche,
                'contexte_droite': contexte_droite,
                'texte':texte_doc
            })

        return resultats

class RedditDocument(Document):
    def __init__(self, titre="", auteur="", date="", url="", texte="",commentaire=""):
        super().__init__(titre="", auteur="", date="", url="", texte="")
        self.commentaire=commentaire
    def __str__(self):
        parent=super().__str__()
        return f"{parent},{self.commentaire}"
    def getType(self):
        return "Docuemnt Reddit"
    
class ArxivDocument(Document):
    def __init__(self, titre="", auteur="", date="", url="", texte="",coauteurs=""):
        super().__init__(titre="", auteur="", date="", url="", texte="")
        self.coauteurs=coauteurs
    def __str__(self):
        parent=super().__str__()
        return f"{parent},{self.coauteurs}"
    def getType(self):
        return "Docuemnt Arxiv"