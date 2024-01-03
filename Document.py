############################ Partie 1 #############################
## Question 1.1 et 1.2:
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