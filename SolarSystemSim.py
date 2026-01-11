
#imports
import pygame
import math
import numpy as np
import sys
import matplotlib.pyplot as plot
from gameui import *
from objects import *
#---------------------------------------------------
#pygame initializations
pygame.init()

screen = pygame.display.set_mode((2000,1000), pygame.RESIZABLE)
screen_rect = screen.get_rect()
pygame.display.set_caption("Solar System Simulator")

clock = pygame.time.Clock()

dt = 1e-8
prev_dt = dt
#----------------------------------------------------------------------------------------------------------------------------------------------------
#object initializations
sun = Star("Sun", (1000,500), "yellow", 100, 1.2e30, dt)
# rigel = ob.Star("Rigel", (-10000,200), "light blue", 7900, 3.58e31, dt)
# sirius = ob.Star("Sirius", (-500,-500), "white", 171, 4.02e30, dt)
# betelgeuse = ob.Star("Betelgeuse", (-1000000,-500), (255,100,0), 76400, 2.78e31, dt)
# vega = ob.Star("Vega", (0,5500), "light blue", 236, 4.01e30, dt)
# polaris = ob.Star("Polaris", (2200,2200), "light yellow", 3750, 1.09e31, dt)
# proxima_centauri = ob.Star("P Centauri", (100,0), "red", 14, 2.45e29, dt)
# antares = ob.Star("Antares", (1000000,0), "red", 88300, 1.3e31, dt)

earth = Planet("Earth", (3700,500), "teal", 9, 5.97e24, dt, star=sun)
venus = Planet("Venus", (3050,500), (200, 150, 0), 8, 4.87e24, dt, star=sun)
mars = Planet("Mars", (4400,500), "red", 4, 6.42e23, dt, star=sun)
mercury = Planet("Mercury", (2200,500), "gray", 2, 3.3e23, dt, star=sun)
jupiter = Planet("Jupiter", (6300,500), "orange", 20, 1.9e27,  dt, star=sun)
saturn = Planet("Saturn", (7600,500), "tan", 18, 5.68e26,  dt, star=sun)
uranus = Planet("Uranus", (8500,500), "light blue", 15, 8.68e25, dt, star=sun)
neptune = Planet("Neptune", (10000,500), "blue", 14, 1.02e26, dt, star=sun)

moon = Moon("Moon", (3720,500), "gray", 2, 7.35e22, dt, planet=earth)
ganymede = Moon("Ganymede", (6550, 500), (152,133,88), 3, 1.48e23, dt, planet=jupiter)
io = Moon("Io", (6350, 500), (255,204, 102), 2, 8.93e22, dt, planet=jupiter)
europa = Moon("Europa", (6450, 500), (210,212,200), 2, 4.8e22, dt, planet=jupiter)
callisto = Moon("Callisto", (6650, 500), (110, 100, 90), 3, 1.08e23, dt, planet=jupiter)
phobos = Moon("Phobos", (4425,500), (150,120,100), 1, 1.07e16, dt, planet = mars)
deimos = Moon("Deimos", (4470,500), (170, 140, 110), 1, 1.48e15, dt, planet=mars)

initBackgroundStars(screen, 100)

star_data = [
    {"type": Star, "name": "Sun", "color": "yellow", "radius": 100, "mass": 1.2e30},
    {"type": Star, "name": "Rigel", "color": "light blue", "radius": 7900, "mass": 3.58e31},
    {"type": Star, "name": "Sirius", "color": "white", "radius": 171, "mass": 4.02e30},
    {"type": Star, "name": "Betelgeuse", "color": (255,100,0), "radius": 76400, "mass": 2.78e31},
    {"type": Star, "name": "Vega", "color": "light blue", "radius": 236, "mass": 4.01e30},
    {"type": Star, "name": "Polaris", "color": "light yellow", "radius": 3750, "mass": 1.09e31},
    {"type": Star, "name": "P Centauri", "color": "red", "radius": 14, "mass": 2.45e29},
    {"type": Star, "name": "Antares", "color": "red", "radius": 88300, "mass": 1.3e31},
    {"type": Star, "name": "Aldebaran", "color": "orange", "radius": 4400, "mass": 2.5e30},
    {"type": Star, "name": "Pollux", "color": "orange", "radius": 900, "mass": 1.9e30},
    {"type": Star, "name": "Spica", "color": (240,255,240), "radius": 700, "mass": 2.2e31},
    {"type": Star, "name": "Fomalhaut", "color": "white", "radius": 190, "mass": 4.2e30},
    {"type": Star, "name": "Deneb", "color": "white", "radius": 20000, "mass": 4e31},
    {"type": Star, "name": "Alnitak", "color": (200,200,255), "radius": 2000, "mass": 3.3e31},
    {"type": Star, "name": "Regulus", "color": "light blue", "radius": 360, "mass": 7.9e30},
    {"type": Star, "name": "Capella", "color": "yellow", "radius": 1200, "mass": 5.4e30}
]

