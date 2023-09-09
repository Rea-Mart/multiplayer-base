import pygame
import math

from globals import colors,font, log_font

class Button():
    def __init__(self,loc:tuple,text:str,func,width=0, img=None):
        if img == None:
            self.img = font.render(text,1,colors["black"],None,width)
        else:
            self.img = pygame.image.load(img).convert_alpha()
        self.rect = self.img.get_rect()
        self.rect.height = self.rect.height + 20
        self.rect.width = self.rect.width + 20
        self.rect.topleft = loc
        self.hovered = False
        self.clicked = False
        self.func = func
        self.yanim = 0
        self.realy = loc[1]
        self.text = text
    def update(self,events):
        global focused_entry
        self.yanim *= 0.9
        self.rect.y = self.realy + self.yanim
        if self.rect.collidepoint(events["mouse_point"]):
            self.hovered = True
            if events["mouse_0"] == 1:
                self.clicked = True
                self.func()
                focused_entry = None
                self.yanim = 10
            else:
                self.clicked = False
        else:
            self.hovered = False
    def draw(self,screen, events):
        pygame.draw.rect(screen,colors["grey"],self.rect,0,15)
        if not self.hovered:
            pygame.draw.rect(screen,colors["dark"],self.rect,5,15)
        else:
            pygame.draw.rect(screen,colors["yellow"],self.rect,5,15)
        screen.blit(self.img,(self.rect.x+10,self.rect.y+10))
class Entry():
    def __init__(self,loc:tuple,length:int,pre_text:str="",def_text:str="", font=font):
        self.font = font
        self.img = self.font.render("".join(["6" for x in range(length)]),1,colors["black"],None)
        self.rect = self.img.get_rect()
        self.rect.height = self.rect.height + 20
        self.rect.width = self.rect.width + 20+5
        self.rect.topleft = loc
        self.text = def_text
        self.pre_text = pre_text
        self.hovered = False
        self.clicked = False
        self.length = length
    def update(self,events): #move long arguments to 1 dict with ui info
        global focused_entry
        if self.rect.collidepoint(events["mouse_point"]):
            self.hovered = True
            if events["mouse_0"] == 1:
                self.clicked = True
                events["focused_element"] = self
            else:
                self.clicked = False
        else:
            self.hovered = False
    def draw(self,screen,events):
        textimg = self.font.render(self.text,1,colors["black"])
        pygame.draw.rect(screen,colors["white"],self.rect,0,15)
        if not events["focused_element"] == self:
            pygame.draw.rect(screen,colors["dark"],self.rect,5,15)
        else:
            pygame.draw.rect(screen,colors["yellow"],self.rect,5,15)

            if math.sin(pygame.time.get_ticks()/180) > 0:
                # pygame.draw.line(screen, colors["black"],(self.rect.x+10+textimg.get_width(),self.rect.y+10),(self.rect.x+10+textimg.get_width(),self.rect.y+self.rect.height-10))
                pygame.draw.circle(screen,colors["yellow"],(self.rect.x+10+textimg.get_width(),self.rect.y+5),4)
                pygame.draw.circle(screen,colors["yellow"],(self.rect.x+10+textimg.get_width(),self.rect.y+self.rect.height-5),4)
        if len(self.text) >0:
            screen.blit(textimg,(self.rect.x+10,self.rect.y+10))
        else:
            screen.blit(self.font.render(self.pre_text,1,colors["grey"]),(self.rect.x+10,self.rect.y+10))
class Text():
    def __init__(self, loc:tuple,length:int,text:str="",fetch=None,font:tuple=("Figtree-Medium.ttf",15)) -> None:
        self.font = pygame.font.Font(font[0],font[1])
        self.loc = loc
        self.length = length
        self.text = text
        self.fetch = fetch
    def update(self,events):
        if self.fetch == None:
            self.text = self.text
        else:
            self.text = self.fetch()
    def draw(self,screen, events):
        screen.blit(self.font.render(self.text,1,colors["black"]),self.loc)
class Log():
    def __init__(self,size:tuple,pos:tuple,font:pygame.font.Font):
        self.rect = pygame.rect.Rect(pos[0],pos[1],size[0],size[1])
        self.msgs = []
        self.font = font
        self.fontheight = self.font.get_height()
        self.maxmsg = size[1] // self.fontheight
        self.colorcodes = {
            "[SERVER]":colors["blue"],
            "[INF]":colors["yellow"],
            "[ERR]":(255,0,0)
        }
    def append(self,text:str):
        self.msgs.insert(0,text)
        if len(self.msgs) > self.maxmsg:
            del self.msgs[-1]
    def draw(self,screen):
        pygame.draw.rect(screen,colors["grey"],self.rect,5,15)
        height_used = 0
        for x, msg in enumerate(self.msgs):
            for key in self.colorcodes:
                if key in msg:
                    color = self.colorcodes[key]
            text_surf = self.font.render(msg,1,color,None,self.rect.width-15)
            height = text_surf.get_height()
            if height_used + height + 10 < self.rect.height:
                screen.blit(text_surf,(self.rect.x+10,self.rect.y+height_used+10))
                height_used += height
