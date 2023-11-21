from base_blibli import base_bibli
import os
import shutil

class Simple_bibli(base_bibli):
    def __init__(self, path):
        self.path = path
        self.livres = []
        try:
            # Liste des fichiers dans le répertoire
            fichiers = os.listdir(path)
            self.livres = fichiers
        except FileNotFoundError:
            print(f"Le dossier {path} n'a pas été trouvé.")
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")

    def est_dossier_local(self, chemin):
        return os.path.isdir(chemin)

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
            self.livres.append(os.path.basename(livre.ressource))
            return True
        except FileNotFoundError:
            print(f"Le fichier {os.path.basename(livre.ressource)} n'a pas été trouvé.")
            return False
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")
            return False

    def __str__(self):
        msg=""
        for i in self.livres:
            msg+=i+" "
        return msg