planet_data = [
    {"type": Planet, "name": "Mercury", "color": "gray", "radius": 2, "mass": 3.3e23},
    {"type": Planet, "name": "Venus", "color": (200, 150, 0), "radius": 8, "mass": 4.87e24},
    {"type": Planet, "name": "Earth", "color": "teal", "radius": 9, "mass": 5.97e24},
    {"type": Planet, "name": "Mars", "color": "red", "radius": 4, "mass": 6.42e23},
    {"type": Planet, "name": "Jupiter", "color": "orange", "radius": 20, "mass": 1.9e27},
    {"type": Planet, "name": "Saturn", "color": "tan", "radius": 18, "mass": 5.68e26},
    {"type": Planet, "name": "Uranus", "color": "light blue", "radius": 15, "mass": 8.68e25},
    {"type": Planet, "name": "Neptune", "color": "blue", "radius": 14, "mass": 1.02e26},
    {"type": Planet, "name": "51 Pegasi b", "color": (255,213,128), "radius": 117, "mass": 1.2e30},
    {"type": Planet, "name": "HD 209458 b", "color": (204,204,255), "radius": 117, "mass": 1.2e30},
    {"type": Planet, "name": "Gliese 581g", "color": "brown", "radius": 14, "mass": 1.2e30},
    {"type": Planet, "name": "Kepler 22 b", "color": (175,238,238), "radius": 22, "mass": 1.2e30},
    {"type": Planet, "name": "TRAPPIST 1 e", "color": (122,106,79), "radius": 9, "mass": 1.2e30},
    {"type": Planet, "name": "GJ 1214 b", "color": (176,196,222), "radius": 24, "mass": 1.2e30},
    {"type": Planet, "name": "WASP-12 b", "color": (10,10,10), "radius": 162, "mass": 1.2e30},
    {"type": Planet, "name": "CoRoT-7 b", "color": (255,36,0), "radius": 15, "mass": 1.2e30}
]

moon_data = [
    {"type": Moon, "name": "Moon", "color": "gray", "radius": 2, "mass": 7.35e22},
    {"type": Moon, "name": "Ganymede", "color": (152, 133, 88), "radius": 3, "mass": 1.48e23},
    {"type": Moon, "name": "Europa", "color": (210, 212, 200), "radius": 2, "mass": 4.80e22},
    {"type": Moon, "name": "Callisto", "color": (110, 100, 90), "radius": 3, "mass": 1.08e23},
    {"type": Moon, "name": "Io", "color": (255, 204, 102), "radius": 2, "mass": 8.93e22},
    {"type": Moon, "name": "Titan", "color": (205, 173, 0), "radius": 3, "mass": 1.35e23},
    {"type": Moon, "name": "Enceladus", "color": (220, 220, 255), "radius": 1, "mass": 1.08e20},
    {"type": Moon, "name": "Triton", "color": (190, 200, 255), "radius": 2, "mass": 2.14e22},
    {"type": Moon, "name": "Phobos", "color": (150, 120, 100), "radius": 1, "mass": 1.07e16},
    {"type": Moon, "name": "Deimos", "color": (170, 140, 110), "radius": 1, "mass": 1.48e15},
    {"type": Moon, "name": "Rhea", "color": (200, 200, 180), "radius": 2, "mass": 2.31e21},
    {"type": Moon, "name": "Iapetus", "color": (130, 120, 110), "radius": 2, "mass": 1.81e21},
    {"type": Moon, "name": "Dione", "color": (210, 210, 210), "radius": 2, "mass": 1.10e21},
    {"type": Moon, "name": "Miranda", "color": (160, 160, 170), "radius": 1, "mass": 6.59e19},
    {"type": Moon, "name": "Charon", "color": (180, 170, 160), "radius": 2, "mass": 1.52e21},
    {"type": Moon, "name": "Mimas", "color": (180, 180, 180), "radius": 1, "mass": 3.75e19}
]

