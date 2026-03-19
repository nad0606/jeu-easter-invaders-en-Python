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

import random
import pygame
pygame.init()

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
#liste des 3 ennemies et leur position et type
ennemis = [{"x": 100, "y": 50, "vivant": True, "type": "poulet"}, {"x": 300, "y": 50, "vivant": True, "type": "cloche"}, {"x": 500, "y": 50, "vivant": True, "type": "oeuf"} ]
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

def ajouter_float(x, y, texte, couleur): # faire des textes flottants
    floats.append({
        "x": x, "y": y,
        "texte": texte, # choix du text
        "couleur": couleur, #choix couleur
        "alpha": 400, # transparence
        "vy": -1 # vitesse de montée
    })


while running: #lancement du jeu et de la fenetre
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and etat == "accueil":
                etat = "jeu"
    
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
        texte = font.render("EASTER INVADERS", True, (156, 237, 74))#texte 1
        x = (800 - texte.get_width()) // 2 # larguer de la fenetre - largeur du texte pour centrer le texte
        fenetre.blit(texte, (x, 200)) # emplacement du texte 1 centré
        texte2 = font_texte2.render("Appuie sur ENTER pour jouer !", True, (255, 255, 255)) # text 2
        x = (800 - texte2.get_width()) // 2 
        fenetre.blit(texte2, (x, 300)) #emplacement texte 2

    elif etat == "jeu":

        
        fenetre.blit(image, (lapin_x, lapin_y))#position de l'image defini plus haut
        
        temps_actuel = pygame.time.get_ticks() # donne temps écoulé en milliseconde tout comme Date.now()

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
                            ajouter_float(ennemi["x"], ennemi["y"], "+ 100 points", (126, 245, 5))
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
                print(f"Tireur : {tireur['type']} x={tireur['x']}")
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
            texte_niveau = font.render(f"Niveau {niveau} !", True, (48, 117, 74))
            x = (800 - texte_niveau.get_width()) // 2 
            fenetre.blit(texte_niveau, (x, 300))
            pygame.display.flip()
            pygame.time.wait(2000)
            ennemis = [] #reinitialise les ennemis en rajoutant 1 de plus à chaque niveau
            for i in range(niveau + 2): #ajoute des ennemis à chaque niveau
                ennemis.append({"x": 80 + i * 100, "y": 50, "vivant": True, "type": types[i % 3]}) # alterne entre les 3 ennemis avec modulo



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
            ennemis = [
                {"x": 100, "y": 50, "vivant": True, "type": "poulet"},
                {"x": 300, "y": 50, "vivant": True, "type": "cloche"},
                {"x": 500, "y": 50, "vivant": True, "type": "oeuf"}
                 ]
            etat = "accueil" #jeu redemarre à accueil
            
    
        texte_vies = font_emoji.render("❤️" * vies, True, (255, 0, 0)) #affichage des vie avec police compatible emojis
        fenetre.blit(texte_vies, (650, 10)) #emplacement de l'affichage des vie    

    pygame.display.flip()
    horloge.tick(60)

    

pygame.quit()



