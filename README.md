# Optimisation

Ce programme est compatible avec les versions de python 3.11.x et supérieur.

Les dépendances à installer sont présentes dans le fichier requirements.txt

> Cette commande permet d'installer toute les dépendances il est conseillé d'utiliser un venv
```bash
pip install -r .\requirements.txt
```

A la fin de son éxécution il affiche via matplotlib le clavier et l'évolution du meilleur individu
et créé un fichier res.txt avec le resultat dans le dossier resultats ainsi que la representation graphique du clavier et de l'évolution du meilleur individu.

Un docker-compose est disponible pour lancer le programme dans un container docker pour éviter l'installation des dépendances, dans ce cas matplotlib ne pourra pas ouvrir de fenetre graphique mais les résultats seront quand même sauvegardés dans le dossier resultats avec l'image du clavier ( un bug/effet de bord nous empeche de sauvegarder l'image du graphique de l'évolution du meilleur individu en mode CLI)

```bash
docker-compose up
```
> Attention il y a un peu de latence/décalage pour l'affichage des logs dans le terminal quand on utilise docker-compose , ils peuvent arriver par paquets.