dwarf_asteroid_data = [
    {"type": Planet, "name": "Ceres", "color": (200, 200, 200), "radius": 3, "mass": 9.4e20},
    {"type": Planet, "name": "Pluto", "color": (220, 210, 200), "radius": 4, "mass": 1.31e22},
    {"type": Planet, "name": "Haumea", "color": (190, 190, 190), "radius": 3, "mass": 4.01e21}, 
    {"type": Planet, "name": "Makemake", "color": (210, 190, 180), "radius": 3, "mass": 3.1e21},
    {"type": Planet, "name": "Eris", "color": (230, 230, 240), "radius": 4, "mass": 1.67e22},          

    {"type": Moon, "name": "Vesta", "color": (150, 150, 140), "radius": 2, "mass": 2.6e20},   
    {"type": Moon, "name": "Pallas", "color": (160, 160, 160), "radius": 2, "mass": 2.1e20},   
    {"type": Moon, "name": "Hygiea", "color": (170, 170, 170), "radius": 2, "mass": 8.6e19},   
    {"type": Moon, "name": "Quaoar", "color": (180, 170, 160), "radius": 3, "mass": 1.3e21},         
    {"type": Moon, "name": "Orcus", "color": (140, 130, 120), "radius": 3, "mass": 6.3e20}
]


#--------------------------------------------------------------------------------------------------------------------
#Button action definitions
def zoom_in():
    global zoom
    zoom = min(zoom*1.1, 50)

def zoom_out():
    global zoom
    zoom = max(zoom/1.1, 0.001)

def resume_sim():
    global dt, prev_dt
    dt = prev_dt if prev_dt != 0 else 1e-8
    for e in entities:
        e.dt = prev_dt if prev_dt !=0 else 1e-8
    game_menu.rect.topleft = game_menu.pos
    settings_menu.rect.topleft = settings_menu.pos
    game_menu.vis = False
    settings_menu.vis = False

def quit_game():
    pygame.quit()
    sys.exit()

def open_settings():
    game_menu.rect.topleft = game_menu.pos
    settings_menu.rect.center = screen_rect.center
    game_menu.vis = False
    settings_menu.vis = True

def back_settings():
    game_menu.vis = True 
    settings_menu.vis = False
    game_menu.rect.center = screen.get_rect().center

def clear_sim():
    global dt
    entities.clear()
    for menu in menus:
        menu.rect.topleft = menu.pos
        menu.vis = False
    zoom_in_button.rect.x = zoom_out_button.rect.x = zoom_x_i
    dt = 1e-8

def add_object(obj_type, name, color, radius, mass):
    global zoom, cam_x, cam_y, dt, object_attached, attached_object, obj_mass
    new_obj = obj_type(name, (0,0), color, radius, 0, 0)
    obj_mass = mass
    attached_object = new_obj
    object_menu.rect.left = screen.get_size()[0]
    object_menu.vis = False
    object_attached = True
    zoom_in_button.rect.x = zoom_out_button.rect.x = zoom_x_i

       
#-------------------------------------------------------------------
#camera initializations
cam_x, cam_y = 1000, 500
zoom = 1
dx = 0.1

isDragging = False
drag_start = pygame.Vector2(0,0)
cam_start = pygame.Vector2(cam_x,cam_y)

overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
overlay.fill((0,0,0,150))

object_attached = False
attached_object = None

#object menu initializations------------------------------------------------------------------------------------------------------------------
object_menu = Menu("object menu", (500,2000),(500,1000), (50,50,50), screen, TL=screen_rect.topright, border_radius=0)
object_menu.add_text("Object Menu", "consolas", 40, "white", center=(250,40))
object_menu.add_text("Stars", "consolas", 30, "white", topleft=(25,125), underline=True)
object_menu.add_text("Planets", "consolas", 30, "white", topleft=(25,550), underline=True)
object_menu.add_text("Moons", "consolas", 30, "white", topleft=(25,1025), underline=True)
object_menu.add_text("Dwarf Planets & Asteroids", "consolas", 30, "white", topleft=(25,1450), underline=True)

