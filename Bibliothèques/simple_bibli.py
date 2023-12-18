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

    # retourne la liste des auteurs et leurs livres de la bibliothèque
    def auteur_livres(self):
        auteurs = self.auteurs
        livres = self.livres
        auteurs_et_livres = {}

        for auteur in auteurs:
            auteurs_et_livres[auteur] = []

        for livre in livres:
            auteur = livre.auteur()
            # Ajoutez le livre à la liste des livres de l'auteur
            auteurs_et_livres[auteur].append(livre)
        return auteurs_et_livres

    # créer le contenu du rapport au format EPUB qui liste les auteurs et leurs livres de la bibliothèque
    def contenu_epub_auteur(self):
        liste_auteurs = self.auteur_livres()
        contenu = "<h1>Liste des auteurs et de leurs livres :</h1>"
        contenu += "<table>"
        contenu += "<tr><th>Auteur</th><th>Titres</th><th>Dates</th><th>Sujets</th><th>Langues</th></tr>"
        for auteur in liste_auteurs:
            contenu += f"<tr><td>{auteur}</td>"
            liste_titre = []
            liste_date = []
            liste_sujet = []
            liste_langue = []
            for livre in liste_auteurs[auteur]:
                motif = livre.type()
                match motif:
                    case "PDF":
                        metadonnees = f.recup_PDF(livre.ressource)
                    case "EPUB":
                        metadonnees = f.recup_EPUB(livre.ressource)
                    case _:
                        raise Exception("Type de livre non pris en compte")
                liste_date.append(metadonnees['date'])
                liste_titre.append(metadonnees['titre'])
                liste_sujet.append(metadonnees['sujet'])
                liste_langue.append(metadonnees['langue'])
            contenu += f"<td><ul>"
            for titre in liste_titre:
                contenu += f"<li>{titre}</li>"
            contenu += f"</ul></td>"
            contenu += f"<td><ul>"
            for date in liste_date:
                contenu += f"<li>{date}</li>"
            contenu += f"</ul></td>"
            contenu += f"<td><ul>"
            for sujet in liste_sujet:
                contenu += f"<li>{sujet}</li>"
            contenu += f"</ul></td>"
            contenu += f"<td><ul>"
            for langue in liste_langue:
                contenu += f"<li>{langue}</li>"
            contenu += f"</ul></td></tr>"
        contenu += "</table>"
        return contenu

    # créer un rapport au format PDF ou EPUB qui liste les livres de la bibliothèque
    def rapport_livres(self, format, fichier='./rapport'):
        match format:
            case 'PDF':
                contenu = " "
                for file in os.listdir(self.path):
                    if file.endswith('.epub'):
                        metadonne = f.recup_EPUB(self.path + '/' + file)
                        contenu += f"Titre: {metadonne['titre']}\nAuteur: {metadonne['auteur']}\nDate: {metadonne['date']}\nSujet: {metadonne['sujet']}\nLangue: {metadonne['langue']}\n\n"
                    elif file.endswith('.pdf'):
                        metadonne = f.recup_PDF(self.path + '/' + file)
                        contenu += f"Titre: {metadonne['titre']}\nAuteur: {metadonne['auteur']}\nDate: {metadonne['date']}\nSujet: {metadonne['sujet']}\nLangue: {metadonne['langue']}\n\n"
                f.rapport_PDF(fichier, contenu, "livre")
            case 'EPUB':
                contenu = "<h1>Liste des livres :</h1>"
                contenu += '<table>'
                contenu += '<tr><th>Type</th><th>Auteur</th><th>titre</th><th>date</th><th>sujet</th><th>langue</th></tr>'
                for livre in self.livres:
                    if type(livre).__name__ == "Livre_PDF":
                        metadonnees = f.recup_PDF(livre.ressource)
                    elif type(livre).__name__ == "Livre_EPUB":
                        metadonnees = f.recup_EPUB(livre.ressource)
                    contenu += f"<tr><td>{livre.type()}</td><td>{livre.auteur()}</td><td>{livre.titre()}</td><td>{metadonnees['date']}</td><td>{metadonnees['sujet']}</td><td>{metadonnees['langue']}</td></tr>"
                contenu += '</table>'
                f.rapport_EPUB(fichier, contenu, "livre")
            case _:
                raise Exception("Format non pris en compte")

    # créer un rapport au format PDF ou EPUB qui liste les auteurs et leurs livres de la bibliothèque
    def rapport_auteurs(self, format, fichier="./rapport"):
        match format:
            case 'PDF':
                auteurs_et_livres = self.auteur_livres()
                contenu = ""
                for auteur in auteurs_et_livres:
                    contenu += f"{auteur} :\n"
                    for livre in auteurs_et_livres[auteur]:
                        if type(livre).__name__ == "Livre_PDF":
                            metadonnees = f.recup_PDF(livre.ressource)
                        elif type(livre).__name__ == "Livre_EPUB":
                            metadonnees = f.recup_EPUB(livre.ressource)
                        contenu += f"\t\t\tTitre: {metadonnees['titre']}\n\t\t\tDate: {metadonnees['date']}\n\t\t\tSujet: {metadonnees['sujet']}\n\t\t\tLangue: {metadonnees['langue']}\n\n"
                    contenu += "\n"
                f.rapport_PDF(fichier, contenu, "auteur")
            case 'EPUB':
                contenu = self.contenu_epub_auteur()
                f.rapport_EPUB(fichier, contenu, "auteur")
            case _:
                raise Exception("Format non pris en compte")
