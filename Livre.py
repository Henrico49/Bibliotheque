from base_livre import *
import json


class Livre(base_livre):
    def __init__(self,ressource):
        self.ressource = ressource
        self.arg = {} #dictionnaire

    def titre(self):
        return self.arg["titre"]

    def auteur(self):
        return self.arg["auteur"]

    def langue(self):
        return self.arg["langue"]

    def sujet(self):
        return self.arg["sujet"]

    def date(self):
        return self.arg["date"]

    def __str__(self):
        # Convertir le dictionnaire en chaîne de caractères JSON
        donnees_str = json.dumps(self.arg, indent=2)
        return f"Livre :\n{donnees_str}"