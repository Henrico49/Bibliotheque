from ebooklib import epub
import requests
from bs4 import BeautifulSoup
import os


def scrap(url, nbmax):
    # Désactive la vérification du certificat SSL
    reponse = requests.get(url, verify=False)

    # Si la requête a foncionnée
    if reponse.ok:
        liens = []
        soup = BeautifulSoup(reponse.text, 'html.parser')
        trs = soup.findAll('tr')
        n = nbmax + 3 if nbmax + 3 < len(trs) else len(trs)

        # Récupération des liens
        for i in range(3, n):
            liens.append('https://math.univ-angers.fr/~jaclin/biblio/livres/' + trs[i].find('a')['href'])
        return liens
    else:
        raise Exception("La requête n'a pas aboutie")


# Fonction pour télécharger un fichier PDF/EPUB depuis un lien
def download(url, destination_folder):
    # Désactive la vérification du certificat SSL
    response = requests.get(url, verify=False)

    # On s'assure que le dossier de destination existe
    os.makedirs(destination_folder, exist_ok=True)

    # Extrait le nom du fichier du lien
    file_name = os.path.join(destination_folder, url.split("/")[-1])

    # Enregistre le fichier
    with open(file_name, 'wb') as pdf_file:
        pdf_file.write(response.content)

    return file_name


def scrap_and_download(url, nbmax, destination_folder):
    # Scrap les liens
    liens = scrap(url, nbmax)

    # Télécharge les fichiers liés
    for lien in liens:
        download(lien, destination_folder)


def recuperer_EPUB(epub_path):
    # Récupère le livre
    livre = epub.read_epub(epub_path)

    # Récupère la date
    date = livre.get_metadata('DC', 'date')[0][0] if livre.get_metadata('DC', 'date') else "N/A"

    # Récupère le sujet
    sujet = livre.get_metadata('DC', 'description')[0][0] if livre.get_metadata('DC', 'description') else "N/A"

    # Récupère le titre du livre
    titre = livre.get_metadata('DC', 'title')[0][0] if livre.get_metadata('DC', 'title') else "N/A"

    # Récupère la langue du livre
    language = livre.get_metadata('DC', 'language')[0][0] if livre.get_metadata('DC', 'language') else "N/A"

    # Récupère l'auteur du livre
    auteur = ", ".join(author[0] for author in livre.get_metadata('DC', 'creator')) if livre.get_metadata('DC',
                                                                                                          'creator') else "N/A"

    return titre, auteur, language, sujet, date


####### SECTION TEST ########
if __name__ == "__main__":
    epub_path = r'C:\Users\alexe\Downloads\abraham_leon-la_conception_materialiste_de_la_question_juive.epub'
    title, author, langue, sujet, date = recuperer_EPUB(epub_path)
    print("Titre:", title)
    print("Auteur:", author)
    print("langue:", langue)
    print("sujet:", sujet)
    print("date:", date)

    liens = scrap('https://math.univ-angers.fr/~jaclin/biblio/livres/', 10)
    print(liens)

    url = 'https://math.univ-angers.fr/~jaclin/biblio/livres/'
    nbmax = 10
    destination_folder = r'D:\COURS\M1\Bibliotheque\Livres'

    scrap_and_download(url, nbmax, destination_folder)


