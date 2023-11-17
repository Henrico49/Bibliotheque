from Livre import *

class Livre_PDF(Livre):
    def __init__(self, ressource):
        super().__init__(ressource)
        self.arg = recup_pdf(ressource)

    def type(self):
        return "PDF"