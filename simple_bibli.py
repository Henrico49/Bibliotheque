from base_blibli import base_bibli
import os
import shutil
from Livre_EPUB import Livre_EPUB
from Livre_PDF import Livre_PDF

class Simple_bibli(base_bibli):
    def __init__(self, path):
        self.path = path
        try:
            if not os.path.exists(path):
                # Crée le dossier si celui-ci n'existe pas
                self.livres = []
                os.makedirs(path)
            # Liste des fichiers dans le répertoire
            fichiers = os.listdir(path)
            for fichier in fichiers:
                print(fichier)
                if fichier.lower().endswith('.epub'):
                    self.livres.append(Livre_EPUB(os.path.join(self.path,fichier)))
                elif fichier.lower().endswith('.pdf'):
                    book = os.path.join(self.path,fichier)
                    self.livres.append(Livre_PDF(book))

        except Exception as e:
            print(f"Une erreur s'est produite : {e}")

    def ajouter(self, livre):
        try:
            # Vérifie si le livre est déjà présent
            if os.path.basename(livre.ressource) in self.livres:
                print(f"Le livre {os.path.basename(livre.ressource)} est déjà présent.")
                return False
            # Vérifie si le chemin existe
            if os.path.isdir(livre.ressource):
                # Si c'est un dossier local, copie le fichier dans le dossier
                shutil.copy(livre.ressource, self.path)
                print(f"Le livre {os.path.basename(livre.ressource)} a été ajouté au dossier.")
            else:
                print("Type de chemin non pris en charge.")
                return False

            # Ajoute le livre à la liste des livres
            self.livres.append(livre)
            return True
        except FileNotFoundError:
            print(f"Le fichier {os.path.basename(livre.ressource)} n'a pas été trouvé.")
            return False
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")
            return False

    def __str__(self):
        return ", ".join(str(livre) for livre in self.livres)
