from Bibliothèques.base_blibli import base_bibli
from Livres.Livre_EPUB import Livre_EPUB
from Livres.Livre_PDF import Livre_PDF
import os
import shutil
import fonctions.fonctions_fichier as f


class Simple_bibli(base_bibli):
    def __init__(self, path="Default"):
        self.path = path
        self.livres = []
        self.auteurs = []
        try:
            if not os.path.exists(path):
                # Crée le dossier si celui-ci n'existe pas
                print(f"Le dossier {path} n'existe pas.")
                print(f"Création du dossier {path}.")
                os.makedirs(path)
            # Liste des fichiers dans le répertoire
            fichiers = os.listdir(path)
            # ajoute les livres déjà présents dans le dossier
            for fichier in fichiers:
                extension = os.path.splitext(fichier)[1].lower()
                match extension:
                    case '.epub':
                        self.livres.append(Livre_EPUB(os.path.join(self.path, fichier)))
                        self.ajoute_auteur(Livre_EPUB(os.path.join(self.path, fichier)))
                    case '.pdf':
                        self.livres.append(Livre_PDF(os.path.join(self.path, fichier)))
                        self.ajoute_auteur(Livre_PDF(os.path.join(self.path, fichier)))
                    case _:
                        print("Extension " + extension + " pas prise en compte")
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")

    def ajouter(self, livre):
        try:
            # Vérifie si le livre est déjà présent
            if livre in self.livres:
                print(f"Le livre {livre.titre()} est déjà présent.")
                return True
            # Vérifie si le chemin existe
            if os.path.isfile(livre.ressource):
                # Si c'est un dossier local, copie le fichier dans le dossier
                shutil.copy(livre.ressource, self.path)
                print(f"Le livre {os.path.basename(livre.ressource)} a été ajouté au dossier.")
            else:
                print("Type de chemin non pris en charge.")
                return False

            # Ajoute le livre à la liste des livres et l'auteur à la liste des auteurs
            self.livres.append(livre)
            self.ajoute_auteur(livre)
            return True
        except FileNotFoundError:
            print(f"Le fichier {os.path.basename(livre.ressource)} n'a pas été trouvé.")
            return False
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")
            return False

    def __str__(self):
        return "\n".join(str(livre) for livre in self.livres)

    # ajoute un auteur à la liste des auteurs
    def ajoute_auteur(self, livre):
        if livre.auteur() not in self.auteurs:
            self.auteurs.append(livre.auteur())
            return True
        return False

    def rapport_livres(self, format, fichier='./rapport'):
        match format:
            case 'PDF':
                rapport = open("rapport_livres.txt", 'w')
                for livre in self.livres:
                    rapport.write(livre.__str__() + "\n")
                rapport.close()
            case 'EPUB':
                f.rapport_EPUB(fichier, self.path)
