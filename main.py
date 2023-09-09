from socket import gaierror
import pygame
import hisock
import ui
import globals
import checksum


class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("framework")
        self.screen_size = pygame.display.get_desktop_sizes()[0]
        self.screen = pygame.display.set_mode(self.screen_size,flags=pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.mouse_point = (0,0)
        self.clicktim = 0

        self.cache = checksum.load_safe("cache.dat",{"name":"none","ip":""})
        self.tab = "home"
        self.network_state = ""
        self.tabs = {"home":{
                            "host":ui.Button((100,100),"host game",lambda:setattr(self,"tab","host"),0),
                            "join":ui.Button((100,200),"join game",lambda:setattr(self,"tab","join"),0),
                            "name":ui.Entry((100,320),16,"nickname",self.cache["name"]),
                            },
                    "join":{
                            "home":ui.Button((5,20),"home",lambda:setattr(self,"tab","home"),0,"home.png"),
                            "ip":ui.Entry((100,100),16,"host IP",self.cache["ip"]),
                            "ctrlv":ui.Text((100,163),0,"tip: use ctrl+v to paste server IP"),
                            "connect":ui.Button((100,210),"connect",self.join_game),
                            },
                    "host":{
                            "home":ui.Button((5,20),"home",lambda:setattr(self,"tab","home"),0,"home.png"),
                            "copy":ui.Button((100,100),"copy IP",lambda:pygame.scrap.put_text(hisock.get_local_ip()),0),
                            "host":ui.Button((100,200),"start server",self.host_game,0)
                            },
                    "play":{
                        
                            },
                    "starting":{
                        
                            }
                    }

        self.name = "player"
        self.event_dict = {
            "mouse_point":(),
            "mouse_0":0,
            "mouse_1":0,
            "mouse_2":0,
            "focused_element":None,
            "text":"",
            "backspace":False,
            "enter":False,
        }
        self.log = ui.Log((200,300),(self.screen_size[0]-200,self.screen_size[1]-300),globals.log_font)
    def loop(self):
        while self.running:
            self.screen.fill(globals.colors["white"])
            self.events()
            self.mouse_point = pygame.mouse.get_pos()
            self.screen.blit(globals.log_font.render(self.tab,1,globals.colors["black"]),(20,0))
            self.log.draw(self.screen)
            self.update_ui()
            self.clock.tick(60)
            pygame.display.update()

    def events(self):
        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.pre_quit()
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pre_quit()
                    pygame.quit()
                    raise SystemExit
                elif event.key == pygame.K_BACKSPACE:
                    self.event_dict["focused_element"].text = self.event_dict["focused_element"].text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.event_dict["focused_element"] = None
                elif event.key == pygame.K_v and pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]:
                    self.event_dict["focused_element"].text = pygame.scrap.get_text()[:self.event_dict["focused_element"].length]
            elif event.type == pygame.VIDEORESIZE:
                self.screen_size = event.size
            elif event.type == pygame.TEXTINPUT and self.event_dict["focused_element"]:
                if self.event_dict["focused_element"].length > len(self.event_dict["focused_element"].text):
                    self.event_dict["focused_element"].text = self.event_dict["focused_element"].text + event.text.lower()
        if pygame.mouse.get_pressed()[0]:
            self.clicktim += 1
        else:
            self.clicktim = 0
    
    def update_ui(self):
        self.update_event_dict()
        current_tab = self.tabs[self.tab]
        for name in current_tab.keys():
            current_tab[name].update(self.event_dict)
            current_tab[name].draw(self.screen,self.event_dict)
        if (pygame.time.get_ticks() //1000) % 2 == 0:
            text = globals.log_font.render(self.network_state,1,globals.colors["blue"])
            self.screen.blit(text,(self.screen_size[0]-text.get_width()-5,0))
    def update_event_dict(self):
        self.event_dict["mouse_point"] = pygame.mouse.get_pos()
        for button, pressed in enumerate(pygame.mouse.get_pressed()):
            if pressed:
                self.event_dict[f"mouse_{button}"] += 1
            else:
                self.event_dict[f"mouse_{button}"] = 0
    def update_cache(self):
        self.cache["name"] = self.tabs["home"]["name"].text
        self.cache["ip"] = self.tabs["join"]["ip"].text
    
    def host_game(self):
        if not self.network_state == "":
            self.log.append(f"[ERR] already {self.network_state}")
            return
        try:
            self.server = hisock.server.ThreadedHiSockServer((hisock.get_local_ip(), 6969))
            self.broadcast("started")
            self.broadcast("waiting for players")
            self.network_state = "HOSTING"
            profile = {"name":self.tabs["home"]["name"].text}
            @self.server.on("join")
            def on_client_join(client: hisock.utils.ClientInfo):
                self.server.send_client(client, "ask_profile",profile)
                self.broadcast(f"{client.name} connected!")

                self.server.send_all_clients("tab","starting")
                self.tab = "starting"
            @self.server.on("client_profile")
            def on_profile_r(client: hisock.utils.ClientInfo, profile:dict):
                self.otherprofile = profile
                print(self.otherprofile)
            @self.server.on("move")
            def handle_move(client: hisock.utils.ClientInfo, move:list):
                print(f"{client.name} did {move}")

            self.server.start()
        except WindowsError as err:
            if err.winerror == 10048:
                self.log.append("[ERR] port already occupied")
                self.network_state = ""
    def join_game(self):
        if not self.network_state == "":
            self.log.append(f"[ERR] already {self.network_state}")
            return
        ip = self.tabs["join"]["ip"].text
        name = self.tabs["home"]["name"].text
        self.network_state = "JOINED"
        profile = {"name":self.tabs["home"]["name"].text}
        try:
            self.client = hisock.client.ThreadedHiSockClient((ip, 6969),name)
            @self.client.on("ask_profile")
            def send_profile(otherprofile: dict):
                self.otherprofile = otherprofile
                self.client.send("client_profile", profile)
                print(self.otherprofile)
                self.log.append(f"[INF] playing against {self.otherprofile['name']}")
            @self.client.on("server_msg")
            def server_msg(msg:str):
                self.log.append(f"[SERVER] {msg}")
            @self.client.on("tab")
            def set_tab(tab:str):
                self.tab = tab
            self.client.start()
        except hisock.utils.ServerNotRunning:
            self.network_state = ""
            self.log.append(f"[ERR] server not running")
        except gaierror:
            self.network_state = ""
            self.log.append(f"[ERR] server non-existent")
    def broadcast(self,text:str):
        self.server.send_all_clients("server_msg",text)
        self.log.append(f"[SERVER] {text}")
    def pre_quit(self):
        self.update_cache()
        if self.network_state == "HOSTING":
            self.server.close()
        elif self.network_state == "JOINED":
            self.client.close()
        checksum.save_safe(self.cache,"cache.dat")
if __name__ == "__main__":
    game = Game()
    game.loop()