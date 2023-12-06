from ebooklib import epub
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message="In the future version we will turn default option ignore_ncx to True.")

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

def creer():
    book = epub.EpubBook()
    book.add_metadata('DC', 'description', 'This is description for my book')
    metadonnees = recup_EPUB("/Users/alexandresalgueiro/Documents/GitHub/Bibliotheque/tmp/bibli/livres/about_edmond_-_le_roi_des_montagnes.epub")
    # intro chapter
    c1 = epub.EpubHtml(title='Introduction',
                       file_name='intro.xhtml',
                       lang='en')
    contenu_c1 = f"<html><body><p>{metadonnees['titre']} : {metadonnees['auteur']}, {metadonnees['date']}, {metadonnees['langue']}</p></body></html>"
    c1.set_content(contenu_c1)
    # about chapter
    c2 = epub.EpubHtml(title='About this book',
                       file_name='about.xhtml')
    c2.set_content('<h1>About this book</h1><p>This is a book.</p>')

    book.add_item(c1)
    book.add_item(c2)
    style = 'body { font-family: Times, Times New Roman, serif; }'

    nav_css = epub.EpubItem(uid="style_nav",
                            file_name="style/nav.css",
                            media_type="text/css",
                            content=style)
    book.add_item(nav_css)
    book.toc = (epub.Link('intro.xhtml', 'Introduction', 'intro'),
                (
                    epub.Section('Languages'),
                    (c1, c2)
                )
                )
    book.spine = ['nav', c1, c2]
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    epub.write_epub('test.epub', book)

# Exemple d'utilisation
creer()
def creer_epub(titre, auteur, contenu, chemin_sortie):
    try:
        # Créer un objet EPUB
        livre = epub.EpubBook()

        # Ajouter les métadonnées (titre, auteur, etc.)
        livre.set_identifier('id123456')
        livre.set_title(titre)
        livre.set_language('fr')
        livre.add_author(auteur)

        # Créer une section
        section = epub.EpubHtml(title='Contenu', file_name='contenu.xhtml', lang='fr')
        section.content = contenu

        # Ajouter la section au livre
        livre.add_item(section)

        # Ajouter la table des matières
        livre.toc = [section]

        # Créer un fichier EPUB
        epub.write_epub(chemin_sortie, livre)
        print(f"Fichier EPUB créé avec succès : {chemin_sortie}")

    except Exception as e:
        print(f"Une erreur s'est produite lors de la création de l'EPUB : {e}")

# Exemple d'utilisation
titre_livre = "Mon Premier Livre"
auteur_livre = "John Doe"
contenu_livre = "<h1>Bienvenue dans mon livre !</h1><p>Ceci est le contenu de mon livre.</p>"
chemin_sortie_livre = "mon_premier_livre.epub"

#creer_epub(titre_livre, auteur_livre, contenu_livre, chemin_sortie_livre)



def lire_contenu_epub(chemin_fichier):
    try:
        # Ouvrir le fichier EPUB
        livre = epub.read_epub(chemin_fichier)

        # Parcourir les éléments du livre
        for i, item in enumerate(livre.items):
            # Vérifier si l'élément est de type Text
            if isinstance(item, epub.EpubItem):
                # Lire le contenu du texte
                contenu_texte = item.content
                print(f"Contenu du texte (partie {i + 1}):\n{contenu_texte}\n")

    except Exception as e:
        print(f"Une erreur s'est produite lors de la lecture de l'EPUB : {e}")

# Exemple d'utilisation
chemin_fichier_epub = "test.epub"
lire_contenu_epub(chemin_fichier_epub)




print(recup_EPUB("test.epub"))