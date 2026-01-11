#imports
import pygame
import math
import numpy as np
import matplotlib.pyplot as plot
#---------------------------------------------------
menus = []
mini_menus = []
class Menu:
    def __init__(self, name, size, window_size, bgcolor, screen, TL=None, TR=None, C=None, border_radius=10, vis=False):
        self.name = name
        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        self.window = pygame.Surface(window_size, pygame.SRCALPHA)
        self.scroll = 0

        self.bgcolor = bgcolor
        if(TL != None):
            self.rect = self.surface.get_rect(topleft=TL)
        elif(C != None):
            self.rect = self.surface.get_rect(center=C)
        elif(TR != None):
            self.rect = self.surface.get_rect(topright=TR)
        else:
            self.rect = self.surface.get_rect()
        self.pos = self.rect.topleft

        self.text_list = []
        self.text_r_list = []

        self.screen = screen
        self.border_radius = border_radius
        self.vis = vis
        self.buttons = []
        menus.append(self)
        
    def create(self):
        self.surface.fill((0,0,0,0))
        self.window.fill((0,0,0,0))
        pygame.draw.rect(self.screen, self.bgcolor, self.rect, border_radius=self.border_radius)
        for t, tr in zip(self.text_list, self.text_r_list):
            self.surface.blit(t, tr)

        for b in self.buttons:
            b.create()

        self.scroll = max(0, min(self.scroll, self.surface.get_size()[1]/2))
        self.window_rect = pygame.Rect((0, self.scroll), self.window.get_size())
        self.window.blit(self.surface, (0,0), area=self.window_rect)
        self.screen.blit(self.window, self.rect.topleft)
    
    def add_buttons(self, *buttons):
        self.buttons = list(buttons)
    
    def add_text(self, text, font, fontsize, textcolor, center=None, topleft=None, topright=None, bottomleft=None, bottomright=None, midtop=None, bold=False, italics=False, underline=False):
        font = pygame.font.SysFont(font, fontsize)
        font.set_bold(bold)
        font.set_italic(italics)
        font.set_underline(underline)
        text = font.render(text, True, textcolor)
        if(center):
            text_r = text.get_rect(center=center)
        elif(topleft):
            text_r = text.get_rect(topleft=topleft)
        elif(topright):
            text_r = text.get_rect(topright=topright)
        elif(bottomleft):
            text_r = text.get_rect(bottomleft=bottomleft)
        elif(bottomright):
            text_r = text.get_rect(bottomright=bottomright)
        elif(midtop):
            text_r = text.get_rect(midtop=midtop)
        self.text_list.append(text)
        self.text_r_list.append(text_r)

class Obj_Info_Menu(Menu):

    def __init__(self, obj, size, window_size, bgcolor, screen, TL=None, TR=None, C=None, border_radius=10, vis=False):
        super().__init__(f"{obj.name} Menu", size, window_size, bgcolor, screen, TL=TL, TR=TR, C=C, border_radius=border_radius, vis=vis)
        self.object = obj
        self.add_text(f"{obj.name} Menu", "consolas", 30, "white", midtop=(size[0]/2, 15), underline=True)
        self.model_bg = pygame.Surface((size[0],size[1]*.3))
        self.model_rect = self.model_bg.get_rect(topleft=(0,60))
        self.model_bg.fill((0,0,0))
    
    def create(self):
        self.surface.fill((0,0,0,0))
        self.window.fill((0,0,0,0))
        pygame.draw.rect(self.screen, self.bgcolor, self.rect, border_radius=self.border_radius)
        for t, tr in zip(self.text_list, self.text_r_list):
            self.surface.blit(t, tr)

        for b in self.buttons:
            b.create()

        self.surface.blit(self.model_bg, self.model_rect)
        pygame.draw.rect(self.surface, "white", self.model_rect, width=2)
        pygame.draw.circle(self.model_bg, self.object.color, self.model_bg.get_rect().center, self.model_rect.height/2*.9)
        self.scroll = max(0, min(self.scroll, self.surface.get_size()[1]/2))
        self.window_rect = pygame.Rect((0, self.scroll), self.window.get_size())
        self.window.blit(self.surface, (0,0), area=self.window_rect)
        self.screen.blit(self.window, self.rect.topleft)

class Mini_Menu:
    def __init__(self, obj, screen, border_radius=10):
        self.screen = screen
        self.surface = pygame.Surface((200,150), pygame.SRCALPHA)
        self.object = obj
        self.border_radius = border_radius
        self.bgcolor = (50,50,50)
        font = pygame.font.SysFont("consolas", 20)
        self.text = font.render(obj.name, True, "white")
        self.text_rect = self.text.get_rect(midtop=(100,5))
        self.rect = self.surface.get_rect(topleft=(self.object.screen_x+self.object.radius+10, self.object.screen_y+self.object.radius+10))
        self.buttons = []
        mini_menus.append(self)

        self.scroll = 0
    
    def create(self, zoom):
        self.surface.fill((0,0,0,0))
        self.rect = self.surface.get_rect(topleft=(self.object.screen_x+self.object.radius*zoom+10, self.object.screen_y+self.object.radius*zoom+10))
        self.surface.blit(self.text, self.text_rect)
        pygame.draw.rect(self.screen, self.bgcolor, self.rect, border_radius=self.border_radius)
        for b in self.buttons:
            b.create()
        self.screen.blit(self.surface, self.rect.topleft)
    
    def add_buttons(self, *buttons):
        self.buttons = list(buttons)
        
    

