from base_livre import *


class Livre(base_livre):
    def __init__(self, ressource):
        self.ressource = ressource
        self.arg = {}  # dictionnaire

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
        return f"Livre :\n{self.arg}"

    def __eq__(self, other):
        if type(other).__name__ != type(self).__name__:
            return False
        return self.arg == other.arg
