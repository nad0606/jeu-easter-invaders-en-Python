# 🐰 EASTER INVADERS — Python / Pygame

> Création en Python/Pygame d'un jeu de type Space Invaders sur le thème de Pâques,  
> initialement développé en HTML5/CSS3/JavaScript disponible sur mon GITHUB.

## 🎮 Description du jeu

Easter Invaders est un jeu de tir inspiré de Space Invaders.  
Le joueur incarne Papa Lapin qui doit défendre sa famille contre des vagues d'ennemis de Pâques.

- **3 types d'ennemis** : Œuf (100 pts), Cloche (200 pts), Poulet (300 pts)
- **Système de vies** : jusqu'à 5 vies représentées par des cœurs ❤️
- **Niveaux progressifs** : Niveaux illimités, chaque niveau ajoute des ennemis avec formations variées
- **Délai de tir** : rechargement de 400ms entre chaque balle
- **Écran d'accueil** et **Game Over** avec réinitialisation complète
- **Menu complet** : Jouer, Scénario, Commandes, Scores, Crédits
- **Scénario narratif** : 3 scènes avec bulle de dialogue avant le jeu
- **High scores** : top 3 enregistré avec pseudo (fichier JSON)
- **Pause** : touche P pour mettre le jeu en pause
- **Bonus** : carottes (+1 vie), panier de carottes (+5 vies), double tir (20 sec)
- **Malus** : champignons lancés par les ennemis (-1 vie)
---

## 🛠️ Technologies utilisées

| Technologie | Utilisation |
|---|---|
| Python 3.11 | Langage principal |
| Pygame 2.6 | Moteur graphique et gestion des événements |
| JSON | Sauvegarde des meilleurs scores |


## 🚀 Installation et lancement

### Prérequis

- Python 3.11 (⚠️ Pygame n'est pas compatible avec Python 3.14+)
- Pygame 2.6

### Installation de Pygame


py -3.11 -m pip install pygame


### Lancer le jeu


py -3.11 jeu.py



## 🕹️ Contrôles
 
| Touche / Action | Effet |
|---|---|
| ← / → | Déplacer le lapin |
| Souris | Déplacer le lapin |
| Espace | Tirer |
| Clic gauche | Tirer |
| P | Pause |
| ECHAP | Quitter vers le menu |

## 👾 Ennemis et formations
 
| Type | Points |
|---|---|
| Œuf | 100 pts |
| Cloche | 200 pts |
| Poulet | 300 pts |
 
**4 formations** : ligne, V, zigzag, aléatoire — les formations s'adaptent automatiquement pour ne jamais dépasser les bords de la fenêtre.
 
Les ennemis **lancent des champignons** aléatoirement vers le joueur.
 
---
 
## ⚡ Bonus et Malus
 
| Objet | Effet | Fréquence |
|---|---|---|
| 🥕 Carotte | +1 vie (max 5) | toutes les 20 sec |
| 🧺 Panier de carottes | +5 vies (max 5) | toutes les 45 sec |
| 🔥 Double tir | 2 balles simultanées pendant 20 sec | aléatoire 60-120 sec |
| 🍄 Champignon | -1 vie | toutes les 3 sec |
 
---
 
## 🏆 High Scores
 
Les 3 meilleurs scores sont sauvegardés dans un fichier `scores.json`.  
À chaque Game Over, le joueur peut entrer son pseudo pour apparaître au classement.
 
---
 
## 🎬 Menu principal
 
- **Jouer** → Scénario → Page commandes → Jeu
- **Scénario** → Voir uniquement le scénario
- **Commandes** → Contrôles, ennemis, bonus/malus
- **Scores** → Top 3 des meilleurs scores
- **Crédits** → Auteure du jeu
 

## 🔄 Du JavaScript au Python — Ce que j'ai appris

Ce projet est la **Création en Python** de mon jeu Easter Invaders,  
initialement développé en HTML5 Canvas / JavaScript / CSS.

### Comparaison des deux versions

| Concept | JavaScript (version originale) | Python/Pygame (cette version) |
|---|---|---|
| Boucle de jeu | `requestAnimationFrame()` | `while running` + `horloge.tick(60)` |
| Temps écoulé | `Date.now()` | `pygame.time.get_ticks()` |
| Dessin à l'écran | `ctx.drawImage()` | `fenetre.blit()` |
| Effacer l'écran | `ctx.clearRect()` | `fenetre.fill()` |
| Afficher | automatique | `pygame.display.flip()` |
| Touches pressées | `addEventListener('keydown')` | `pygame.key.get_pressed()` |
| Stocker les ennemis | tableau d'objets `[]` | liste de dictionnaires `[]` |
| Collisions | fonction `hit(a, b)` manuelle | même logique rectangulaire |
| Texte à l'écran | `ctx.fillText()` | `font.render()` + `blit()` |
| Sauvegarde scores | `localStorage` | fichier `JSON` |
 
### Ce qui change vraiment
 
En JavaScript, le navigateur gère le rendu automatiquement.  
En Python avec Pygame, **tout est manuel** :
- On efface l'écran à chaque frame avec `fill()`
- On redessine tout dans l'ordre
- On appelle `flip()` pour afficher le résultat
 
Cela permet de comprendre exactement ce qui se passe à chaque image du jeu.
 
### Ce que j'ai appris en Python

- Les **variables**, **conditions**, **boucles** et **fonctions** de base
- Les **listes** et **dictionnaires** pour stocker les données du jeu
- Le **f-string** : `f"Score : {score}"`
- Le **modulo** `%` pour alterner les types d'ennemis
- La gestion des **images** et **polices** avec Pygame
- La structure d'une **boucle de jeu** professionnelle

## 📌 Version JS originale

La version JavaScript originale du jeu est disponible séparément.  
Elle inclut 20 niveaux, des formations d'ennemis variées, un scénario narratif,  
un système de classement localStorage et des contrôles mobiles.

**HAMDOUN Nada** 

## Capture d'écran du jeu en cours de création ##

![Ecran d'accueil](jeueasterinvaderspython1.jpg)