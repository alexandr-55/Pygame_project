import pygame
import os, sys
import random
spBoard = []

NCELLS = 9 # размерность игрового поля - число клеток

# проверка на попадание в ячейки в игровое поле
#
def is_cell_in_board(row, col):
    if  0 <= row < NCELLS  and  0 <= col < NCELLS:
        return True;
    else:
        return False

# построить маршрут передвижения шарика из ячейки (row0, col0)   в  (row1, col1) 
#
def marshrut(row0, col0, row1, col1):
    sp = []
    for i in spBoard:
        sp0 = []
        for j in i:
            sp0.append(j)
        sp.append(sp0)
    
    for r in range(NCELLS):
        for c in range(NCELLS):
            if sp[r][c] != None:
                sp[r][c] = 100
    sp[row0][col0] = 0
    i = 0  
    cont = True
    while cont:
        priznak = False
        for r in range(9):
            for c in range(NCELLS):
                if sp[r][c] == i:
                    if is_cell_in_board(r - 1, c) and sp[r - 1][c] == None:
                        sp[r - 1][c] = i + 1 
                        priznak = True
                    if is_cell_in_board(r + 1, c) and sp[r + 1][c] == None:
                        sp[r + 1][c] = i + 1    
                        priznak = True
                    if is_cell_in_board(r, c - 1) and sp[r][c - 1] == None:
                        sp[r][c - 1] = i + 1
                        priznak = True
                    if is_cell_in_board(r, c + 1) and sp[r][c + 1] == None:
                        sp[r][c + 1] = i + 1                        
                        priznak = True
                    if sp[row1][col1] != None:
                        break
                if sp[row1][col1] != None:
                    break                 
        i += 1
        #print(sp[row1][col1])
        if sp[row1][col1] != None:
            cont = False
        if not priznak:
            cont = False
        
    if sp[row1][col1] == None:
        return([])
    else:
        sp_mrsh = []
        sp_mrsh.append((row1, col1))
        i -= 1
        r = row1
        c = col1
        while i > 0:
            if is_cell_in_board(r - 1, c) and sp[r - 1][c] == i:
                r -= 1
                sp_mrsh.append((r, c))
            elif is_cell_in_board(r + 1, c) and sp[r + 1][c] == i:
                r += 1
                sp_mrsh.append((r, c))
            elif is_cell_in_board(r, c - 1) and sp[r][c - 1] == i: 
                c -= 1
                sp_mrsh.append((r, c))
            elif is_cell_in_board(r, c + 1) and sp[r][c + 1] == i:
                c += 1
                sp_mrsh.append((r, c))
            i -= 1
        sp_mrsh.append((row0, col0))
        #print(sp)
        #print(sp_mrsh)
        return sp_mrsh[::-1]


def start_cell_line(row, col, ind_color, dr, dc):
    i = 1
    cont = True
    while cont:
        if is_cell_in_board(row + dr, col +  dc):
            if spBoard[row + dr][col + dc] == ind_color:
                row += dr
                col += dc
            else:
                cont = False
        else:
            cont = False
    return (row, col)

def cells_in_line(coord1, ind_color, dr, dc):
    sp1 = []
    sp1.append(coord1)
    row = coord1[0]
    col = coord1[1]
    cont = True
    while cont:
        row += dr
        col += dc            
        if is_cell_in_board(row, col) and spBoard[row][col] == ind_color:
                sp1.append((row, col))
        else:
            cont = False
    if len(sp1) >= 5:
        return sp1
    else:
        return []
    
    
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = []
        for _ in range(height):
            sp0 = []
            for _ in range(width):
                sp0.append(None)
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
            return cell 
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
        return cell_coords
        #if cell_coords[0] != None:
            #print(cell_coords)
        #else:
            #print('None')


class Ball(pygame.sprite.Sprite):
    sp_colours = [[255, 0, 0], [40, 255, 40], [0, 0, 255], [255, 255, 0], 
                  [66, 170, 255], [128, 0, 128]]
   
    def __init__(self, radius):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        self.vybor = False
        self.ind_color = random.randint(0, len(Ball.sp_colours) - 1)
        pygame.draw.circle(self.image, Ball.sp_colours[self.ind_color],
                           (radius, radius), radius)

        cont = True
        while cont:
            self.col = random.randint(0, NCELLS - 1)
            self.row = random.randint(0, NCELLS - 1)
            if spBoard[self.row][self.col] == None:
                spBoard[self.row][self.col] = self.ind_color
                cont = False

        self.vx = 75 + self.col * 40 + 4
        self.vy = 75 + self.row * 40 + 4 
        self.dy = 0
        self.rect = pygame.Rect(self.vx, self.vy, 2 * radius, 2 * radius)
        self.centr = self.rect.center
 

    def update(self):
        if self.vybor:
            self.rect = self.rect.move(0, self.dy)
            self.dy = - self.dy
        else:
            self.rect.center = self.centr
            
    def moves(self, new_cell):
        self.vx = 75 + new_cell[1] * 40 + 4
        self.vy = 75 + new_cell[0] * 40 + 4 
        self.rect = pygame.Rect(self.vx, self.vy, 2 * self.radius, 2 * self.radius)
        self.centr = self.rect.center        
        spBoard[self.row][self.col] = None
        spBoard[new_cell[0]][new_cell[1]] = self.ind_color
        self.col = new_cell[1]
        self.row = new_cell[0]       
            
    def get_event(self, event):
        if self.rect.collidepoint(event.pos):
            self.vybor = not(self.vybor)
            self.rect = self.rect.move(0, 2)
            self.dy = -4
     
            return True 
        else:
            return False
         
    def kill(self, spdel):
        for j in range(len(spdel)):
            r = spdel[j][0]
            c = spdel[j][1]
            for i in all_sprites: 
                if i.row == r and i.col == c:
                    all_sprites.remove(i)
                    spBoard[r][c] = None
                    break
                
    
    def ball_lines(self):
        sp = []
        # по горизонтали
        coord1 = start_cell_line(self.row, self.col, self.ind_color, 0, -1)
        sp0 = cells_in_line(coord1, self.ind_color, 0, 1)
        if len(sp0) >= 5:
            return sp0
    
        # по вертикали
        sp0 = []
        coord1 = start_cell_line(self.row, self.col, self.ind_color, -1, 0)
        sp0 = cells_in_line(coord1, self.ind_color, 1, 0)
        if len(sp0) >= 5:
            return sp0
        
        # по диагонали -x=y
        sp0 = []
        coord1 = start_cell_line(self.row, self.col, self.ind_color, -1, -1)
        sp0 = cells_in_line(coord1, self.ind_color, 1, 1)
        if len(sp0) >= 5:
            return sp0
        
        # по диагонали x=y
        sp0 = []
        coord1 = start_cell_line(self.row, self.col, self.ind_color, 1, -1)
        sp0 = cells_in_line(coord1, self.ind_color, -1, 1)
        if len(sp0) >= 5:
            return sp0        
        return sp0

       #clock.tick(FPS)

