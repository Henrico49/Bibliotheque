from Livre import *

class Livre_EPUB(Livre):
    def __init__(self, ressource):
        super().__init__(ressource)
        self.arg = recup_EPUB(ressource)

    def type(self):
        return "EPUB"