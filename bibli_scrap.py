from ebooklib import epub

def recuperer_EPUB(epub_path):
    livre = epub.read_epub(epub_path)

    date = livre.get_metadata('DC', 'date')[0][0] if livre.get_metadata('DC', 'date') else "N/A"

    # Obtenez le sujet
    sujet = livre.get_metadata('DC', 'description')[0][0] if livre.get_metadata('DC', 'description') else "N/A"

    # Obtenez le titre du livre
    titre = livre.get_metadata('DC', 'title')[0][0] if livre.get_metadata('DC', 'title') else "N/A"

    # Obtenez la langue du livre
    language = livre.get_metadata('DC', 'language')[0][0] if livre.get_metadata('DC', 'language') else "N/A"

    # Obtenez l'auteur du livre
    auteur = ", ".join(author[0] for author in livre.get_metadata('DC', 'creator')) if livre.get_metadata('DC', 'creator') else "N/A"

    return titre, auteur, language, sujet, date

# Exemple d'utilisation
epub_path = r'C:\Users\alexe\Downloads\abraham_leon-la_conception_materialiste_de_la_question_juive.epub'
title, author, langue, sujet, date = recuperer_EPUB(epub_path)

print("Titre:", title)
print("Auteur:", author)
print("langue:", langue)
print("sujet:", sujet)
print("date:", date)




