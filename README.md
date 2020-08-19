# Projet *tpviz* : moteur de traitement de données 

Dans ce dossier se trouve le programme : **apptp-data-engine**. Ce programme a servi a traiter et à produire les données qui ont servi dans le cadre du travail de mémoire **La couverture géographique des reportages de Temps Présent : apport des archives numériques et des visualisations de données à une histoire des magazines de grands reportages**. Ce projet porte le nom de code tpviz.

Le programme *apptp-data-engine* est un programme Python. Ce programme n'est pas une librairie. Il a été créé spécialement pour traiter le corpus orignial qui a été sélectionné dans le cadre du mémoire et pour laisser une trace des étapes de traitement des données que j'ai suivi dans ce projet. A noter que ce programme pourrait évoluer vers une librairie. Pour des précisions sur l'orientation méthodologique prise dans le traitement des données, le lecteur peut se référer au chapitre 2 et 3 du mémoire.

La fonction première du programme est d'acquérir des données (via la librairie ssr-rts-api) et d'enrichir les données de localisations avec des données de géolocalisation. Les données de géolocalisation sont empruntées à l'API Googlemaps.

# commment ?

Pour explorer le code, il suffit de télécharger le dossier de sauvegarde, de le déployer dans un dossier local et de le dossier avec Python. Pour des raisons de place, l'environnement virtuel avec lequel je travail n'a pas été déposé dans le dossier.

Pour faire tourner le programme l'environnement suivant doit être en place sur une machine:

1. Python 3
2. Idéalement la base de données apptp-db : https://github.com/rerouj/apptp-db
3. les librairies suivantes doivent être installées
    a. ssr-rts-api
    b. marshmallow
    c. matplotlib
    d. pymongo
    e. googlemaps

# qui ?

L'ensemble du code apptp-data-engine a été produit par l'auteur du mémoire (Renato Diaz). N'hésitez pas à forker et n'oubliez pas d'ajouter une étoile ⭐️ ;)

Contact renato.diaz@outlook.com
