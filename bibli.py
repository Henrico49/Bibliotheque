from simple_bibli import Simple_bibli
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import shutil
from Livre_EPUB import Livre_EPUB
from Livre_PDF import Livre_PDF


class bibli(Simple_bibli):
    def __init__(self, path="Default"):
        self.livres = []
        super().__init__(path)

    def telecharger(self, lien):
            try:
                # Vérifie si le livre est déjà présent
                nom_fichier = os.path.basename(lien)
                if nom_fichier in self.livres:  # attention
                    print(f"Le livre {nom_fichier} est déjà présent.")
                else:
                    # Envoie une requête GET pour récupérer le contenu du fichier
                    response = requests.get(lien, stream=True, verify=False)

                    # Vérifie si la requête a réussi (code 200 OK)
                    if response.status_code == 200:
                        # Récupère le nom du fichier depuis l'URL
                        nom_fichier = os.path.basename(lien)
                        # Enregistre le fichier dans le dossier local
                        chemin_local = os.path.join(self.path, nom_fichier)
                        with open(chemin_local, 'wb') as fichier_local:
                            shutil.copyfileobj(response.raw, fichier_local)
                        extension = os.path.splitext(nom_fichier)[1].lower()
                        match extension:
                            case '.epub':
                                livre = Livre_EPUB(os.path.join(self.path, nom_fichier))
                                self.livres.append(livre)
                                self.ajoute_auteur(livre)
                            case '.pdf':
                                livre = Livre_PDF(os.path.join(self.path, nom_fichier))
                                self.livres.append(livre)
                                self.ajoute_auteur(livre)
                            case _:
                                raise Exception("Extension pas prise en compte")
                        print(f"Le livre {nom_fichier} a été téléchargé et enregistré.")
                        return True
                    else:
                        print(f"Échec de la requête avec le code d'état : {response.status_code}")
                        return False

            except Exception as e:
                print(f"Une erreur s'est produite lors du téléchargement du livre {lien} : {e}")

    def alimenter(self, url, nbmax=10):
        try:
            # Envoie une requête GET à l'URL spécifiée
            response = requests.get(url, verify=False)
            # Vérifie si la requête a réussi (code 200 OK)
            response.raise_for_status()

            # Analyse le contenu HTML de la page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Récupère tous les liens avec un attribut href
            liens = soup.find_all('a', href=True)

            # Filtrer les liens se terminant par ".epub" ou ".pdf"
            liens_epub_pdf = [urljoin(url, lien['href']) for lien in liens if
                              lien['href'].lower().endswith(('.epub', '.pdf'))]

            for lien in liens_epub_pdf:
                if len(self.livres) >= nbmax:
                    break
                self.telecharger(lien)

            return liens_epub_pdf

        except requests.exceptions.RequestException as req_err:
            print(f"Erreur de requête : {req_err}")
            return None
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")
            return None
