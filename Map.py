import pygame as pg
import Bloc



# 1280*720
class Map:
    """
    Classe Map
    """

    def __init__(self, screen, cvsFile):
        """
        Constructeur de la classe Map
        :param cvsFile: chemin du fichier csv
        :param resolution: tuple (x,y) de la résolution de la map
        :param screen: écran sur lequel on dessine la map
        :return: None
        """


        self.screen = screen
        self.initFromCsv(cvsFile)



    def initFromCsv(self, cvsFile):
        """
        Initialise la matrice de blocs à partir d'un fichier csv, case vide = 0, case pleine = Objet Bloc
        :param cvsFile: chemin du fichier csv
        :return: None
        """

        # TODO variable à mettre dans un fichier variable d'environnement
        HAUTEUR_BLOC = 25
        LARGEUR_BLOC = 25


        # lecture du fichier csv
        nbLigne = 0
        # Ouverture du fichier en lecture seule, en mode texte
        file = open(cvsFile, "r")
        # Récupération de la liste des lignes du fichier dans une liste
        lignes = file.read().split("\n")
        # supression de la dernière ligne vide
        lignes.pop()

        # Initialisation de la matrice de blocs avec le bon nombre de lignes en fonction du csv
        self.blocs = [[] for i in range(lignes.__len__())]

        # On récupère chaque éléments des lignes et on les transforme en entier
        for ligne in lignes:
            line = ligne.split(",")
            for i in range(len(line)):
                line[i] = int(line[i])
            self.blocs[nbLigne] = line
            nbLigne += 1
        # fermeture du fichier
        file.close()

        # Parcours de la matrice pour créer les blocs chaque 1 est remplaçé par un bloc
        x = 0
        while x < self.blocs[0].__len__():
            j = 0
            while j < self.blocs.__len__():
                if self.blocs[j][x] == 1:
                    self.blocs[j][x] = Bloc.Bloc(x * HAUTEUR_BLOC, j * LARGEUR_BLOC)
                j += 1
            x += 1




    def draw(self):
        """
        Dessine la map sur l'écran screen, pour chaque bloc de la matrice on appelle la méthode draw de la classe Bloc
        :return:
        """
        for ligne in self.blocs:
            for bloc in ligne:
                if (bloc != 0):
                    bloc.draw(self.screen)