star_buttons = []
planet_buttons = []
moon_buttons = []
dp_a_buttons = []
d,q = 0,0
for a_data in dwarf_asteroid_data:
    dp_a_buttons.append(Button(
        (100,100), (20+d, 1500+q), a_data["name"], "consolas", 25, "white", "black", Menu=object_menu,
        object_display_data={"color": a_data["color"], "radius": a_data["radius"]},
        action=lambda data=a_data: add_object(data["type"], data["name"], data["color"], data["radius"], data["mass"])))
    if(d<380):
        d+=120
    else:
        d=0
        q=150
d,q = 0,0
for s_data, p_data, m_data in zip(star_data, planet_data, moon_data):
    star_buttons.append(Button(
        (100,100), (20+d, 175+q), s_data["name"], "consolas", 25, "white", "black", Menu=object_menu,
        object_display_data={"color": s_data["color"], "radius": s_data["radius"]},
        action=lambda data=s_data: add_object(data["type"], data["name"], data["color"], data["radius"], data["mass"])))
    planet_buttons.append(Button(
        (100,100), (20+d, 600+q), p_data["name"], "consolas", 25, "white", "black", Menu=object_menu,
        object_display_data={"color": p_data["color"], "radius": p_data["radius"]},
        action=lambda data=p_data: add_object(data["type"], data["name"], data["color"], data["radius"], data["mass"])))
    moon_buttons.append(Button(
        (100,100), (20+d, 1075+q), m_data["name"], "consolas", 25, "white", "black", Menu=object_menu,
        object_display_data={"color": m_data["color"], "radius": m_data["radius"]},
        action=lambda data=m_data: add_object(data["type"], data["name"], data["color"], data["radius"], data["mass"])))
    if(d<740):
        d+=120
    else:
        d=0
        q=150

star_slide_button = Slide_Button((100,25), (25, 480), "white", star_buttons, Menu=object_menu, container=(object_menu.surface, (30,30,30), pygame.Rect(25,480, 450,25)))
planet_slide_button = Slide_Button((100,25), (25, 905), "white", planet_buttons, Menu=object_menu, container=(object_menu.surface, (30,30,30), pygame.Rect(25,905, 450,25)))
moon_slide_button = Slide_Button((100,25), (25,1380), "white", moon_buttons, Menu=object_menu, container=(object_menu.surface, (30,30,30), pygame.Rect(25,1380, 450,25)))
dp_a_slide_button = Slide_Button((100,25), (25,1805), "white", dp_a_buttons, Menu=object_menu, container=(object_menu.surface, (30,30,30), pygame.Rect(25,1805, 450,25)))
object_menu.add_buttons(*star_buttons, *planet_buttons, *moon_buttons, *dp_a_buttons, star_slide_button, planet_slide_button, moon_slide_button, dp_a_slide_button)


#system menu initializations
system_menu = Menu("settings menu", (500, 1000),(500,1000), (50,50,50), screen, TL=screen_rect.topright, border_radius=0)
system_menu.add_text("Systems", "consolas", 40, "white", (250,40))

#game menu initializations
game_menu = Menu("game menu", (800,800),(800,800), (50,50,50), screen, C=(screen_rect.centerx, screen_rect.bottom+400))
game_menu.add_text("Game Menu", "consolas", 40, "white", (400,50))
resume_button = Button((200,50), (300,95), "Resume", "consolas", 30, "black", "white", Menu=game_menu, action=resume_sim)
quit_button = Button((200,50), (300,305), "Quit Game", "consolas", 30, "black", "white", Menu=game_menu, action=quit_game)
settings_button = Button((200,50), (300,165), "Settings", "consolas", 30, "black", "white", Menu=game_menu, action=open_settings)
new_sim_button = Button((200,50), (300,235), "Start New Sim", "consolas", 30, "black", "white", Menu=game_menu, action=clear_sim)
game_menu.add_buttons(resume_button, quit_button, settings_button, new_sim_button)

#settings menu initializations
settings_menu = Menu("settings menu", (800,800),(800,800), (50,50,50), screen, C=(screen_rect.centerx, screen_rect.bottom+400))
settings_menu.add_text("Settings", "consolas", 40, "white", (400,50))
back_button = Button((200,50), (300,95), "Back", "consolas", 30, "black", "white", Menu=settings_menu, action=back_settings)
settings_menu.add_buttons(back_button)

