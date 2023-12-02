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

    def scrap(self, url, profondeur, nbmax=10):
        if profondeur >= 0 and nbmax > 0:
            nbinitial = len(self.livres)
            self._scrap(url, nbmax)
            if profondeur >= 1:  # si la profondeur est supérieure à 1 on regarde les liens vers d'autres sites
                liens_externes = recup_liens_externes(url)
                i = 0
                while len(self.livres) - nbinitial <= nbmax and i < len(liens_externes):
                    try:
                        # on appelle récursivement la fonction scrap avec profondeur -1
                        #et le nbmax - le nombre de livres téléchargés avant l'appel
                        self.scrap(liens_externes[i], profondeur - 1, nbmax - (len(self.livres) - nbinitial))
                        i += 1
                    except Exception as e:
                        i += 1
                        print(e)

        elif nbmax == 0:
            print("Nombre maximal de livre téléchargés.")
        elif nbmax < 0:
            raise ValueError("Le nombre maximal de livres doit être un entier positif.")
        elif profondeur < 0:
            raise ValueError("La profondeur doit être un entier positif.")
