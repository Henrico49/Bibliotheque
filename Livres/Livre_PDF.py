from Livres.Livre import *
import fonctions.fonctions_fichier as f


class Livre_PDF(Livre):
    def __init__(self, ressource):
        super().__init__(ressource)
        self.arg = f.recup_PDF(self.ressource)

    def type(self):
        return "PDF"

    def __str__(self):
        return f"Livre PDF:\n{self.arg}"

