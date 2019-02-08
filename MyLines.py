import pygame
import os, sys
import random
spBoard = []

def is_cell_in_board(x, y):
    if  0 <= x < 9  and  0 <= y < 9:
        return True;
    else:
        return False
    
class Board:
    # �������� ����
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = []
        for _ in range(height):
            sp0 = []
            for _ in range(width):
                sp0.append(-1)
            self.board.append(sp0)
            spBoard.append(sp0)
        #print(self.board)
        # �������� �� ���������
        self.left = 75
        self.top = 75
        self.cell_size = 40
        

    # ��������� �������� ����
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        
    def render(self, screen):
        for i in range(self.width):
            for j in range(self.height):
                color = (200, 200, 180)
#                color = (0, 0, 0)
                pygame.draw.rect(screen, color, (self.left + i * self.cell_size, self.top + j * self.cell_size, self.cell_size, self.cell_size), 0)
                color = (255, 36, 0)
                color = (255, 255, 255)
                pygame.draw.rect(screen, color, (self.left + i * self.cell_size, self.top + j * self.cell_size, self.cell_size, self.cell_size), 1)   
                
    def get_click(self, mouse_pos):
            cell = self.get_cell(mouse_pos)
            return(cell)
            #self.on_click(cell)    
    
    def get_cell(self, mouse_pos):
        x = mouse_pos[0]
        y = mouse_pos[1]
        if x < self.left or x > self.left + self.width * self.cell_size:
            cell_x = None
            cell_y = None
        elif y < self.top or y > self.top + self.height * self.cell_size:
            cell_x = None
            cell_y = None
        else:
            cell_x = (x - self.left + self.cell_size - 1) // self.cell_size - 1
            cell_y = (y - self.top + self.cell_size - 1) // self.cell_size - 1
        return (cell_x, cell_y)
    
    def on_click(self, cell_coords):
        return(cell_coords)
        #if cell_coords[0] != None:
            #print(cell_coords)
        #else:
            #print('None')


class Ball(pygame.sprite.Sprite):
    sp_colours = [[255, 0, 0], [40, 255, 40], [0, 0, 255], [255, 255, 0], 
                  [66, 170, 255], [128, 0, 128]]
#,  [255, 120, 0], [128, 0, 128], [128, 25, 25]] #, [128, 0, 255]] 
#   [66, 170, 255], [255, 150, 0], [75, 0, 130], [128, 25, 25]] #, [128, 0, 255]] 
    
    def __init__(self, radius):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        self.vybor = False
        self.ind = random.randint(0, len(Ball.sp_colours) - 1)
        pygame.draw.circle(self.image, Ball.sp_colours[self.ind],
                           (radius, radius), radius)
        #self.vx = random.randint(-5, 5)
        #self.vy = random.randrange(-5, 5)
        cont = True
        while cont:
            self.indx = random.randint(0, 8)
            self.indy = random.randint(0, 8)
            if spBoard[self.indy][self.indx] == -1:
                spBoard[self.indy][self.indx] = self.ind
                cont = False
   
        self.vx = 75 + self.indx * 40 + 4
        self.vy = 75 + self.indy * 40 + 4 
        self.dy = 0
        self.rect = pygame.Rect(self.vx, self.vy, 2 * radius, 2 * radius)
        self.centr = self.rect.center
 
    #def update(self):
        #self.rect = self.rect.move(self.vx, self.vy)
    def update(self):
        if self.vybor:
            self.rect = self.rect.move(0, self.dy)
            self.dy = - self.dy
        else:
            self.rect.center = self.centr
            
    def moves(self, new_cell):
        self.vx = 75 + new_cell[0] * 40 + 4
        self.vy = 75 + new_cell[1] * 40 + 4 
        #self.dy = 0
        self.rect = pygame.Rect(self.vx, self.vy, 2 * self.radius, 2 * self.radius)
        self.centr = self.rect.center        #self.rect = self.rect.move(50, 50)
        spBoard[self.indy][self.indx] = -1
        spBoard[new_cell[1]][new_cell[0]] = self.ind
        self.indx = new_cell[0]
        self.indy = new_cell[1]       
            
    def get_event(self, event):
        if self.rect.collidepoint(event.pos):
            self.vybor = not(self.vybor)
            self.rect = self.rect.move(0, 2)
            self.dy = -4
            #centr = self.rect.center
                #self.image = self.image_boom
                #self.rect = self.image.get_rect()
                #self.rect.center = centr        
            return True 
        else:
            return False
    


    def ball_lines(self):
        sp = [(self.indx, self.indy)]
        l = 1
        i = 1
        cont = True
        while cont:
            if is_cell_in_board(self.indx - i, self.indy):
                if spBoard[self.indy][self.indx - i] == self.ind:
                    sp.append((self.indx - i, self.indy))
                    l += 1
                else:
                    cont = False
            else:
                cont = False
            i += 1
        i = 1
        cont = True
        while cont:
            if is_cell_in_board(self.indx + i, self.indy):
                if spBoard[self.indy][self.indx + i] == self.ind:
                    sp.append((self.indx + i, self.indy))
                    l += 1
                else:
                    cont = False
            else:
                cont = False            
            i += 1
        print(sp)
        return sp

       #clock.tick(FPS)
