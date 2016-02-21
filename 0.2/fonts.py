import pygame

pygame.font.init()

ailerons = dict()
for x in range(6,80):
	ailerons[str(x)] = pygame.font.Font("Ailerons-Typeface.ttf" , x)

adamCG = dict()
for x in range(6,120):
	adamCG[str(x)] = pygame.font.Font("ADAM.CG PRO.ttf", x)

fontConsole = dict()
for x in range(6,80):
	fontConsole[str(x)] = pygame.font.Font("Inconsolata-Regular.ttf",x)