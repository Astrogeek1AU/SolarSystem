#imports
import pygame
import math
import numpy as np
import matplotlib.pyplot as plot
from physics import *
import random
from gameui import *

entities = []
stars = []
planets = []
moons = []

class Entity:
    def __init__(self, name, pos, color, radius, mass, dt):
        self.name = name
        self.pos = pygame.Vector2(pos)
        self.color = color
        self.radius = radius
        self.mass = mass
        self.dt = dt
        self.isSelected = False
        self.screen_x, self.screen_y = 0,0
        entities.append(self)
        self.screen = None
        self.info_menu = None

    
    def create(self, screen, cam_x, cam_y, zoom):
        self.screen_x = (self.pos.x - cam_x) * zoom + 1000
        self.screen_y = (self.pos.y - cam_y) * zoom + 500
        self.screen = screen
        if self.isSelected and hasattr(self, "obj_menu"):
            pygame.draw.circle(screen, "white", (int(self.screen_x), int(self.screen_y)), self.radius*1.2*zoom, width=2)
            self.obj_menu.create(zoom)
        pygame.draw.circle(screen, self.color, (int(self.screen_x), int(self.screen_y)), int(max(1,self.radius*zoom))) if obj_vis else pygame.draw.circle(screen, self.color, (int(self.screen_x), int(self.screen_y)), int(self.radius*zoom))
    
    def select(self, event, zoom):
        self.rect = pygame.Rect(self.screen_x-(self.radius*zoom), self.screen_y-(self.radius*zoom), self.radius*2*zoom, self.radius*2*zoom)
        if event.button == 1 and self.rect.collidepoint(pygame.mouse.get_pos()):
            if (not hasattr(self, "obj_menu") or self.obj_menu not in mini_menus) and self.screen:
                self.obj_menu = Mini_Menu(self, self.screen)
                delete_button = Button((180,30), (10,65), "Delete Object", "consolas", 15, "white", (230,0,0), Menu=self.obj_menu, action= lambda: delete_entity(self))
                info_menu_button = Button((180,30), (10,30), "Info", "consolas", 15, "white", (25,25,25), Menu=self.obj_menu, action= lambda: open_obj_info_menu(self, self.screen))
                self.obj_menu.add_buttons(delete_button, info_menu_button)
            self.isSelected = True
        elif (event.button == 1 and self.isSelected) and (not self.obj_menu.rect.collidepoint(pygame.mouse.get_pos())):
            self.isSelected = False


   
class Star(Entity):
    
    def __init__(self, name, pos, color, radius, mass, dt):
        super().__init__(name, pos, color, radius, mass, dt)
        self.type = "star"
        stars.append(self)


class Planet(Entity):
    
    def __init__(self, name, pos, color, radius, mass, dt, star=None):
        super().__init__(name, pos, color, radius, mass, dt)
        self.type = "planet"

        #Nearest star finder, not needed now, but could have implementation when the system menu is used
        # star_dist = float('inf')
        # if star == None:
        #     for s in stars:
        #         if s.pos.length() < star_dist:
        #             star_dist = s.pos.length()
        #             star = s
        self.star = star
        if star:
            self.rvec = self.pos - star.pos
            self.star_dist = self.rvec.length()
            self.v = pygame.Vector2(0, -math.sqrt(G*star.mass/self.star_dist))
        else:
            self.star_dist = 0
            self.v = pygame.Vector2(0,0)
        self.dt = dt
        planets.append(self)
    
    def create(self, screen, cam_x, cam_y, zoom):
        g=pygame.Vector2(0,0)
        for s in stars:
            g += gravField(self.pos, s)

        self.v += g*self.dt
        self.pos += self.v*self.dt
        super().create(screen, cam_x, cam_y, zoom)

        #Hill radius display, not needed right now but can be toggled
        # if self.star:
        #     screen_x = (self.pos.x - cam_x) * zoom + 1000
        #     screen_y = (self.pos.y - cam_y) * zoom + 500
        #     pygame.draw.circle(screen, "white", (int(screen_x), int(screen_y)), int(hill_radius(self.star, self)*zoom), width=1)

class Moon(Entity):

    def __init__(self, name, pos, color, radius, mass, dt, planet=None):
        super().__init__(name, pos, color, radius, mass, dt)
        self.planet = planet

        #Nearest planet finder, not needed now, but could have implementation when the system menu is used
        # planet_dist = float('inf')
        # if planet == None:
        #     for p in planets:
        #         if p.pos.length() < planet_dist:
        #             planet_dist = p.pos.length()
        #             planet = p
        if planet:
            self.rvec = self.pos - planet.pos
            self.planet_dist = self.rvec.length()
            self.v = pygame.Vector2(0, -math.sqrt(G * planet.mass / self.planet_dist))*math.sqrt(100) + planet.v
            # orbital_speed = math.sqrt(G * planet.mass / self.planet_dist)
            # tangent = pygame.Vector2(-self.rvec.y, self.rvec.x).normalize()
            # self.v = planet.v + tangent * orbital_speed
        else:
            self.planet_dist = 0
            self.v = pygame.Vector2(0,0)
        self.dt = dt
        moons.append(self)
    
    def create(self, screen, cam_x, cam_y, zoom):
        g=pygame.Vector2(0,0)
        # for p in planets:
        #     g += gravField(self.pos, p)
        for s in stars:
            g += gravField(self.pos, s)
        if self.planet:
            g += gravField(self.pos, self.planet)*100

        self.v += g*self.dt
        self.pos += self.v*self.dt

        super().create(screen, cam_x, cam_y, zoom)

#Function definitions
#----------------------------------------------------------------------------------
background_stars = []
obj_vis = False
def initBackgroundStars(screen, numStars):
    num_background_stars = numStars

    for i in range(num_background_stars):
        x = random.randint(0,screen.get_size()[0])
        y = random.randint(0,screen.get_size()[1])
        radius = random.randint(1,2)
        background_stars.append((x, y, radius))

def addBackgroundStars(screen):
    for x, y, radius, in background_stars:
        pygame.draw.circle(screen, "white", (x,y), radius)

def delete_entity(obj):
    if obj in entities:
        entities.remove(obj)

    if obj in stars:
        stars.remove(obj)
    elif obj in planets:
        planets.remove(obj)
    elif obj in moons:
        moons.remove(obj)

    mini_menus[:] = [m for m in mini_menus if m.object != obj]

def toggle_obj_vis():
    global obj_vis
    obj_vis = not obj_vis

def open_obj_info_menu(obj, screen):
    if not obj.info_menu:
        obj_info_menu = Obj_Info_Menu(obj, (500,1000), (500,1000), (50,50,50), screen, TL=screen.get_rect().topright, border_radius=0)
        obj.info_menu = obj_info_menu
    obj.info_menu.rect.topright = screen.get_rect().topright
    obj.info_menu.vis = True

