import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import fitz
from langdetect import detect
import re
from ebooklib import epub
import warnings
import urllib3
import os
import shutil
import configparser
import sys

# pour rajouter un format de fichier, ajoutez l'extension au tuple:
extensions = ('.pdf', '.epub')

# pour ignorer les warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore", category=UserWarning,
                        message="In the future version we will turn default option ignore_ncx to True.")


# pour créer un livre avec un url
def telecharger(lien):
    try:
        # Envoie une requête GET pour récupérer le contenu du fichier
        response = requests.get(lien, stream=True, verify=False)

        # Vérifie si la requête a réussi (code 200 OK)
        if response.status_code == 200:
            # Récupère le nom du fichier depuis l'URL
            nom_fichier = os.path.basename(lien)
            repertoire_telechargements = os.getcwd() + "/telechargements"
            # Vérifie si le répertoire de téléchargement existe, sinon le crée
            if not os.path.exists(repertoire_telechargements):
                os.makedirs(repertoire_telechargements)
            # Enregistre le fichier dans le dossier local
            chemin_local = os.path.join(repertoire_telechargements, nom_fichier)
            with open(chemin_local, 'wb') as fichier_local:
                shutil.copyfileobj(response.raw, fichier_local)
            print(f"Le livre {nom_fichier} a été téléchargé et enregistré.")
            return chemin_local
        # Si la requête n'est pas réussie, une exception est levée
        raise Exception(f"Échec de la requête avec le code d'état : {response.status_code}")

    except Exception as e:
        print(f"Une erreur s'est produite lors du téléchargement du livre {lien} : {e}")


def recup_date_langue(pdf_path, numero_page):
    with fitz.open(pdf_path) as pdf_document:
        # Vérifier si le numéro de page est valide
        if 0 <= numero_page < pdf_document.page_count:
            # Récupérer la page spécifique
            page = pdf_document[numero_page]
            # Récupère le texte de la page
            texte_page = page.get_text()
            # Utilise une expression régulière pour trouver le premier nombre
            match = re.search(r'\b\d+\b', texte_page)
            # Vérifie si une correspondance a été trouvée
            if match:
                date = match.group()
            else:
                date = None
            try:
                # Récupère la langue du texte
                language = detect(texte_page)
            except Exception as e:
                print("Erreur lors de la détection de la langue :", str(e))
                return date, "pas de langue détectée"
            return date, language


# pour un nouveau format de fichier, ajoutez une fonction de récuperation adaptée:
def recup_pdf(pdf_path):
    with fitz.open(pdf_path) as pdf_document:
        # Récupère le sujet
        sujet = pdf_document.metadata.get("subject", None)
        # Récupère l'auteur
        auteur = pdf_document.metadata.get("author", None)
        # Récupère le titre
        titre = pdf_document.metadata.get("title", None)
        # Récupère la date et la langue
        date, language = recup_date_langue(pdf_path, 0)

        dict_resultat = {'titre': titre, 'auteur': auteur, 'date': date, 'sujet': sujet, 'langue': language}
        return dict_resultat


def recup_EPUB(epub_path):
    # Récupère le livre
    livre = epub.read_epub(epub_path)
    # Récupère la date
    date = livre.get_metadata('DC', 'date')[0][0] if livre.get_metadata('DC', 'date') else None

    # Récupère le sujet
    sujet = livre.get_metadata('DC', 'description')[0][0] if livre.get_metadata('DC', 'description') else None

    # Récupère le titre du livre
    titre = livre.get_metadata('DC', 'title')[0][0] if livre.get_metadata('DC', 'title') else None

    # Récupère la langue du livre
    language = livre.get_metadata('DC', 'language')[0][0] if livre.get_metadata('DC', 'language') else None

    # Récupère l'auteur du livre
    auteur = ", ".join(author[0] for author in livre.get_metadata('DC', 'creator')) if livre.get_metadata('DC',
                                                                                                          'creator') else None
    dict = {'titre': titre, 'auteur': auteur, 'date': date, 'sujet': sujet, 'langue': language}
    return dict


def recup_liens_livres(url):
    # Envoie une requête GET à l'URL spécifiée
    response = requests.get(url, verify=False)
    # Vérifie si la requête a réussi (code 200 OK)
    response.raise_for_status()

    # Analyse le contenu HTML de la page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Récupère tous les liens avec un attribut href qui se terminent par les extensions supportées
    liens = soup.find_all('a', href=True)
    liens_filtres = [urljoin(url, lien.get('href')) for lien in liens if
                     lien.get('href').lower().endswith(extensions)]
    return liens_filtres


# récupère tous les liens sauf ceux qui sont des documents
def recup_liens_externes(url):
    # Envoie une requête GET à l'URL spécifiée
    response = requests.get(url, verify=False)
    # Vérifie si la requête a réussi (code 200 OK)
    response.raise_for_status()

    # Analyse le contenu HTML de la page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Récupère tous les liens avec un attribut href
    liens = soup.find_all('a', href=True)
    # tous les liens "externes", qui ne sont pas des documents
    liens_filtres = [urljoin(url, lien.get('href')) for lien in liens if not
    lien.get('href').lower().endswith(extensions + ('.zip',)) and est_url_valide(urljoin(url, lien.get('href')))]
    return liens_filtres

# cette fonction permet de vérifier qu'une chaine de caractère est bien un lien web
def est_lien_web(chaine):
    try:
        result = urlparse(chaine)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


# cette fonction permet de verifier qu'un lien dirige bien vers une page web différente
# et pas seulement vers la même page paramétrée différement
def est_url_valide(url):
    # Vérifier si la chaîne est une URL valide
    try:
        parsed_url = urlparse(url)
        if parsed_url.scheme and parsed_url.netloc:
            # Vérifier s'il n'y a pas de paramètres dans la requête
            if not parsed_url.query:
                return True
    except ValueError:
        pass

    return False

# cette fonction permet de lire un fichier de configuration
def lire_config(chemin_fichier):
    config = configparser.ConfigParser()
    config.read(chemin_fichier)
    return config

# cette fonction permet de récupérer les paramètres de configuration
def config_defaut():
    config = lire_config(sys.argv[2])
    chemin_bibliotheque = config.get('Bibliotheque', 'bibliotheque')
    chemin_etats = config.get('Bibliotheque', 'etats')
    nb_max = config.getint('Bibliotheque', 'nbmax')
    print(f"Vous avez executer le programme avec le fichier de configuration : {sys.argv[2]}")
    print(f"Chemin de la bibliothèque : {chemin_bibliotheque}")
    print(f"Chemin des états : {chemin_etats}")
    print(f"Nombre maximum de livres : {nb_max}")
    return chemin_bibliotheque, chemin_etats, nb_max
