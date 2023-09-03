import hisock
import random as ra
import json
import math
import pygame
def startclient(name,ip,port=6969):
    client = hisock.client.ThreadedHiSockClient(
        (hisock.get_local_ip(), port),
        name=name)
    profile = {"age":ra.randint(0,100),"color":ra.choice(("red","green","blue","violet"))}

    @client.on("ask_profile")
    def send_profile(question: str):
        client.send("client_profile", profile)

    client.start()

colors = {"white":"#FFFFFF","blue":"#0080AA","yellow":"#FFD027","grey":"#DCE6E8","dark":"#1F2A2D","black":"#000000"}
mainClock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Game Base (By ReaMart)')
screen_width, screen_height = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode((screen_width, screen_height),flags=pygame.RESIZABLE)
running = True
font = pygame.font.Font("Figtree-Medium.ttf",35)
def check_for_quit():
    global focused_entry
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            on_quit()
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                on_quit()
                pygame.quit()
                raise SystemExit
            elif event.key == pygame.K_BACKSPACE and not focused_entry == None:
                focused_entry.text = focused_entry.text[:-1]
            elif event.key == pygame.K_RETURN and not focused_entry == None:
                focused_entry = None
        elif event.type == pygame.TEXTINPUT:
            if not focused_entry == None and not len(focused_entry.text) > focused_entry.length:
                focused_entry.text = focused_entry.text + event.text


class Button():
    def __init__(self,loc:tuple,text:str,func,width=0, img=None):
        if img == None:
            self.img = font.render(text,1,colors["black"],None,width)
        else:
            self.img = pygame.image.load(img).convert_alpha()
        self.rect = self.img.get_rect()
        print(text,":",self.rect.width,"x",self.rect.height)
        self.rect.height = self.rect.height + 20
        self.rect.width = self.rect.width + 20
        self.rect.topleft = loc
        self.hovered = False
        self.clicked = False
        self.func = func
        self.yanim = 0
        self.realy = loc[1]
    def update(self):
        global focused_entry
        self.yanim *= 0.9
        self.rect.y = self.realy + self.yanim
        if self.rect.collidepoint(mouse_point):
            self.hovered = True
            if click_tim == 1:
                self.clicked = True
                self.func()
                focused_entry = None
                self.yanim = 10
            else:
                self.clicked = False
        else:
            self.hovered = False
    def draw(self):
        pygame.draw.rect(screen,colors["grey"],self.rect,0,15)
        if not self.hovered:
            pygame.draw.rect(screen,colors["dark"],self.rect,5,15)
        else:
            pygame.draw.rect(screen,colors["yellow"],self.rect,5,15)
        screen.blit(self.img,(self.rect.x+10,self.rect.y+10))
class Entry():
    def __init__(self,loc:tuple,length:int,pre_text:str="",def_text:str=""):
        self.img = font.render("".join(["6" for x in range(length)]),1,colors["black"],None)
        self.rect = self.img.get_rect()
        self.rect.height = self.rect.height + 20
        self.rect.width = self.rect.width + 20+5
        self.rect.topleft = loc
        self.text = def_text
        self.pre_text = pre_text
        self.hovered = False
        self.clicked = False
        self.length = length
    def update(self):
        global focused_entry
        if self.rect.collidepoint(mouse_point):
            self.hovered = True
            if click_tim == 1:
                self.clicked = True
                focused_entry = self
            else:
                self.clicked = False
        else:
            self.hovered = False
    def draw(self):
        textimg = font.render(self.text,1,colors["black"])
        pygame.draw.rect(screen,colors["white"],self.rect,0,15)
        if not focused_entry == self:
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
            screen.blit(font.render(self.pre_text,1,colors["grey"]),(self.rect.x+10,self.rect.y+10))
class Text():
    def __init__(self, loc:tuple,length:int,text:str="",fetch=None) -> None:
        self.loc = loc
        self.length = length
        self.text = text
        self.fetch = fetch
    def update(self):
        if self.fetch == None:
            self.text = self.text
        else:
            self.text = self.fetch()
    def draw(self):
        screen.blit(font.render(self.text,1,colors["black"]),self.loc)
def update_buttons(buttons_list):
    for button in buttons_list:
        button.draw()
        button.update()
def start():
    startclient(find_object(game_screens["home"],"pre_text","nickname").text,find_object(game_screens["join"],"pre_text","host IP").text)
    print("start")
def paste():
    global focused_entry
    for widget in game_screens[this_screen]:
        if type(widget) == Entry and widget.pre_text == "host IP":
            text = pygame.scrap.get_text()
            if not text == None:
                widget.text = text[:widget.length]
def copy():
    pygame.scrap.put_text(hisock.get_local_ip())
def backhome():
    global this_screen
    this_screen = "home"
def to_host():
    global this_screen
    this_screen = "host"
def to_join():
    global this_screen
    this_screen = "join"
def find_object(list, attr, val):
    for obj in list:
        if hasattr(obj, attr) and getattr(obj, attr) == val:
            return obj
    return None
def on_quit():
    name = find_object(game_screens["home"],"pre_text","nickname").text
    ip = find_object(game_screens["join"],"pre_text","host IP").text
    dict = {"name":name,"ip":ip}
    with open("cache.dat","w") as f:
        json.dump(dict,f)
try:
    with open("cache.dat","r") as f:
        cache = json.load(f)
except FileNotFoundError:
    cache = {"name":"","ip":""}
this_screen = "home"
game_screens = {"home":[Button((100,100),"host game",to_host,0),Button((100,210),"join game",to_join,0),Entry((100,320),16,"nickname",cache["name"])],
                "join":[Button((100,100),"paste",paste,0,"paste.png"),Button((10,10),"home",backhome,0,"home.png"),Button((100,210),"go",start), Entry((173,100),16,"host IP",cache["ip"])],
                "host":[Button((100,100),"copy your IP",copy,0),Button((10,10),"home",backhome,0,"home.png")],
}


focused_entry = None
click_tim = 0
while running:
    check_for_quit()
    mouse_point = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:
        click_tim += 1
    else:
        click_tim = 0
    screen.fill(colors["white"])
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]) and keys[pygame.K_v]:
        paste()
    update_buttons(game_screens[this_screen])
    pygame.display.update()
    mainClock.tick(60)