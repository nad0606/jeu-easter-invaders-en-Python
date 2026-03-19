# ✅ Fenêtre Pygame
# ✅ Écran d'accueil
# ✅ Joueur qui bouge
# ✅ Tir avec délai de recharge
# ✅ Ennemis qui descendent
# ✅ Collisions balles/ennemis
# ✅ Score selon le type d'ennemi
# ✅ Vies avec cœurs emojis
# ✅ Game Over
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

import random
import pygame
pygame.init()


# Definitions

def ajouter_float(x, y, texte, couleur): # faire des textes flottants
    floats.append({
        "x": x, "y": y,
        "texte": texte, # choix du text
        "couleur": couleur, #choix couleur
        "alpha": 400, # transparence
        "vy": -1 # vitesse de montée
    })


def creer_ennemis(formation, nombre): #creation des formations
    ennemis = []
    types = ["oeuf", "cloche", "poulet"]

    if formation == "ligne":
        for i in range(nombre):
            ennemis.append({
                "x": 80 + i * ((800 - 160) // (nombre - 1 or 1)),
                "y": 60,
                "vivant": True,
                "type": types[i % 3]
                })
            
    elif formation == "v":
        milieu = nombre // 2
        for i in range(nombre):
            x = 400 + (i - milieu) * 70
            y = 60 + abs(i - milieu) * 20
            ennemis.append({
                "x": max(50, min(750, x)),
                "y": y,
                "vivant": True,
                "type": types[i % 3]
                })
    
    elif formation == 'zigzag':
        for i in range(nombre):
            ennemis.append({
                "x": max(50, min(720, 80 + i * 80)),
                "y": 60 + (i % 3) * 60,
                "vivant": True,
                "type": types[i % 3]
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

   
# Variables

fenetre = pygame.display.set_mode((800,600), pygame.RESIZABLE) #Taille fenetre et pygame.RESIZABLE permet de pouvoir agrandir la fenetre
pygame.display.set_caption("Easter Invaders")#titre de la fenetre du jeu

horloge = pygame.time.Clock() # permet de stabiliser la fenetre pour qu'elle reste ouverte

running = True #variable demarrage jeu

font = pygame.font.Font("fonttitre1.ttf", 40) #ecrire le texte 1, taille et font
font_texte2 = pygame.font.Font("fonttitre2.ttf", 50) #ecrire le texte 2, taille et font telecharger sur google font en ttf
font_emoji = pygame.font.SysFont("segoe ui emoji", 30) #appel une police avec emoji

image = pygame.image.load("lapinface.png") #inserer une image 
image = pygame.transform.scale(image, (120, 120)) # taille image
lapin_x = 350 #position de depart du joueur horizontale
lapin_y = 480 #position fixe du joueur verticale
balles = [] #variable balle
#image de chaque ennemis et taille
image_ennemi = pygame.image.load("soldatpoulet2.png")
image_ennemi = pygame.transform.scale(image_ennemi, (80, 80))
image_ennemi1 = pygame.image.load("soldatcloche.png")
image_ennemi1 = pygame.transform.scale(image_ennemi1, (80, 80))
image_ennemi2 = pygame.image.load("soldatoeuf3.png")
image_ennemi2 = pygame.transform.scale(image_ennemi2, (80, 80))
score = 0 # variable score
vies = 3 #variable vie
dernier_tir = 0 #gere l'interval entre chaque tir
etat = "accueil"
niveau = 1
types = ["oeuf", "cloche", "poulet"]
image_fond_accueil = pygame.image.load("lapinfamille.jpg")
image_fond_accueil = pygame.transform.scale(image_fond_accueil, (800, 600))  # adapte à la taille de la fenêtre
champignons = [] #variable champignon
dernier_champignon = 0 #gere l'intervalle entre chaque champignon
hit_effet = 0 # defini l'halo rouge autour de la fenetre
image_champignon = pygame.image.load("champignon.png")
image_champignon = pygame.transform.scale(image_champignon, (50, 50))
carotte = [] # variable carotte
derniere_carotte = 0 #gere l'intervalle entre les carottes
image_carotte = pygame.image.load("carotte.png")
image_carotte = pygame.transform.scale(image_carotte, (50, 50))
floats = []
font_float = pygame.font.SysFont("arial", 24)
filtre = pygame.Surface((800, 600), pygame.SRCALPHA) # ajout d'un filtre sur image
filtre.fill((0, 0, 0, 120)) # filtre noir avec transparence
formations = ["ligne", "v", "zigzag", "aleatoire"] # formations des ennemis
ennemis = creer_ennemis("ligne", 3)
boutons = [ #création bouton menu principal
    {"texte": "Jouer",     "x": 300, "y": 200, "w": 200, "h": 50},
    {"texte": "Scénario", "x": 300, "y": 280, "w": 200, "h": 50},
    {"texte": "Crédits",  "x": 300, "y": 360, "w": 200, "h": 50},
]
scenes = [ #scenario du jeu
    {"image": "lapinfamille.jpg",
     "texte": "il était une fois une famille de lapins heureuses..."},
    {"image": "lapinkidnapping.jpg", 
     "texte": "Mais un jour, Monsieur Poulet enleva Maman Lapine !"},
    {"image": "lapinlapinedebutjeu.jpg", 
     "texte": "Papa Lapin jura de la retrouver coûte que coûte..."},
]
scene_index = 0 




while running: #lancement du jeu et de la fenetre
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()  # position de la souris
           #mise en place bouton et evenement du menu
            clique_menu = False
            for bouton in boutons:
                if (bouton["x"] < mx < bouton["x"] + bouton["w"] and
                    bouton["y"] < my < bouton["y"] + bouton["h"]):
                    if bouton["texte"] == "Jouer": # chemin du bouton
                        etat = "scenario"
                        scene_index = 0                     
                    elif bouton["texte"] == "Scénario":
                        etat = "scenario_menu" #scenario et retour menu principal
                        scene_index = 0
                    elif bouton["texte"] == "Crédits":
                        etat = "credits"

            if not clique_menu:
                if etat in ("scenario", "scenario_menu"):
                    if 550 < mx < 730 and 555 < my < 595:
                        scene_index += 1
                        if scene_index >= len(scenes):
                            etat = "jeu" if etat == "scenario" else "accueil"
                            scene_index = 0
                    if 60 < mx < 240 and 555 < my < 595:
                        etat = "jeu" if etat == "scenario" else "accueil"
                        scene_index = 0  

                if etat == "credits":
                    if 300 < mx < 500 and 430 < my < 480:
                        etat = "accueil"

            if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE and etat == "credits":
                            etat = "accueil"
        
    fenetre.blit(image_fond_accueil, (0, 0))  #remplir le fond avec image
    fenetre.blit(filtre, (0, 0))
    
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


    if hit_effet > 0: # dessin du halo
        hit_effet -= 1
        alpha = hit_effet / 20 
        surface_rouge = pygame.Surface((800, 600), pygame.SRCALPHA) # defini la taille du halo et la transparence
        pygame.draw.rect(surface_rouge, (255, 0, 0, int(alpha * 180)), (0, 0, 800, 600), 40) # couleur et epaisseur du halo
        fenetre.blit(surface_rouge, (0, 0))


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
       
    elif etat == "jeu": #si on appui sur jouer
        fenetre.blit(image, (lapin_x, lapin_y))    #position de l'image defini plus haut
        temps_actuel = pygame.time.get_ticks()# donne temps écoulé en milliseconde tout comme Date.now()

        touchs = pygame.key.get_pressed()#choix des touches de jeu

        if touchs[pygame.K_LEFT]:#lapin va de 5px a gauche avec la fleche gauche
            lapin_x -= 5
        if touchs[pygame.K_RIGHT]:#lapin va de 5px a droite avec la fleche droite
            lapin_x += 5
        if touchs[pygame.K_SPACE] and temps_actuel - dernier_tir > 400: #lapin tire les balles avec espace et le temps de recharge entre chaque balle et de 0,4 sec
            balles.append({"x": lapin_x + 50, "y": lapin_y})
            dernier_tir = temps_actuel
       

        for balle in balles:#determine les balles
            balle["y"] -= 7 #chaque balle monte de 7px
            pygame.draw.rect(fenetre, (245, 75, 17), (balle["x"], balle["y"], 6, 12)) #taille des balles et trajectoire

        balles = [b for b in balles if b["y"] > 0]# pour que la balle ne sorte pas de la fentre de jeu
        lapin_x = max(0, min(700, lapin_x)) #pour ne pas sortir de la fenetre            
        
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

        if temps_actuel - dernier_champignon > 2000: #champignon toutes les 2 sec mini
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

        if temps_actuel - derniere_carotte > 8000:
            carotte.append({
                "x": random.randint(50, 750),
                "y": -60
            })
            derniere_carotte = temps_actuel

        for c in carotte:
            c["y"] += 2
            fenetre.blit(image_carotte, (c["x"], c["y"]))

        carotte = [c for c in carotte if c["y"] < 600]
                        

        for carottes in carotte: # collision carotte
            if (carottes["x"] < lapin_x + 100 and
                carottes["x"] + 30 > lapin_x and
                carottes["y"] < lapin_y + 100 and
                carottes["y"] + 30 > lapin_y):
                vies = min(vies + 1, 5) #    # ajoute une vie mais pas plus de 5 vie max
                ajouter_float(lapin_x + 50, lapin_y, "+1 vie", (126, 245, 5))
                carotte = [c for c in carotte if c != carottes]


        text_score = font.render(f"score : {score}", True, (255, 255, 255)) #affichage du score
        fenetre.blit(text_score, (10, 10)) #emplacement texte score

        for ennemi in ennemis:
            if ennemi["vivant"] and ennemi["y"] > 600: #verifie si ennemi atteint le bas de la fenetre
                ennemi["vivant"] = False #si atteind le bas = ennemi meurt
                vies -=1 #si atteind le bas joueur perd 1 vie


        for ennemi in ennemis:#affichage des ennemis dans la fenetre de jeu
            if ennemi["vivant"]:
                if ennemi["type"] == "poulet":
                    fenetre.blit(image_ennemi, (ennemi["x"], ennemi["y"]))
                elif ennemi["type"] == "cloche":
                    fenetre.blit(image_ennemi1, (ennemi["x"], ennemi["y"]))
                elif ennemi["type"] == "oeuf":
                    fenetre.blit(image_ennemi2, (ennemi["x"], ennemi["y"]))
        
        for ennemi in ennemis: #deplacement des ennemis
            if ennemi["vivant"]:
                ennemi["y"] += 0.4 #vitesse de descente des ennemi en Y "verticale" à modifier celon les niveaux

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



        if vies <= 0: #verifie si vie arrive a 0
            texte_go = font.render("GAME OVER", True, (255, 0, 0)) #texte affiche si vie arrive a 0
            x = (800 - texte_go.get_width()) // 2 
            fenetre.blit(texte_go, (x, 300)) #emplacement fenetre GAME OVER
            pygame.display.flip()
            pygame.time.wait(3000) #attend 3 sec
            #reinitialise tout
            score = 0
            vies = 3
            lapin_x = 350
            balles = []
            ennemis = creer_ennemis("ligne", 3)
            champignons = []        
            carotte = []            
            dernier_champignon = 0  
            derniere_carotte = 0
            etat = "accueil" #jeu redemarre à accueil
            
    
        texte_vies = font_emoji.render("❤️" * vies, True, (255, 0, 0)) #affichage des vie avec police compatible emojis
        fenetre.blit(texte_vies, (650, 10)) #emplacement de l'affichage des vie    
        
    elif etat in ("scenario", "scenario_menu"):
        scene = scenes[scene_index]
        img_scene = pygame.image.load(scene["image"])
        img_scene = pygame.transform.scale(img_scene, (800, 600))
        fenetre.blit(img_scene, (0, 0))
        fenetre.blit(filtre, (0, 0))

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

        # boutons suivant et passer
        pygame.draw.rect(fenetre, (218, 237, 225), (550, 555, 180, 40), border_radius=8)
        t_suiv = font_float.render("Suivant", True, (9, 79, 35))
        fenetre.blit(t_suiv, (555, 563))

        pygame.draw.rect(fenetre, (218, 237, 225), (60, 555, 180, 40), border_radius=8)
        t_pass = font_float.render("Passer", True, (9, 79, 35))
        fenetre.blit(t_pass, (65, 563))

    elif etat == "credits":
        texte_c = font.render("🐰 Easter Invaders 🐰", True, (99, 235, 149))
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
     

    

pygame.quit()



