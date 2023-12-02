from Livre import *
from fonctions_fichier import *


class Livre_PDF(Livre):
    def __init__(self, ressource):
        super().__init__(ressource)
        self.arg = recup_pdf(self.ressource)

    def type(self):
        return "PDF"

    def __str__(self):
        return f"Livre PDF:\n{self.arg}"

