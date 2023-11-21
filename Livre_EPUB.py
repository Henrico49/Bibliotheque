from Livre import *
from ebooklib import epub

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


class Livre_EPUB(Livre):
    def __init__(self, ressource):
        super().__init__(ressource)
        self.arg = recup_EPUB(ressource)

    def type(self):
        return "EPUB"