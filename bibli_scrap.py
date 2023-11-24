from bibli import bibli
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import shutil
from Livre_EPUB import Livre_EPUB
from Livre_PDF import Livre_PDF

def liens_pdf_epub(url):
    # Envoie une requête GET à l'URL spécifiée
    response = requests.get(url, verify=False)
    # Vérifie si la requête a réussi (code 200 OK)
    response.raise_for_status()

    # Analyse le contenu HTML de la page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Récupère tous les liens avec un attribut href
    liens = soup.find_all('a', href=True)
    liens_filtres = [urljoin(url, lien.get('href')) for lien in liens if
                      lien.get('href').lower().endswith(('.epub', '.pdf'))]
    return liens_filtres
def recup_liens(url):  #  récupère tous les liens sauf ceux pdf et epub
    # Envoie une requête GET à l'URL spécifiée
    response = requests.get(url, verify=False)
    # Vérifie si la requête a réussi (code 200 OK)
    response.raise_for_status()

    # Analyse le contenu HTML de la page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Récupère tous les liens avec un attribut href
    liens = soup.find_all('a', href=True)
    liens_filtres = [urljoin(url, lien.get('href')) for lien in liens if not
                     lien.get('href').lower().endswith(('.epub', '.pdf'))]
    return liens_filtres


class bibli_scrap(bibli):
    def __init__(self, path):
        self.livres = []
        super().__init__(path)
    def telecharger(self, lien):
        try:
            # Vérifie si le livre est déjà présent
            nom_fichier = os.path.basename(lien)
            if nom_fichier in self.livres:
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
                    if nom_fichier.lower().endswith('.epub'):
                        self.livres.append(Livre_EPUB(os.path.join(self.path, nom_fichier)))
                    elif nom_fichier.lower().endswith('.pdf'):
                        book = os.path.join(self.path, nom_fichier)
                        self.livres.append(Livre_PDF(book))
                    print(f"Le livre {nom_fichier} a été téléchargé et enregistré.")
                else:
                    print(f"Échec de la requête avec le code d'état : {response.status_code}")
        except Exception as e:
            print(f"Une erreur s'est produite lors du téléchargement du livre {lien} : {e}")


    def scrap(self, url, profondeur, nbmax):



















