# Projet Bibliothèque

*Alexandre et Noé*

## Objectifs

L’objectif est de concevoir une application pour constituer et suivre une bibliothèque de livres. L’idée est de pouvoir
collecter des livres sur le web (web scraping) pour constituer une bibliothèque, et générer divers catalogues de cette
bibliothèque. On s’intéresse ici aux livres au format EPUB et PDF. Mais l’application doit être extensible de façon à
pouvoir facilement ajouter d’autres formats.

## Fonctionnalités

* Créer un livre à partir d'un fichier (PDF ou EPUB), en accédant aux métadonnées des fichiers.
* Créer une bibliothèque à partir d'un dossier.
* Créer une bibliothèque à partir d'un site internet (web scrapping).
* Possibilité d'ajouter un nouveau format de livre simplement.

## Etapes de réalisation

### 1. Créations et implémentations des différentes classes.

* Création de la classe *Livre* dont les différents types de livres (PDF, EPUB...)
  hériteront par la suite. Ainsi pour ajouter un nouveau format de livre. Il
  suffira de créer une nouvelle sous-classe de *Livre* et
  seulement d'implémenter la fonction de récupération correspondante
  à ce type de fichier. 
* Créations des classes *Livres_PDF* et *Livres_EPUB* comme expliqué précédemment.
  À ce stade les fonctions de récupération ne sont
  pas encore implémentées.
* Créations des classes *bibli*, *simple_bibli* et *bibli_scrap*.

### 2. Implémentations des fonctions
* Les fonctions *recup_pdf* et *recup_epub* sont définies de manière
  à renvoyer un dictionnaire des métadonnées (titre, auteur, langue, sujet et date) du fichier en utilisant
 les modules nécessaires.
* La fonction *ajoute* de la classe *simple_blibli*, ajoute un livre
 à partir d'un chemin d'accès.
* La fonction *alimenter* de la classe *bibli*, télécharge tous les livres d'une 
 page web à partir d'un url.
* La fonction *scrap* de la classe *bibli_scrap*.