pygame.init()

size = width, height = 500, 500
screen = pygame.display.set_mode(size)
pygame.display.flip()
#start_screen()
screen.fill([0, 0, 0])
board = Board(9, 9)
tracing = False
sp_board = []

all_sprites = pygame.sprite.Group()
for _ in range(3):
    all_sprites.add(Ball(16))

clock = pygame.time.Clock()
fps = 300
ball_new = None
ball_last = None
pr_add_bal = False
while True:
    screen.fill((0, 0, 0))

    if pr_add_bal:
        sp_lin = []
        for _ in range(3):
            newb = Ball(16)
            all_sprites.add(newb)
            sp_lin = newb.ball_lines()
            
            
        pr_add_bal = False
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            coord_cell = board.get_click(event.pos)
            a = coord_cell[1]
            if coord_cell[0] != None:
                for i in all_sprites:
                    if i.get_event(event):
                        ball_last = ball_new
                        ball_new = i
                        if ball_last != None:
                            ball_last.vybor = False
                        if ball_new == ball_last:
                            ball_new = None
                            ball_last.vybor = True
                    print(i.indx, i.indy)
                if ball_new != None and spBoard[coord_cell[1]][coord_cell[0]] == -1:
                    print(spBoard)

                    ball_new.moves(coord_cell)
                    ball_new.vybor = False
                    sp_lin = ball_new.ball_lines()
                    ball_last = None
                    ball_new = None
                    
                    pr_add_bal = True
                    #if not board.lines():
                        #pr_add_bal = True
                    #ball_vybor.vybor =False
                    #ball_vybor = -100
                    
    board.render(screen)
    #for _ in range(3):
        #all_sprites.add(Ball(16))    
    all_sprites.draw(screen)   

    clock.tick(fps/60)
    all_sprites.update()    
    pygame.display.flip()




'''while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.MOUSEBUTTONDOWN:
            l.start_move(event.pos)
            tracing = True
        if event.type == pygame.MOUSEMOTION:
            
            if tracing:
                l.move(event.pos)
#            pygame.draw.circle(screen, (0, 0, 255), event.pos, 20)
        if event.type == pygame.MOUSEBUTTONUP:
            tracing = False
    board.render(screen)
    pygame.display.flip()
        #elif event.type == pygame.KEYDOWN or \
            #event.type == pygame.MOUSEBUTTONDOWN:
            #return  # начинаем игру
#while pygame.event.wait().type != pygame.QUIT:
    #pass
#pygame.quit()
'''