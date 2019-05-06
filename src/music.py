import pygame
playlist = list()
playlist.append ( "/Users/eforgacs/PycharmProjects/DragonWarrior_clone/data/02_-_Dragon_Warrior_-_NES_-_Chateau_Ladutorm.ogg" )


pygame.mixer.music.load ( playlist.pop() )
pygame.mixer.music.queue ( playlist.pop() )
pygame.mixer.music.set_endevent ( pygame.USEREVENT )
pygame.mixer.music.play()