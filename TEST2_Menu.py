import pygame
import game

# Initialisation de Pygame
pygame.init()

# Définir les dimensions de la fenêtre
largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Menu Mystère")

# Couleurs
blanc = (255, 255, 255)
noir = (0, 0, 0)

# Classe pour représenter un bouton
class Bouton:
    def __init__(self, x, y, largeur, hauteur, texte, couleur_texte, couleur_fond, action=None):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte
        self.couleur_texte = couleur_texte
        self.couleur_fond = couleur_fond
        self.action = action

    def afficher(self, fenetre):
        pygame.draw.rect(fenetre, self.couleur_fond, self.rect)
        afficher_texte(self.texte, 36, self.rect.centerx, self.rect.centery, self.couleur_texte)

# Classe pour représenter le menu
class Menu:
    def __init__(self):
        self.boutons = []

    def ajouter_bouton(self, bouton):
        self.boutons.append(bouton)

    def afficher(self, fenetre):
        for bouton in self.boutons:
            bouton.afficher(fenetre)

# Fonction pour afficher du texte sur l'écran
def afficher_texte(texte, taille, x, y, couleur):
    police = pygame.font.Font(None, taille)
    texte_surface = police.render(texte, True, couleur)
    texte_rect = texte_surface.get_rect()
    texte_rect.center = (x, y)
    fenetre.blit(texte_surface, texte_rect)

# Créer le menu et les boutons
menu = Menu()
bouton_jouer = Bouton(300, 200, 200, 50, "Jouer", noir, blanc)
bouton_options = Bouton(300, 300, 200, 50, "Options", noir, blanc)

menu.ajouter_bouton(bouton_jouer)
menu.ajouter_bouton(bouton_options)

# Boucle de jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for bouton in menu.boutons:
                    if bouton.rect.collidepoint(event.pos):
                        if bouton.action:
                            bouton.action()


    # Action à effectuer lorsque le bouton "Jouer" est cliqué
    def action_jouer():
        game.Game()  # Exécute la fonction principale du module de jeu


    # Créer le menu et les boutons
    menu = Menu()
    bouton_jouer = Bouton(300, 200, 200, 50, "Jouer", noir, blanc, action_jouer)
    bouton_options = Bouton(300, 300, 200, 50, "Options", noir, blanc)

    menu.ajouter_bouton(bouton_jouer)
    menu.ajouter_bouton(bouton_options)

    # Effacer l'écran
    fenetre.fill(noir)

    # Afficher le titre du jeu
    afficher_texte("Menu Mystère", 64, largeur // 2, 100, blanc)

    # Afficher le menu
    menu.afficher(fenetre)

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
