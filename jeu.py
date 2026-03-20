# py -3.11 jeu.py   lancement jeu
# ✅ Fenêtre Pygame
# ✅ Écran d'accueil
# ✅ Joueur qui bouge
# ✅ Tir avec délai de recharge
# ✅ Ennemis qui descendent
# ✅ Collisions balles/ennemis
# ✅ Score selon le type d'ennemi
# ✅ Vies avec cœurs emojis
# ✅ Game Over et réinitialisation
# ✅ Polices personnalisées, sur google font
# ✅ Couleurs personnalisées, couleur RGB choisi sur colorcodes
# ✅ Niveau suivant avec ennemis variés
# ✅ Réinitialisation complète au Game Over
# ✅ Champignons ennemis avec tireur aléatoire
# ✅ Collision champignon/lapin avec halo rouge
# ✅ Carottes bonus +1 vie (max 5 vies)
# ✅ Textes flottants (score, vies)
# ✅ Filtre sombre sur image de fond
# ✅ Menu principal avec boutons
# ✅ Scénario avec bulle de dialogue
# ✅ Crédits
# ✅ Formations d'ennemis (ligne, v, zigzag, aléatoire)
# ✅ Contrôles souris (déplacement + tir clic gauche)
# ✅ Page commandes (contrôles, ennemis, bonus/malus)
# ✅ Page commandes accessible depuis menu et après scénario
# ✅ High scores avec enregistrement JSON
# ✅ Saisie du pseudo après Game Over
# ✅ Panier carottes bonus (+5 vies toutes les 45 sec)
# ✅ Double tir bonus (10 sec, délai aléatoire 60-120 sec)
# ✅ Pause avec touche P
# ✅ Quitter avec ECHAP
# ✅ Souris bloquée dans la fenêtre pendant le jeu
# ✅ Légende ECHAP/P affiché pendant le jeu

import random # permet aléatoire 
import pygame # permet de creer le jeu
import json # pour sauvegarde scores

pygame.init()


######## Definitions  ########
#### FONCTION TEXTE FLOTTANT ###
def ajouter_float(x, y, texte, couleur): # faire des textes flottants
    floats.append({
        "x": x, "y": y,
        "texte": texte, # choix du text
        "couleur": couleur, #choix couleur
        "alpha": 400, # transparence
        "vy": -1 # vitesse de montée
    })

