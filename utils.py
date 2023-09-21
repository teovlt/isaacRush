# utils.py
import pygame, os

def importFolder(path):
    surfaceList = []

    for _, __, imgFiles in os.walk(path):
        for image in imgFiles:
            fullPath = f"{path}/{image}"
            if os.path.splitext(fullPath)[1] == '.png':
                imageSurf = pygame.image.load(fullPath).convert_alpha()
                surfaceList.append(imageSurf)

    return surfaceList