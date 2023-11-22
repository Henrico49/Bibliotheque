from Livre import *
import PyPDF2
from pypdf import PdfReader
from langdetect import detect
import re

def detect_language(text):
    try:
        language = detect(text)
        return language
    except Exception as e:
        print("Erreur lors de la détection de la langue :", str(e))
        return None

def extract_first_number(input_string):
    # Utilise une expression régulière pour trouver le premier nombre
    match = re.search(r'\b\d+\b', input_string)

    # Vérifie si une correspondance a été trouvée
    if match:
        return int(match.group())
    else:
        return None

#TODO: Changer cette méthode qui bug de fou
def recup_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)

        # Récupération des informations
        reader = PdfReader(pdf_path)
        sujet = reader.metadata["/Comments"] if reader.metadata["/Comments"] else None
        auteur = reader.metadata["/Author"] if reader.metadata["/Author"] else None
        titre = reader.metadata["/Title"] if reader.metadata["/Title"] else None
        page = pdf_reader.pages[0]
        texte = page.extract_text()
        lignes = texte.splitlines()
        date = extract_first_number(lignes[3])
        page = pdf_reader.pages[1]
        texte = page.extract_text()
        langue = detect_language(texte)

        dict = {'titre': titre, 'auteur': auteur, 'date': date, 'sujet': sujet, 'langue': langue}
        return dict

class Livre_PDF(Livre):
    def __init__(self, ressource):
        super().__init__(ressource)
        self.arg = recup_pdf(ressource)

    def type(self):
        return "PDF"