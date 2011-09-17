'''
Created on Sep 13, 2011

@author: deadguy
'''
from os import pardir
from os.path import join

from pygame.image import load
from pygame import error

def load_png(name):
    fullname = join(pardir, 'data', name)
    try:
        image = load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except error, e:
        print "Can't load ", fullname
        raise SystemExit, e
    return image, image.get_rect()
