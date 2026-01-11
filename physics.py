#imports
import pygame
import math
import numpy as np
import matplotlib.pyplot as plot
#----------------------------------

#physical constants
G = 6.67e-11
SBC = 5.67e-8
c = 299792458
#---------------------------------------------------

def gravField(pos, center_obj):
    r = pos - center_obj.pos
    radius = r.length()

    if(radius == 0):
        return pygame.Vector2(0,0)
    
    return -G*center_obj.mass*r/radius**3

def hill_radius(prim_obj, sec_obj):
    a = (sec_obj.pos - prim_obj.pos).length()
    mT = prim_obj.mass + sec_obj.mass

    return a*(sec_obj.mass/(3*mT))**(1/3)
