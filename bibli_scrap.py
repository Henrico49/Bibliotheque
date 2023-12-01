from bibli import bibli
from fonctions_fichier import *


class bibli_scrap(bibli):
    def __init__(self, path="Default"):
        self.livres = []
        super().__init__(path)

    def _scrap(self, url, nbmax):
        liens_livres = recup_liens_livres(url)
        nblivres = 0  # compte le nombre de livres effectivement téléchargés
        for lien_livre in liens_livres:
            if self.telecharger(lien_livre):
                nblivres += 1
            if nblivres >= nbmax:
                break

    def scrap(self, url, profondeur, nbmax):
        if profondeur > 0 and nbmax > 0:
            nbinitial = len(self.livres)
            self._scrap(url, nbmax)
            liens_externes = recup_liens_externes(url)
            i = 0
            while len(self.livres) - nbinitial > nbmax and i < len(liens_externes):
                self.scrap(liens_externes[i], profondeur - 1, len(self.livres) - nbinitial)
                i += 1

        elif nbmax == 0:
            print("Nombre maximal de livres atteint.")
        else:
            print("Profondeur maximale atteinte.")


