from Livre import *
import fitz  # PyMuPDF
from langdetect import detect
import re


def recup_date_langue(pdf_path, numero_page):
    with fitz.open(pdf_path) as pdf_document:
        # Vérifier si le numéro de page est valide
        if 0 <= numero_page < pdf_document.page_count:
            # Récupérer la page spécifique
            page = pdf_document[numero_page]

            # Afficher le texte de la page
            texte_page = page.get_text()
            # Utilise une expression régulière pour trouver le premier nombre
            match = re.search(r'\b\d+\b', texte_page)

            # Vérifie si une correspondance a été trouvée
            if match:
                date = match.group()
            else:
                date = None
            try:
                language = detect(texte_page)
            except Exception as e:
                print("Erreur lors de la détection de la langue :", str(e))
                return None
            return date, language


def recup_pdf(pdf_path):
    with fitz.open(pdf_path) as pdf_document:
        sujet = pdf_document.metadata.get("subject", None)
        auteur = pdf_document.metadata.get("author", None)
        titre = pdf_document.metadata.get("title", None)
        date, language = recup_date_langue(pdf_path, 0)
        dict_resultat = {'titre': titre, 'auteur': auteur, 'date': date, 'sujet': sujet, 'langue': language}
        return dict_resultat


class Livre_PDF(Livre):
    def __init__(self, ressource):
        super().__init__(ressource)
        self.arg = recup_pdf(ressource)

    def type(self):
        return "PDF"

    def __str__(self):
        return f"Livre PDF:\n{self.arg}"