#button initializations
zoom_in_button = Button((50,50), (1940, 880), "+", "consolas", 40, "black", "white", surface=screen, action=zoom_in)
zoom_out_button = Button((50,50), (1940, 940), "-", "consolas", 40, "black", "white", surface=screen, action=zoom_out)
zoom_x_i = zoom_in_button.rect.x

TOV_button = Button((130,40), (15,71), "Toggle Obj Vis", "consolas", 20, "white", "white", surface=screen, border_width=2, action=toggle_obj_vis)


#GAME LOOP--------------------------------------------------
while True:

    screen.fill("black")
    screen_size = screen.get_size()

    #event handler
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            pygame.quit()
            sys.exit()
       
        #use for all button clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (event.button == 2 and not game_menu.vis and not settings_menu.vis):
                isDragging = True
                drag_start = pygame.Vector2(pygame.mouse.get_pos())
                cam_start = pygame.Vector2(cam_x, cam_y)

            zoom_in_button.leftclick(event)
            zoom_out_button.leftclick(event)
            TOV_button.leftclick(event)

            if game_menu.vis:
                resume_button.leftclick(event)
                quit_button.leftclick(event)
                settings_button.leftclick(event)
                new_sim_button.leftclick(event)
            elif settings_menu.vis:
                back_button.leftclick(event)
            elif object_menu.vis:
                for b in object_menu.buttons:
                    b.leftclick(event)
            
            if object_attached and event.button == 3:
                delete_entity(attached_object)
            
            for menu in menus:
                if not menu.rect.collidepoint(pygame.mouse.get_pos()):
                    for e in entities:
                        e.select(event, zoom)
            for mm in mini_menus:
                for b in mm.buttons:
                    b.leftclick(event)


        if event.type == pygame.MOUSEMOTION:
            if isDragging:
                mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
                delta = (drag_start - mouse_pos) / zoom
                cam_x = cam_start.x + delta.x
                cam_y = cam_start.y + delta.y
            
            if object_attached:
                mx, my = pygame.mouse.get_pos()
                world_x = (mx - 1000) / zoom + cam_x
                world_y = (my - 500) / zoom + cam_y
                attached_object.pos = pygame.Vector2(world_x, world_y)
            
            for b in object_menu.buttons:
                if isinstance(b, Slide_Button):
                    b.leftclick(event)
        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 2:
                isDragging = False
            
            if event.button == 1:
                if attached_object is not None:
                    attached_object.dt = dt
                    attached_object.mass = obj_mass
                    attached_object = None
                object_attached = False
            
            for b in object_menu.buttons:
                if isinstance(b, Slide_Button):
                    b.leftclick(event)
        
        if(event.type == pygame.MOUSEWHEEL and (not game_menu.vis and not system_menu.vis)):
            if(not object_menu.rect.collidepoint(pygame.mouse.get_pos()) and not system_menu.rect.collidepoint(pygame.mouse.get_pos())):
                mx, my = pygame.mouse.get_pos()
                world_x_before = (mx - 1000) / zoom + cam_x
                world_y_before = (my - 500) / zoom + cam_y

                zoom *= 1.1 ** event.y
                zoom = max(0.001, min(zoom, 50))

                world_x_after = (mx - 1000) / zoom + cam_x
                world_y_after = (my - 500) / zoom + cam_y

                cam_x += world_x_before - world_x_after
                cam_y += world_y_before - world_y_after
            
            if(object_menu.rect.collidepoint(pygame.mouse.get_pos())):
                object_menu.scroll -= event.y*100

      

        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_SPACE and (not game_menu.vis or not settings_menu.vis)):
                if(dt != 0):
                    prev_dt = dt
                    dt = 0
                    for e in entities:
                        e.dt = 0
                else:
                    dt = prev_dt if prev_dt != 0 else 1e-8
                    for e in entities:
                        e.dt = prev_dt if prev_dt != 0 else 1e-8
                    
            if(event.key == pygame.K_ESCAPE):
                if(not game_menu.vis and not settings_menu.vis):
                    game_menu.rect.center = screen_rect.center
                    prev_dt = dt
                    dt = 0
                    for e in entities:
                        e.dt = 0
                    game_menu.vis = True
                
                elif(settings_menu.vis):
                    back_settings()
                elif(game_menu.vis):
                    resume_sim()
                    
            if(event.key == pygame.K_c):
                zoom = 1
                cam_x,cam_y = 1000,500
               
            if(event.key == pygame.K_RIGHT):
                dt*=2
                for e in entities:
                    e.dt *= 2
            if(event.key == pygame.K_LEFT):
                dt/=2
                for e in entities:
                    e.dt /= 2

            if(event.key == pygame.K_m):
                if(system_menu.vis):
                    system_menu.rect.topleft = (screen.get_size()[0], 0)

                    system_menu.vis = False
                if(not object_menu.vis):
                    object_menu.rect.topright = (screen.get_size()[0],0)
                    
                    min_zoom = zoom_x_i - object_menu.rect.width
                    zoom_in_button.rect.x = zoom_out_button.rect.x = max(min_zoom, zoom_in_button.rect.x - object_menu.rect.width)

                    object_menu.vis = True
                else:
                    object_menu.rect.topleft = (screen.get_size()[0], 0)
                    zoom_in_button.rect.x = zoom_out_button.rect.x = zoom_x_i
                    object_menu.vis = False
                    
            if(event.key == pygame.K_r):
                if(object_menu.vis):
                    object_menu.rect.topleft = (screen.get_size()[0], 0)
                    object_menu.vis = False
                if(not system_menu.vis):
                    system_menu.rect.topright = (screen.get_size()[0],0)

                    min_zoom = zoom_x_i - system_menu.rect.width
                    zoom_in_button.rect.x = zoom_out_button.rect.x = max(min_zoom, zoom_in_button.rect.x - system_menu.rect.width)
                    system_menu.vis = True
                else:
                    system_menu.rect.topleft = (screen.get_size()[0], 0)
                    zoom_in_button.rect.x = zoom_out_button.rect.x = zoom_x_i
                    system_menu.vis = False
            
            if(event.key == pygame.K_i):
                for e in entities:
                    if e.info_menu and e.info_menu.vis:
                        e.info_menu.rect.topleft = screen_rect.topright
                        e.info_menu.vis = False

            if(event.key == pygame.K_DELETE):
                for e in entities:
                    if e.isSelected:
                        delete_entity(e)

        if(event.type == pygame.VIDEORESIZE):
            diffx = event.size[0] - screen_size[0]
            diffy = event.size[1] - screen_size[1]
            object_menu.rect.topright = (object_menu.rect.topright[0]+diffx, 0)
            system_menu.rect.topright = (system_menu.rect.topright[0]+diffx, 0)
            size = event.size
            initBackgroundStars(screen, 100)

    for menu in menus:
        if(menu.rect.collidepoint(pygame.mouse.get_pos())):
            isDragging = False

    keys = pygame.key.get_pressed()
    cam_speed = 200/zoom
    if(keys[pygame.K_w]):
        cam_y -= cam_speed*dx
    if(keys[pygame.K_s]):
        cam_y += cam_speed*dx
    if(keys[pygame.K_d]):
        cam_x += cam_speed*dx
    if(keys[pygame.K_a]):
        cam_x -= cam_speed*dx


    # sun.create(screen, cam_x, cam_y, zoom)

    # for p in planets:
    #     p.create(screen, cam_x, cam_y, zoom)

    for e in entities:
        e.create(screen, cam_x, cam_y, zoom)
    
    zoom_in_button.create()
    zoom_out_button.create()
    TOV_button.create()
    font = pygame.font.SysFont("consolas", 20)
    zoom_text = font.render(f"Zoom: {zoom:.3f}x", True, "white")
    screen.blit(zoom_text, (15, 43))

    fps = clock.get_fps()
    fps_text = font.render(f"FPS: {fps:.1f}", True, "white")
    screen.blit(fps_text, (15, 15))

    for menu in menus:
        menu.create()

    if(game_menu.vis):
        screen.blit(overlay, (0,0))
        game_menu.create()
    
    if(settings_menu.vis):
        screen.blit(overlay, (0,0))
        settings_menu.create()
       
    pygame.display.update()
    clock.tick(60)
    #---------------------------------------------------------------------