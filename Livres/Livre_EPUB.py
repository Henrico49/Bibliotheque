from Livre import *
from fonctions_fichier import *


class Livre_EPUB(Livre):
    def __init__(self, ressource):
        super().__init__(ressource)
        self.arg = recup_EPUB(self.ressource)

    def type(self):
        return "EPUB"

    def __str__(self):
        return f"Livre EPUB:\n{self.arg}"