def mtext(ch):
    screen.fill((0, 0, 255))
    font = pygame.font.Font(None, 70)
    text = font.render('Счёт: ' + str(ch), 1, (255, 0, 0))
    text_x = 170
    text_y = 30
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    font = pygame.font.Font(None, 30)
    text1 = font.render('>> Новая игра <<', 1, (255, 255, 255))
    text_x1 = 175
    text_y1 = 460
    text_w1 = text.get_width()
    text_h1 = text.get_height()
    screen.blit(text1, (text_x1, text_y1))    

pygame.init()

size = width, height = 500, 500
screen = pygame.display.set_mode(size)
pygame.display.flip()
screen.fill([0, 0, 0])
board = Board(NCELLS, NCELLS)
tracing = False
sp_board = []
chet = 0
nball = 0

all_sprites = pygame.sprite.Group()
for _ in range(3):
    all_sprites.add(Ball(16))
nball = 3

clock = pygame.time.Clock()
fps = 300
ball_new = None
ball_last = None
pr_add_bal = False
while True:
    mtext(chet)
    if pr_add_bal:
        sp_lin = []
        # добавить новые шарики - если возможно то 3 шарика
        pr_del_line = False
        for _ in range(3):
            if nball >= NCELLS * NCELLS:
                print('!!!!! end', chet)
                break
            newb = Ball(16)
            all_sprites.add(newb)
            nball += 1
            sp_lin = newb.ball_lines()  # проверить выстроилась ли линия
            if len(sp_lin) >= 5:
                newb.kill(sp_lin)
                chet = chet + 50 + (len(sp_lin) - 5) * 20
                nball -= len(sp_lin)
                pr_del_line = True
                # pr_add_bal = False
        pr_add_bal = False
        #if pr_del_line:
            #pr_add_bal = False
        #else:
            #pr_add_bal = True
            
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # если кликнули мышкой по полю "Новая игра"
            if event.pos[0] >= 175 and event.pos[0] <= 345:
                if event.pos[1] >= 460 and event.pos[1] <= 480:
                    # обнулить все переменные - для начала новой игры
                    spBoard = []
                    board = Board(NCELLS, NCELLS)
                    chet = 0
                    nball = 0
                    all_sprites = pygame.sprite.Group()
                    pr_add_bal = True
                    continue
            # ИГРА
            coord_cell = board.get_click(event.pos)
            if coord_cell[0] != None:
                # Если кликнули мышкой по игровому полю
                for i in all_sprites:
                    if i.get_event(event):  # кликнули по шарику
                        ball_last = ball_new
                        ball_new = i
                        if ball_last != None:  
                            # снять выделение с прошлого шарика
                            ball_last.vybor = False
                        if ball_new == ball_last:  
                            # при выборе того же шарика - отменить выделение
                            ball_last.vybor = False
                            ball_new = None
                            ball_last = None

                if ball_new != None and spBoard[coord_cell[1]][coord_cell[0]] == None:
                    # выбран шарик и задана пустая клетка для его перемещения
                    # ищем возможный маршрут движения шарика в заданную клетку - список spm
                    
                    spm = marshrut(ball_new.row, ball_new.col,coord_cell[1], coord_cell[0])
                    if len(spm) > 0:  # возможность перемещения существует
                        for i1 in spm:
                            ball_new.moves(i1)
                            board.render(screen)
                            all_sprites.draw(screen)              
                            clock.tick(fps / 30)
                            all_sprites.update()    
                            pygame.display.flip()
                        
                        # проверить   если получилась линия, то:
                        #   удалить ее 
                        #   увеличить счет
                        #   выставть признак - не добавлять новые шарики след.ходом
                        ball_new.vybor = False
                        pr_del_line = False
                        sp_lin = ball_new.ball_lines()
                        if len(sp_lin) >= 5:
                            ball_new.kill(sp_lin)
                            chet = chet + 50 + (len(sp_lin) - 5) * 20
                            nball -= len(sp_lin)
                            pr_del_line = True
                    
                        ball_last = None
                        ball_new = None
                    
                        pr_add_bal = True
                    if pr_del_line:
                        pr_add_bal = False
                    
    board.render(screen)
    all_sprites.draw(screen)   

    clock.tick(fps / 60)
    all_sprites.update()    
    pygame.display.flip()