#### FONCTION ENNEMIS ####
def creer_ennemis(formation, nombre): #creation des formations
    ennemis = []
    types = ["oeuf", "cloche", "poulet"]
    par_ligne = 8

    if formation == "ligne":
        lignes = (nombre + par_ligne - 1) // par_ligne

        for ligne in range(lignes):
            debut = ligne * par_ligne
            fin = min(debut + par_ligne, nombre)
            nb = fin - debut

            for i in range(nb):
                ennemis.append({
                    "x": max(50, min(720, 80 + i * ((800 - 160) // (nb - 1 or 1)))),  # ← limite x
                    "y": 60 + ligne * 80,  # ← décalage par ligne
                    "vivant": True,
                    "type": types[(debut + i) % 3]  # ← debut + i pour varier les types
                    })
                
    elif formation == "v":
        lignes = (nombre + par_ligne - 1) // par_ligne #nomre de ligne selon nombre d'ennemis pour ne pas avoir de chevauchement

        for ligne in range(lignes):
            debut = ligne * par_ligne
            fin = min(debut + par_ligne, nombre)
            nb = fin - debut
            milieu = nb // 2
            espace = min(60, (700 // (nb or 1)))

            for i in range(nb):
                x = 400 + (i - milieu) * espace
                y = 60 + ligne * 80 + abs(i - milieu) * 20 # permet de decaler les ennemis selon la ligne
                ennemis.append({
                    "x": max(50, min(720, x)),
                    "y": y,
                    "vivant": True,
                    "type": types[(debut + i) % 3]
                    })
    
    elif formation == 'zigzag':
        lignes = (nombre + par_ligne - 1) // par_ligne
        for ligne in range(lignes):
            debut = ligne * par_ligne
            fin = min(debut + par_ligne, nombre)
            nb = fin - debut
            
            for i in range(nb):
                ennemis.append({
                    "x": max(50, min(720, 80 + i * ((800 - 160) // (nb - 1 or 1)))),
                    "y": 60 + ligne * 80 + (i % 2) * 40,
                    "vivant": True,
                    "type": types[(debut + i) % 3]
                })

    elif formation == "aleatoire":
        for i in range (nombre):
            ennemis.append({
            "x": random.randint(50, 750),
            "y": random.randint(30, 150),
            "vivant": True,
            "type": types[i % 3]
            })

    return ennemis

#### FONCTION SCORE ###
def charger_scores():
    try:
        with open("scores.json", "r") as f:
            return json.load(f)
    except:
        return []

def sauvegarder_scores(scores):
    with open("scores.json", "w") as f:
        json.dump(scores, f)

def ajouter_score(pseudo, score, niveau):
    scores = charger_scores()
    scores.append({"pseudo": pseudo, "score": score, "niveau": niveau})
    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:3]
    sauvegarder_scores(scores)

######## Variables  ###########

##### FENETRE ET GESTION DU JEU #####
fenetre = pygame.display.set_mode((800,600)) #Taille fenetre 
pygame.display.set_caption("Easter Invaders")#titre de la fenetre du jeu
horloge = pygame.time.Clock() # permet de stabiliser la fenetre pour qu'elle reste ouverte
running = True #variable demarrage jeu
score = 0 # variable score
vies = 5 #variable vie
dernier_tir = 0 #gere l'interval entre chaque tir
etat = "accueil"
niveau = 1
floats = []
pygame.mouse.set_visible(True)
souris_bouge = False
pseudo = ""
saisie_active = False

##### STYLES TEXTES #####
font = pygame.font.Font("fonttitre1.ttf", 40) #ecriture epaisse et ronde
font_texte2 = pygame.font.Font("fonttitre2.ttf", 50) #ecrire le texte 2, taille et font telecharger sur google font en ttf
font_emoji = pygame.font.SysFont("segoe ui emoji", 30) #ecriture avec emoji
font_petit = pygame.font.SysFont("arial", 20) # ecriture arial classique
font_float = pygame.font.SysFont("arial", 24) #ecriture des textes flottants
font_petit_gras = pygame.font.SysFont("arial", 20, bold=True)  # ecriture arial gras


##### IMAGES DU JEU #####
image = pygame.image.load("lapinface.png") #inserer une image 
image = pygame.transform.scale(image, (120, 120)) # taille image
image_ennemi = pygame.image.load("soldatpoulet2.png")
image_ennemi = pygame.transform.scale(image_ennemi, (80, 80))
image_ennemi1 = pygame.image.load("soldatcloche.png")
image_ennemi1 = pygame.transform.scale(image_ennemi1, (80, 80))
image_ennemi2 = pygame.image.load("soldatoeuf3.png")
image_ennemi2 = pygame.transform.scale(image_ennemi2, (80, 80))
image_fond_accueil = pygame.image.load("lapinfamille.jpg")
image_fond_accueil = pygame.transform.scale(image_fond_accueil, (800, 600))  # adapte à la taille de la fenêtre
image_champignon = pygame.image.load("champignon.png")
image_champignon = pygame.transform.scale(image_champignon, (50, 50))
image_carotte = pygame.image.load("carotte.png")
image_carotte = pygame.transform.scale(image_carotte, (50, 50))
image_arc = pygame.image.load("arc.png")
image_arc = pygame.transform.scale(image_arc, (100, 100))
image_bazooka = pygame.image.load("bazooka.png")
image_bazooka = pygame.transform.scale(image_bazooka, (100, 100))
image_bouclier = pygame.image.load("bouclier.png")
image_bouclier = pygame.transform.scale(image_bouclier, (100, 100))
image_doubletirs = pygame.image.load("doubletirs.png")
image_doubletirs = pygame.transform.scale(image_doubletirs, (100, 100))
image_horloge = pygame.image.load("horloge.png")
image_horloge = pygame.transform.scale(image_horloge, (100, 100))
image_paniercarottes = pygame.image.load("paniercarottes.png")
image_paniercarottes = pygame.transform.scale(image_paniercarottes, (100, 100))
image_balle = pygame.image.load("balle.png")
image_balle = pygame.transform.scale(image_balle, (30, 30))


##### BOUTONS DU JEU #####
boutons = [
    {"texte": "Jouer",     "x": 300, "y": 150, "w": 200, "h": 50},
    {"texte": "Scénario",  "x": 300, "y": 220, "w": 200, "h": 50},
    {"texte": "Commandes", "x": 250, "y": 290, "w": 300, "h": 50},
    {"texte": "Scores",    "x": 300, "y": 370, "w": 200, "h": 50},
    {"texte": "Crédits",   "x": 300, "y": 450, "w": 200, "h": 50},
]

#### SCENES DU JEU ####
scenes = [ #scenario du jeu
    {"image": "lapinfamille.jpg",
     "texte": "il était une fois une famille de lapins heureuses..."},
    {"image": "lapinkidnapping.jpg", 
     "texte": "Mais un jour, Monsieur Poulet enleva Maman Lapine !"},
    {"image": "lapinlapinedebutjeu.jpg", 
     "texte": "Papa Lapin jura de la retrouver coûte que coûte..."},
]
scene_index = 0 


##### EFFETS DU JEU #####
hit_effet = 0 # defini l'halo rouge autour de la fenetre
filtre = pygame.Surface((800, 600), pygame.SRCALPHA) # ajout d'un filtre sur image
filtre.fill((0, 0, 0, 140)) # filtre noir avec transparence


###### PERSONNAGES ET OBJETS DU JEU #####
lapin_x = 350 #position de depart du joueur horizontale
lapin_y = 480 #position fixe du joueur verticale
balles = [] #variable balle
#image de chaque ennemis et taille
types = ["oeuf", "cloche", "poulet"]
champignons = [] #variable champignon
dernier_champignon = 0 #gere l'intervalle entre chaque champignon
carotte = [] # variable carotte
derniere_carotte = 0 #gere l'intervalle entre les carottes
formations = ["ligne", "v", "zigzag", "aleatoire"] # formations des ennemis
ennemis = creer_ennemis("ligne", 3)
paniercarottes = []
dernier_paniercarottes = 0
doubletirs = []
dernier_doubletirs = None
doubletirs_actif = False #  est-ce que le doubletirs est actif ?
doubletirs_fin = 0  # temps du doubletirs
prochain_doubletirs = random.randint(60000, 120000)




     ######## JEU #########

while running: #lancement du jeu et de la fenetre
    temps_actuel = pygame.time.get_ticks() # donne temps écoulé en milliseconde tout comme Date.now()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    ######## COMMANDES ET MENU #########

        if event.type == pygame.MOUSEMOTION and etat == "jeu":
            souris_bouge = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()  # position de la souris
           #mise en place bouton et evenement du menu
            clique_menu = False

      ######## BOUTONS MENU #########
             
            for bouton in boutons:
                if (bouton["x"] < mx < bouton["x"] + bouton["w"] and
                    bouton["y"] < my < bouton["y"] + bouton["h"] and
                    etat == "accueil"):
                    clique_menu = True
                    if bouton["texte"] == "Jouer": # chemin du bouton
                        etat = "scenario"
                        pygame.event.set_grab(True)
                        scene_index = 0                     
                    elif bouton["texte"] == "Scénario":
                        etat = "scenario_menu" #scenario et retour menu principal
                        scene_index = 0
                    elif bouton["texte"] == "Commandes":
                        etat = "commandes"
                    elif bouton["texte"] == "Scores":
                        etat = "highscores"
                    elif bouton["texte"] == "Crédits":
                        etat = "credits"

            if not clique_menu:
                if etat in ("scenario", "scenario_menu"):
                    if 550 < mx < 730 and 555 < my < 595:
                        scene_index += 1
                        if scene_index >= len(scenes):
                            etat = "commandes_jeu" if etat == "scenario" else "accueil"  
                            scene_index = 0
                    if 60 < mx < 240 and 555 < my < 595:
                        etat = "commandes_jeu" if etat == "scenario" else "accueil"  # ← commandes_jeu !
                        scene_index = 0 
                        
                if etat == "commandes":
                    if 300 < mx < 500 and 530 < my < 590:
                        etat = "accueil"

                if etat == "commandes_jeu":
                    if 300 < mx < 500 and 530 < my < 590:
                        etat = "jeu"
                        pygame.event.set_grab(True)

                if etat == "highscores":
                    if 300 < mx < 500 and 500 < my < 550:
                        etat = "accueil"

                if etat == "credits":
                    if 300 < mx < 500 and 380 < my < 500:
                        etat = "accueil"

                if etat == "jeu":
                    if event.button == 1 and temps_actuel - dernier_tir > 400:
                        if doubletirs_actif:
                            balles.append({"x": lapin_x + 30, "y": lapin_y})
                            balles.append({"x": lapin_x + 80, "y": lapin_y})
                        else:
                            balles.append({"x": lapin_x + 50, "y": lapin_y})
                        dernier_tir = temps_actuel


        if event.type == pygame.KEYDOWN:
                

           
                if event.key == pygame.K_ESCAPE and etat == "jeu":
                    pygame.event.set_grab(False)
                    etat = "accueil"
                    
                if event.key == pygame.K_p and etat == "jeu":  #  pause
                    pygame.event.set_grab(False)
                    etat = "pause"

                elif event.key == pygame.K_p and etat == "pause":
                    pygame.event.set_grab(True)
                    etat = "jeu"

                if etat == "saisie_pseudo":
                    if event.key == pygame.K_RETURN and pseudo.strip() != "":
                        ajouter_score(pseudo, score, niveau)
                        pseudo = ""
                        score = 0
                        niveau = 1
                        etat = "highscores"
                    elif event.key == pygame.K_BACKSPACE:
                        pseudo = pseudo[:-1]
                    else:
                        if len(pseudo) < 12:
                            pseudo += event.unicode

                if event.key == pygame.K_ESCAPE and etat == "credits":
                    etat = "accueil"
        
    fenetre.blit(image_fond_accueil, (0, 0))  #remplir le fond avec image
    if etat not in ("scenario", "scenario_menu"):  #  filtre tout sauf scenario
        fenetre.blit(filtre, (0, 0))       


         ######## TEXTES FLOTTANTS #########
                     
    nouveaux_floats = []

    for f in floats:
        f["y"] += f["vy"]
        f["alpha"] -= 6 # disparition progressive
        if f["alpha"] > 0:
            surface = font_float.render(f["texte"], True, f["couleur"])
            surface.set_alpha(f["alpha"])
            fenetre.blit(surface, (f["x"], f["y"]))
            nouveaux_floats.append(f)
    floats = nouveaux_floats

         ######## EFFETS DU JEU #########

    if hit_effet > 0: # dessin du halo
        hit_effet -= 1
        alpha = hit_effet / 20 
        surface_rouge = pygame.Surface((800, 600), pygame.SRCALPHA) # defini la taille du halo et la transparence
        pygame.draw.rect(surface_rouge, (255, 0, 0, int(alpha * 180)), (0, 0, 800, 600), 40) # couleur et epaisseur du halo
        fenetre.blit(surface_rouge, (0, 0))

          ######## MENU PRINCIPAL #########

    if etat == "accueil":
        texte = font.render("EASTER INVADERS", True, (99, 235, 149))#texte 1
        x = (800 - texte.get_width()) // 2 # larguer de la fenetre - largeur du texte pour centrer le texte
        fenetre.blit(texte, (x, 100)) # emplacement du texte 1 centré
        mx, my = pygame.mouse.get_pos()
        for bouton in boutons:
        # changer couleur si souris dessus
            survol = (bouton["x"] < mx < bouton["x"] + bouton["w"] and
                  bouton["y"] < my < bouton["y"] + bouton["h"])
            couleur = (27, 125, 59) if survol else (216, 235, 223)
            pygame.draw.rect(fenetre, couleur, 
                        (bouton["x"], bouton["y"], bouton["w"], bouton["h"]), 
                        border_radius=10)
            t = font.render(bouton["texte"], True, (99, 235, 149)) #couleur texte bouton
            tx = bouton["x"] + (bouton["w"] - t.get_width()) // 2
            ty = bouton["y"] + (bouton["h"] - t.get_height()) // 2
            fenetre.blit(t, (tx, ty))

    elif etat == "saisie_pseudo":
        t = font.render("Nouveau score !", True, (99, 235, 149))
        fenetre.blit(t, ((800 - t.get_width()) // 2, 150))
        t = font_petit_gras.render(f"Score : {score}  |  Niveau : {niveau}", True, (255, 255, 255))
        fenetre.blit(t, ((800 - t.get_width()) // 2, 220))
        t = font_petit_gras.render("Entre ton pseudo :", True, (255, 255, 255))
        fenetre.blit(t, ((800 - t.get_width()) // 2, 280))
        pygame.draw.rect(fenetre, (218, 237, 225), (250, 310, 300, 50), border_radius=10)
        t = font.render(pseudo + "|", True, (9, 79, 35))
        fenetre.blit(t, ((800 - t.get_width()) // 2, 318))
        t = font_petit_gras.render("Appuie sur ENTRÉE pour valider", True, (255, 255, 255))
        fenetre.blit(t, ((800 - t.get_width()) // 2, 390))

    elif etat == "pause":
        t = font.render("PAUSE", True, (99, 235, 149))
        fenetre.blit(t, ((800 - t.get_width()) // 2, 250))
        t = font_petit_gras.render("Appuie sur P pour continuer", True, (255, 255, 255))
        fenetre.blit(t, ((800 - t.get_width()) // 2, 320))
        
    elif etat == "highscores":
        t = font.render("Meilleurs scores", True, (99, 235, 149))
        fenetre.blit(t, ((800 - t.get_width()) // 2, 50))
        scores = charger_scores()
        medals = ["1", "2", "3"]
        couleurs = [(255, 215, 0), (192, 192, 192), (205, 127, 50)]
        if scores:
            for i, s in enumerate(scores):
                y = 150 + i * 100
                pygame.draw.rect(fenetre, (27, 125, 59), (150, y - 10, 500, 70), border_radius=10)
                t = font.render(medals[i], True, couleurs[i])
                fenetre.blit(t, (170, y + 5))
                t = font.render(s["pseudo"], True, (255, 255, 255))
                fenetre.blit(t, (240, y + 5))
                t = font.render(f"{s['score']} pts", True, couleurs[i])
                fenetre.blit(t, (500, y + 5))
                t = font_petit_gras.render(f"niveau {s['niveau']}", True, (200, 200, 200))
                fenetre.blit(t, (510, y + 40))
        else:
            t = font_petit_gras.render("Aucun score enregistré", True, (200, 200, 200))
            fenetre.blit(t, ((800 - t.get_width()) // 2, 250))
        pygame.draw.rect(fenetre, (218, 237, 225), (300, 500, 200, 50), border_radius=10)
        t_retour = font_float.render("← Retour au menu", True, (9, 79, 35))
        tx = 300 + (200 - t_retour.get_width()) // 2
        fenetre.blit(t_retour, (tx, 513))

       ######## MENU JEU #########
          
    elif etat == "jeu": #si on appui sur jouer
        fenetre.blit(image, (lapin_x, lapin_y))    #position de l'image defini plus haut
        # légende en bas de l'écran
        t = font_petit.render("ECHAP : quitter  |  P : pause", True, (255, 255, 255, 100))
        fenetre.blit(t, ((800 - t.get_width()) // 2, 575))
        touchs = pygame.key.get_pressed()#choix des touches de jeu

    
        ######## COMMANDES JEU #########

        #touches clavier
        if touchs[pygame.K_LEFT]:#lapin va de 10px a gauche avec la fleche gauche
            lapin_x -= 10
        if touchs[pygame.K_RIGHT]:#lapin va de 10px a droite avec la fleche droite
            lapin_x += 10
       
        if souris_bouge: # commande souris s'active seulement si la souris bouge
            mx_jeu, my_jeu = pygame.mouse.get_pos() #jouer avec souris
            lapin_x = mx_jeu - 60 #centre lapin à la souris
            souris_bouge = False #reset

        #touche tir
        if touchs[pygame.K_SPACE] and temps_actuel - dernier_tir > 400: #tir avec pause de 0.4 sec entre chaque tir, pas de tir continu
             if doubletirs_actif:
                balles.append({"x": lapin_x + 30, "y": lapin_y})   #  balle gauche
                balles.append({"x": lapin_x + 80, "y": lapin_y})   #  balle droite
             else:
                balles.append({"x": lapin_x + 50, "y": lapin_y})   #  balle simple
             dernier_tir = temps_actuel
        
        # chrono du doubletir
        if doubletirs_actif:
            temps_restant = max(0, (doubletirs_fin - temps_actuel) // 1000)
            t = font_petit_gras.render(f"DOUBLE TIR : {temps_restant}s", True, (242, 33, 5))
            tx = (800 - t.get_width()) // 2
            fenetre.blit(t, (tx + 40, 10))
            fenetre.blit(image_doubletirs, (tx - 70, 2))  #  image à gauche du texte
        if doubletirs_actif and temps_actuel > doubletirs_fin:
            doubletirs_actif = False
            ajouter_float(300, 300, "DOUBLE TIR TERMINÉ !", (242, 33, 5))

       ######## BALLES #########

        for balle in balles:#determine les balles
            balle["y"] -= 7 #chaque balle monte de 7px
            fenetre.blit(image_balle, (balle["x"], balle["y"])) #taille des balles et trajectoire

        balles = [b for b in balles if b["y"] > 0]# pour que la balle ne sorte pas de la fentre de jeu
        lapin_x = max(0, min(700, lapin_x)) #pour ne pas sortir de la fenetre            
        

        ######## TIR SUR ENNEMIS #########

        for ennemi in ennemis :
            if ennemi["vivant"]:
                for balle in balles: #Tue ennemi si :
                    if (balle["x"] < ennemi["x"] + 60 and 
                        balle["x"] + 6 > ennemi["x"] and
                        balle["y"] < ennemi["y"] + 60 and
                        balle["y"] + 12 > ennemi["y"] ):
                        ennemi["vivant"] = False #ennemi tué
                        balles = [b for b in balles if b != balle] #evite d'utiliser  balles.remove(balle) cette liste est plus fiable pour faire disparaitre les balles 
                        if ennemi["type"] == "oeuf": #score selon ennemi touché
                            score += 100
                            ajouter_float(ennemi["x"], ennemi["y"], "+ 100 points", (126, 245, 5)) # texte flottant texte et couleur
                        elif ennemi["type"] == "cloche":
                            score += 200
                            ajouter_float(ennemi["x"], ennemi["y"], "+ 200 points", (126, 245, 5))
                        elif ennemi["type"] == "poulet":
                            score += 300
                            ajouter_float(ennemi["x"], ennemi["y"], "+ 300 points", (126, 245, 5))


              ######## CHAMPIGNONS #########

              ######## TIR DE CHAMPIGNONS #########

        if temps_actuel - dernier_champignon > 3000: #champignon toutes les 2 sec mini
             vivants = [e for e in ennemis if e["vivant"]]
             if vivants: # si ennemi vivant il tire champignon
                tireur = random.choice(vivants) # tireur aléatoire avec random
                champignons.append({
                    "x": tireur["x"] + 30,
                    "y": tireur ["y"] + 60,
                    "w": 30, "h": 30
                    })
                dernier_champignon = temps_actuel

        for champ in champignons:
            champ["y"] += 3
            fenetre.blit(image_champignon, (champ["x"], champ["y"])) #image du champignon
                            
        champignons = [c for c in champignons if c["y"] < 600] #supprime champignon hors fenetre

            ######## COLLISION DE CHAMPIGNONS #########

        for champ in champignons: # collision entre lapin et champignon - 1 vie
            if (champ["x"] < lapin_x + 100 and
                champ["x"] + 30 > lapin_x and
                champ["y"] < lapin_y + 100 and
                champ["y"] + 30 > lapin_y):
                vies -= 1
                ajouter_float(lapin_x + 50, lapin_y, "-1 vie !", (245, 17, 17))
                hit_effet = 20 # niveau d'effet
                champignons = [c for c in champignons if c != champ]
                break

                ######## CAROTTES #########

                ######## TEMPS ENTRE CHAQUE CAROTTE #########

        if temps_actuel - derniere_carotte > 20000:
            carotte.append({
                "x": random.randint(50, 750),
                "y": -60
            })
            derniere_carotte = temps_actuel

        for c in carotte:
            c["y"] += 2
            fenetre.blit(image_carotte, (c["x"], c["y"]))

        carotte = [c for c in carotte if c["y"] < 600]
                        

            ######## COLLISION AVEC CAROTTES #########

        for carottes in carotte: # collision carotte
            if (carottes["x"] < lapin_x + 100 and
                carottes["x"] + 30 > lapin_x and
                carottes["y"] < lapin_y + 100 and
                carottes["y"] + 30 > lapin_y):
                vies = min(vies + 1, 5) #    # ajoute une vie mais pas plus de 5 vie max
                ajouter_float(lapin_x + 50, lapin_y, "+1 vie", (126, 245, 5))
                carotte = [c for c in carotte if c != carottes]

                ######## PANIERCAROTTES #########

        ######## TEMPS ENTRE CHAQUE PANIERCAROTTES #########

        if temps_actuel - dernier_paniercarottes > 45000:
            paniercarottes.append({
                "x": random.randint(50, 750),
                "y": -60
            })
            dernier_paniercarottes = temps_actuel

        for c in paniercarottes:
            c["y"] += 2
            fenetre.blit(image_paniercarottes, (c["x"], c["y"]))

        paniercarottes = [c for c in paniercarottes if c["y"] < 600]
                        

            ######## COLLISION AVEC PANIERCAROTTES #########

        for panier in paniercarottes: # collision paniercarottes
            if (panier["x"] < lapin_x + 100 and
                panier["x"] + 30 > lapin_x and
                panier["y"] < lapin_y + 100 and
                panier["y"] + 30 > lapin_y):
                vies = 5 #    # ajoute vies max
                ajouter_float(lapin_x + 50, lapin_y, "VIES MAX", (126, 245, 5))
                paniercarottes = [c for c in paniercarottes if c != panier]
         

         ######## DOUBLETIRS #########

           ######## TEMPS ENTRE CHAQUE DOUBLETIRS #########

        if dernier_doubletirs is None:
            dernier_doubletirs = temps_actuel # avoir le 1er frame

        if temps_actuel - dernier_doubletirs > prochain_doubletirs:
            doubletirs.append({
                "x": random.randint(50, 750),
                "y": -60
            })
            dernier_doubletirs = temps_actuel
            prochain_doubletirs = random.randint(60000, 120000)

        for c in doubletirs:
            c["y"] += 2
            fenetre.blit(image_doubletirs, (c["x"], c["y"]))

        doubletirs = [c for c in doubletirs if c["y"] < 600]
                        

            ######## COLLISION AVEC DOUBLETIRS #########

        for tir in doubletirs: # collision doubletirs
            if (tir["x"] < lapin_x + 100 and
                tir["x"] + 30 > lapin_x and
                tir["y"] < lapin_y + 100 and
                tir["y"] + 30 > lapin_y):
                doubletirs_actif = True
                doubletirs_fin = temps_actuel + 20000 # dure 20 sec
                ajouter_float(lapin_x + 50, lapin_y, "DOUBLE TIRS", (126, 245, 5))
                doubletirs = [c for c in doubletirs if c != tir]

        if doubletirs_actif and temps_actuel > doubletirs_fin:
            doubletirs_actif = False  # retour au tir simple
      
      
      
      
      
      
        ######## AFFICHAGE SCORE #########

        text_score = font.render(f"score : {score}", True, (255, 255, 255)) #affichage du score
        fenetre.blit(text_score, (10, 10)) #emplacement texte score

        ######## GESTION ENNEMIS #########

        ######## ENNEMIS ARRIVE EN BAS #########

        for ennemi in ennemis:
            if ennemi["vivant"] and ennemi["y"] > 600: #verifie si ennemi atteint le bas de la fenetre
                ennemi["vivant"] = False #si atteind le bas = ennemi meurt
                vies -=1 #si atteind le bas joueur perd 1 vie


        ######## AFFICHAGE ENNEMIS #########

        for ennemi in ennemis:#affichage des ennemis dans la fenetre de jeu
            if ennemi["vivant"]:
                if ennemi["type"] == "poulet":
                    fenetre.blit(image_ennemi, (ennemi["x"], ennemi["y"]))
                elif ennemi["type"] == "cloche":
                    fenetre.blit(image_ennemi1, (ennemi["x"], ennemi["y"]))
                elif ennemi["type"] == "oeuf":
                    fenetre.blit(image_ennemi2, (ennemi["x"], ennemi["y"]))
        
        ######## DEPLACEMENTS ENNEMIS #########

        for ennemi in ennemis: #deplacement des ennemis
            if ennemi["vivant"]:
                ennemi["y"] += 0.4 #vitesse de descente des ennemi en Y "verticale" à modifier celon les niveaux

        ######## NIVEAUX #########

        ######## PASSAGE DE NIVEAUX #########
        
        if all(not e["vivant"] for e in ennemis): #passage de niveau
            niveau += 1
            champignons = []        
            carotte = []            
            dernier_champignon = 0  
            derniere_carotte = 0
            texte_niveau = font.render(f"Niveau {niveau} !", True, (99, 235, 149))
            x = (800 - texte_niveau.get_width()) // 2 
            fenetre.blit(texte_niveau, (x, 300))
            pygame.display.flip()
            pygame.time.wait(2000)
            ennemis = [] #reinitialise les ennemis en rajoutant 1 de plus à chaque niveau
            formation = formations[(niveau - 1) % len(formations)]
            ennemis = creer_ennemis(formation, niveau + 2)


        ######## GAME OVER #########

        if vies <= 0: #verifie si vie arrive a 0
            texte_go = font.render("GAME OVER", True, (255, 0, 0)) #texte affiche si vie arrive a 0
            x = (800 - texte_go.get_width()) // 2 
            fenetre.blit(texte_go, (x, 300)) #emplacement fenetre GAME OVER
            pygame.display.flip()
            pygame.time.wait(3000) #attend 3 sec
            #reinitialise tout
            vies = 3
            lapin_x = 350
            balles = []
            paniercarottes = []
            dernier_paniercarottes = 0
            ennemis = creer_ennemis("ligne", 3)
            champignons = []        
            carotte = []    
            doubletirs = []
            dernier_doubletirs = 0 
            doubletirs_actif = False 
            doubletirs_fin = 0       
            dernier_champignon = 0  
            derniere_carotte = 0
            pygame.event.set_grab(False)
            etat = "saisie_pseudo"
            
    
        ######## VIES #########

        ######## AFFICHAGE VIES #########

        texte_vies = font_emoji.render("❤️" * vies, True, (255, 0, 0)) #affichage des vie avec police compatible emojis
        fenetre.blit(texte_vies, (550, 10)) #emplacement de l'affichage des vie    
        
        ######## MENU SCENARIO #########

    elif etat in ("scenario", "scenario_menu"):
        scene = scenes[scene_index]
        img_scene = pygame.image.load(scene["image"])
        img_scene = pygame.transform.scale(img_scene, (800, 600))
        fenetre.blit(img_scene, (0, 0))
        

        ######## AFFICHAGE SCENARIO #########

        # bulle de dialogue
        pygame.draw.rect(fenetre, (218, 237, 225), (40, 420, 720, 120), border_radius=15)
        pygame.draw.rect(fenetre, (9, 79, 35), (40, 420, 720, 120), 2, border_radius=15)

        # texte dans la bulle avec retour à la ligne automatique
        mots = scene["texte"].split(" ")
        ligne = ""
        y_texte = 445
        for mot in mots:
            test = ligne + mot + " "
            if font_float.size(test)[0] > 680:
                t = font_float.render(ligne, True, (9, 79, 35))
                fenetre.blit(t, (60, y_texte))
                ligne = mot + " "
                y_texte += 28
            else:
                ligne = test
        t = font_float.render(ligne, True, (9, 79, 35))
        fenetre.blit(t, (60, y_texte))

        ######## COMMANDE SCENARIO #########

        # boutons suivant et passer
        pygame.draw.rect(fenetre, (218, 237, 225), (550, 555, 180, 40), border_radius=8)
        t_suiv = font_float.render("Suivant", True, (9, 79, 35))
        fenetre.blit(t_suiv, (555, 563))

        pygame.draw.rect(fenetre, (218, 237, 225), (60, 555, 180, 40), border_radius=8)
        t_pass = font_float.render("Passer", True, (9, 79, 35))
        fenetre.blit(t_pass, (65, 563))

        ######## MENU COMMANDES #########

    elif etat in ("commandes", "commandes_jeu"):
    
        # titre
        t = font.render("Comment jouer", True, (99, 235, 149))
        fenetre.blit(t, ((800 - t.get_width()) // 2, 15))

        # contrôles
        t = font.render("Contrôles", True, (255, 255, 255))
        fenetre.blit(t, ((800 - t.get_width()) // 2, 65))
        for i, ligne in enumerate([
            "← → ou Souris : déplacer le lapin",
            "Espace ou Clic gauche : tirer",
        ]):
            t = font_petit_gras.render(ligne, True, (99, 235, 149))
            fenetre.blit(t, ((800 - t.get_width()) // 2, 105 + i * 25))

        # ennemis
        t = font.render("Ennemis", True, (255, 255, 255))
        fenetre.blit(t, ((800 - t.get_width()) // 2, 160))
        total_largeur = 3 * 80 + 2 * 60
        debut_x = (800 - total_largeur) // 2
        fenetre.blit(image_ennemi2, (debut_x, 195))
        fenetre.blit(image_ennemi1, (debut_x + 140, 195))
        fenetre.blit(image_ennemi, (debut_x + 280, 195))
        t = font_petit_gras.render("100 pts", True, (99, 235, 149))
        fenetre.blit(t, (debut_x + 20, 280))
        t = font_petit_gras.render("200 pts", True, (99, 235, 149))
        fenetre.blit(t, (debut_x + 160, 280))
        t = font_petit_gras.render("300 pts", True, (99, 235, 149))
        fenetre.blit(t, (debut_x + 300, 280))

        # bonus/malus
        t = font.render("Bonus / Malus", True, (255, 255, 255))
        fenetre.blit(t, ((800 - t.get_width()) // 2, 305))
        total_largeur3 = 4 * 60 + 3 * 20
        debut_x3 = (800 - total_largeur3) // 2
        fenetre.blit(image_carotte, (debut_x3, 370))
        fenetre.blit(image_champignon, (debut_x3 + 80, 370))
        fenetre.blit(image_paniercarottes, (debut_x3 + 180, 340))
        fenetre.blit(image_doubletirs, (debut_x3 + 280, 340))
        t = font_petit_gras.render("+1 vie", True, (99, 235, 149))
        fenetre.blit(t, (debut_x3 + 5, 440))
        t = font_petit_gras.render("-1 vie", True, (245, 17, 17))
        fenetre.blit(t, (debut_x3 + 85, 440))
        t = font_petit_gras.render("+5 vies", True, (99, 235, 149))
        fenetre.blit(t, (debut_x3 + 210, 440))
        t = font_petit_gras.render("x2 tir", True, (99, 235, 149))
        fenetre.blit(t, (debut_x3 + 300, 440))

        # bouton retour
        # bouton différent selon l'état
        if etat == "commandes_jeu":
            pygame.draw.rect(fenetre, (218, 237, 225), (300, 530, 200, 50), border_radius=10)
            t_retour = font_float.render("Jouer !", True, (9, 79, 35))
        else:
            pygame.draw.rect(fenetre, (218, 237, 225), (300, 530, 200, 50), border_radius=10)
            t_retour = font_float.render("← Retour au menu", True, (9, 79, 35))
        tx = 300 + (200 - t_retour.get_width()) // 2
        fenetre.blit(t_retour, (tx, 543))



        ######## MENU CREDITS #########

    elif etat == "credits":
        texte_c = font.render("Easter Invaders", True, (99, 235, 149))
        x = (800 - texte_c.get_width()) // 2
        fenetre.blit(texte_c, (x, 150))
        texte_c2 = font.render("Créé par HAMDOUN Nada", True, (255, 255, 255))
        x = (800 - texte_c2.get_width()) // 2
        fenetre.blit(texte_c2, (x, 250))
        texte_c3 = font.render("Python / Pygame 2026", True, (255, 255, 255))
        x = (800 - texte_c3.get_width()) // 2
        fenetre.blit(texte_c3, (x, 320))
        pygame.draw.rect(fenetre, (218, 237, 225), (300, 430, 200, 50), border_radius=10) # bouton retour menu de crédits
        t_retour = font_float.render("← Retour au menu", True, (9, 79, 35))
        tx = 300 + (200 - t_retour.get_width()) // 2
        fenetre.blit(t_retour, (tx, 443))
                
        

    pygame.display.flip()
    horloge.tick(60)
     

    ######## QUIT JEU #########

pygame.quit()



