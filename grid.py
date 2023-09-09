import pygame,math
import sys, json
mainClock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Game Base (By ReaMart)')
screen_width, screen_height = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode((screen_width, screen_height),flags=pygame.RESIZABLE)
running = True
font = pygame.font.Font("Figtree-Medium.ttf",35)
zoom = 1
def check_for_quit():
    global zoom
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.MOUSEWHEEL:
            if not zoom + event.y**3/100 < 0.1:
                zoom += event.y**3/100
            grid.cellsize = zoom*grid.b_cell_size
            grid.rect.width = grid.cellsize*grid.size[0]
            grid.rect.height = grid.cellsize*grid.size[1]
colors = {"white":"#FFFFFF","blue":"#0080AA","yellow":"#FFD027","grey":"#DCE6E8","dark":"#1F2A2D","black":"#000000"}

class Grid():
    def __init__(self,loc,size,cellsize,img1=None,img2=None):
        
        row = [0 for x in range(size[0])]
        self.grid = [json.loads(json.dumps(row)) for y in range(size[1])]
        self.cellsize = cellsize
        self.b_cell_size = cellsize
        self.size = size
        self.rect = pygame.rect.Rect(loc[0],loc[1],size[0]*cellsize,size[1]*cellsize)
        self.mouse_cell = None
        
        self.switch = False # DELETE DELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETE
    def draw(self):
        if self.mouse_cell == None:
            pygame.draw.rect(screen,colors["black"],self.rect,5,10)
        else:
            pygame.draw.rect(screen,colors["yellow"],self.rect,5,10)
            pygame.draw.circle(screen,colors["yellow"],(self.mouse_cell[0]*self.cellsize+self.rect.x+self.cellsize/2,self.mouse_cell[1]*self.cellsize+self.rect.y+self.cellsize/2),10*zoom)


        for row in range(1,self.size[1]):
            pygame.draw.line(screen,colors["black"],(self.rect.left,self.rect.y+row*self.cellsize),(self.rect.right,self.rect.y+row*self.cellsize),3)
        for col in range(1,self.size[0]):
            pygame.draw.line(screen,colors["black"],(self.rect.left+col*self.cellsize,self.rect.top),(self.rect.left+col*self.cellsize,self.rect.bottom),3)
        for row in range(len(self.grid)):
            for cell in range(len(self.grid[0])):
                if self.grid[row][cell] == 1:
                    pygame.draw.circle(screen,colors["yellow"],(cell*self.cellsize+self.rect.x+self.cellsize/2,row*self.cellsize+self.rect.y+self.cellsize/2),self.cellsize/2,5)
                elif self.grid[row][cell] == -1:
                    pygame.draw.line(screen,colors["blue"],(cell*self.cellsize+self.rect.x+self.cellsize,row*self.cellsize+self.rect.y+self.cellsize),(cell*self.cellsize+self.rect.x,row*self.cellsize+self.rect.y),5)
                    pygame.draw.line(screen,colors["blue"],(cell*self.cellsize+self.rect.x+self.cellsize,row*self.cellsize+self.rect.y),(cell*self.cellsize+self.rect.x,row*self.cellsize+self.rect.y+self.cellsize),5)
        text = font.render(str(len(self.check(
            (1,1),
            ((-1,-1),(1,1),(-1,1),(1,-1)),
            1))),1,colors["black"])
        screen.blit(text,(10,10))
    def add(self, pos:tuple, type:int):
        self.grid[pos[1]][pos[0]] = type
        print("added")
        print(self.grid)
    def update(self):
        if self.rect.collidepoint(mouse_point):
            self.mouse_cell = (round((mouse_point[0]-self.rect.x-self.cellsize/2)/self.cellsize),round((mouse_point[1]-self.rect.y-self.cellsize/2)/self.cellsize))
            if click_tim == 1:
                self.clicked = True
                
                if self.switch == True:
                    self.switch = False
                    self.add(self.mouse_cell,1)
                else:
                    self.switch = True
                    self.add(self.mouse_cell,1)
                # print(self.grid[0])
            else:
                self.clicked = False
        else:
            self.mouse_cell = None
            self.clicked = False
    def check(self, loc:tuple, pattern:tuple, val):
        "checks for each point in pattern, relative to loc, if the cell is val, returns finds as list"
        finds = []
        for point in pattern:
            thispoint = (point[0]+loc[0],point[1]+loc[1])
            if self.grid[thispoint[1]][thispoint[0]] == val:
                finds.append(point)
        return finds

            
grid = Grid((100,100),(6,6),40)
click_tim = 0
while running:
    check_for_quit()
    mouse_point = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:
        click_tim += 1
    else:
        click_tim = 0
    screen.fill((255,255,230))
    grid.draw()
    grid.update()
    pygame.display.update()
    mainClock.tick(60)