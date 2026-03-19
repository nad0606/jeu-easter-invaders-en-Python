#  Exercice 5 — Les fonctions
# Dans le jeu il y a des dizaines de fonctions : drawPlayer(), shoot(), endGame()... C'est ce qui organise tout le code !
# À faire : Crée une fonction afficher_score qui prend score et vies en paramètres et affiche :
# --- Tableau de bord ---
# Score : 100
# Vies : 3


def affiche_score(score, vies):
    print("--- Tableau de bord ---")
    print(f"Score : {score}")
    print(f"Vies : {vies}")


affiche_score(100, 3)