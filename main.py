from fonctions_fichier import *
from simple_bibli import Simple_bibli
from bibli import bibli
from bibli_scrap import bibli_scrap
from Livre_PDF import Livre_PDF
from Livre_EPUB import Livre_EPUB


try : 
    b1 = Simple_bibli("bibliothèque_simple")
    b2 = bibli("bibliothèque")
    b3 = bibli_scrap("bibliothèque_scrap")
    l1 = Livre_PDF("https://math.univ-angers.fr/~jaclin/biblio/livres/abbot_flatland.pdf")
    l2 = Livre_EPUB("https://math.univ-angers.fr/~jaclin/biblio/livres/about_edmond_-_germaine.epub")
    b1.ajouter(l1)
    b1.ajouter(l2)
    b2.alimenter("https://math.univ-angers.fr/~jaclin/biblio/livres/")
    b3.scrap("https://math.univ-angers.fr/~jaclin/biblio/livres/", 2, 3)
    print("Bibliothèque simple :")
    print(b1)
    print("Bibliothèque :")
    print(b2)
    print("Bibliothèque scrap :")
    print(b3)
except Exception as e:
    print(e)
    print("Erreur lors de l'execution du programme")




