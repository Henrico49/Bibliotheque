from Livre import *
import fonctions.fonctions_fichier as f


class Livre_EPUB(Livre):
    def __init__(self, ressource):
        super().__init__(ressource)
        self.arg = f.recup_EPUB(self.ressource)

    def type(self):
        return "EPUB"

    def __str__(self):
        return f"Livre EPUB:\n{self.arg}"