class Button:
    def __init__(self, size, pos, text, font, fontsize, textcolor, bgcolor, surface=None, Menu=None, action=None, border_radius=10, border_width=0, object_display_data=None):
        self.rect = pygame.Rect(pos, size)
        self.y_i = self.rect.y
        self.menu = Menu
        self.surface = surface or Menu.surface
        self.surface_rect = Menu.rect if Menu else surface.get_rect()

        self.font = font
        self.fontsize = fontsize
        self.text = text
        self.textcolor = textcolor

        self.bgcolor = bgcolor
        self.action = action

        self.border_radius = border_radius
        self.border_width = border_width
        self.object_display_data = object_display_data
        
    def create(self):
        if self.object_display_data:
            pygame.draw.rect(self.surface, self.bgcolor, self.rect, border_radius=self.border_radius, width=self.border_width)
            font = pygame.font.SysFont(self.font, self.fontsize)
            text = font.render(self.text, True, self.textcolor)
            text_r = text.get_rect(center=(self.rect.centerx, self.rect.bottom + (self.fontsize / 2) + 5))
            if text_r.width > self.rect.width:
                prop = self.rect.width/text_r.width
                text = pygame.transform.smoothscale(text, (text_r.width*prop, text_r.height*prop))
                text_r = text.get_rect(center=(self.rect.centerx, self.rect.bottom + (self.fontsize / 2) + 5))

            self.surface.blit(text, text_r)
            pygame.draw.circle(self.surface, self.object_display_data["color"], self.rect.center, 20)
        else:
            pygame.draw.rect(self.surface, self.bgcolor, self.rect, border_radius=self.border_radius, width=self.border_width)
            font = pygame.font.SysFont(self.font, self.fontsize)
            text = font.render(self.text, True, self.textcolor)
            text_r = text.get_rect(center=self.rect.center)
            if text_r.width > self.rect.width:
                prop = self.rect.width/text_r.width*0.9
                text = pygame.transform.smoothscale(text, (text_r.width*prop, text_r.height*prop))
                text_r = text.get_rect(center=self.rect.center)
            self.surface.blit(text, text_r)

    def leftclick(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            surface_rect = self.menu.rect if self.menu else self.surface.get_rect()
            local_pos = screen_to_surface(event.pos, surface_rect.topleft, self.menu)
            if self.rect.collidepoint(local_pos):
                if self.action:
                    self.action()

class Slide_Button:
    def __init__(self, size, pos, color, sliding_objects, slide_min=0, slide_max=0, border_radius=10, surface=None, Menu=None, container=None):
        self.rect = pygame.Rect(pos, size)
        self.y_i = self.rect.y
        self.color = color
        self.sliding_objects = sliding_objects
        self.slide_min = slide_min
        self.slide_max = slide_max

        self.surface = surface or Menu.surface
        self.menu = Menu
        self.surface_rect = Menu.rect if Menu else surface.get_rect()
        self.container = container

        self.border_radius = border_radius
        self.isDragging = False
        self.drag_start = 0
        if container:
            self.min_x = self.rect.x
            self.max_x = container[2].x + container[2].width - self.rect.width
    
    def create(self):
        pygame.draw.rect(*self.container, border_radius=self.border_radius)
        pygame.draw.rect(self.surface, self.color, self.rect, border_radius=self.border_radius)

    
    def leftclick(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            local_pos = screen_to_surface(event.pos, self.surface_rect.topleft, self.menu) if self.menu else screen_to_surface(event.pos, self.surface_rect.topleft)
            if self.rect.collidepoint(local_pos):
                self.isDragging = True
                self.drag_start = pygame.mouse.get_pos()[0]

        elif event.type == pygame.MOUSEMOTION:
            if self.isDragging:
                mouse_pos = pygame.mouse.get_pos()[0]
                delta = (self.drag_start - mouse_pos)
                self.rect.x -= delta
                self.rect.x = max(self.min_x, min(self.max_x, self.rect.x))

                scroll_prop = (self.rect.x - self.min_x)/(self.max_x - self.min_x)
                button_min = min(o.rect.x for o in self.sliding_objects)
                button_max = max(o.rect.right for o in self.sliding_objects)
                button_row_width = button_max - button_min
                max_scroll = max(button_row_width - self.container[2].width, 0)

                target_offset = -scroll_prop*max_scroll
                for o in self.sliding_objects:
                    o.rect.x = self.container[2].x + target_offset + (o.rect.x - button_min)
                    
                self.drag_start = mouse_pos
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.isDragging = False


def screen_to_surface(pos, surface_pos, menu=None):
    return (pos[0] - surface_pos[0], pos[1] - surface_pos[1] + menu.scroll) if menu else (pos[0] - surface_pos[0], pos[1] - surface_pos[1])