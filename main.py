import fonctions.fonctions_fichier as f
import sys
from Bibliothèques.simple_bibli import Simple_bibli
from Bibliothèques.bibli import bibli
from Bibliothèques.bibli_scrap import bibli_scrap

n = len(sys.argv)
try:
    match n:

        case 1:
            print("Veuillez indiquer les options à utiliser quelques exemples ci-dessous :")
            print("https://math.univ-angers.fr/~jaclin/biblio/livres/")
            print("rapports")
            print("-c config.conf")
            print("-c config.conf rapports")
            print("-c config.conf https://math.univ-angers.fr/~jaclin/biblio/livres/")
            print("-c config.conf https://math.univ-angers.fr/~jaclin/biblio/livres/ 10")
            exit(1)
        case 2:
            if sys.argv[1] == "-c":
                print("Veuillez indiquer un fichier de configuration.")
                exit(1)
            elif sys.argv[1] == "rapports":
                b1 = Simple_bibli()
                b1.rapport_livres("PDF")
                b1.rapport_livres("EPUB")
                b1.rapport_auteurs("PDF")
                b1.rapport_auteurs("EPUB")
            elif f.est_lien_web(sys.argv[1]):
                b1 = bibli()
                b1.alimenter(sys.argv[1])
            else:
                print(f"Option non pris en compte : {sys.argv[1]}")
                exit(1)
        case 3:
            if sys.argv[1] == "-c":
                if sys.argv[2].endswith(".conf"):
                    chemin_bibliotheque, chemin_etats, nb_max = f.config_defaut()
                    b1 = Simple_bibli(chemin_bibliotheque)
                else:
                    print("Veuillez indiquer un fichier de configuration après -c.")
                    exit(1)
            else:
                if f.est_lien_web(sys.argv[1]) and sys.argv[2].isdigit():
                    b1 = bibli_scrap()
                    b1.alimenter(sys.argv[1], int(sys.argv[2]))
        case 4:
            if sys.argv[1] == "-c":
                if sys.argv[2].endswith(".conf"):
                    chemin_bibliotheque, chemin_etats, nb_max = f.config_defaut()
                else:
                    print("Veuillez indiquer un fichier de configuration après -c.")
                    exit(1)
                if sys.argv[3] == "rapports":
                    b1 = Simple_bibli(chemin_bibliotheque)
                    b1.rapport_livres("PDF", chemin_etats)
                    b1.rapport_livres("EPUB", chemin_etats)
                    b1.rapport_auteurs("PDF", chemin_etats)
                    b1.rapport_auteurs("EPUB", chemin_etats)
                elif f.est_lien_web(sys.argv[3]):
                    b1 = bibli(chemin_bibliotheque)
                    b1.alimenter(sys.argv[3])
                else:
                    print("Combinaison d'option non pris en compte.")
                    exit(1)
            else:
                print("Combinaison d'option non pris en compte.")
                exit(1)
        case 5:
            if sys.argv[1] == "-c":
                if sys.argv[2].endswith(".conf"):
                    chemin_bibliotheque, chemin_etats, nb_max = f.config_defaut()
                else:
                    print("Veuillez indiquer un fichier de configuration après -c.")
                    exit(1)
                if f.est_lien_web(sys.argv[3]) and sys.argv[4].isdigit():
                    b1 = bibli_scrap(chemin_bibliotheque)
                    b1.scrap(sys.argv[3], int(sys.argv[4]))
                else:
                    print("Combinaison d'option non pris en compte.")
                    exit(1)
            else:
                print("Combinaison d'option non pris en compte.")
                exit(1)
except Exception as e:
    print(f"Une erreur s'est produite : {e}")
    exit(1)
print(b1)
