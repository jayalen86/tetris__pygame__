import pygame
import random
#pieces
square = [
    [
     [0,0],
     [1,1],
     [1,1],
    ]
   ]

line = [
     [
      [1,1,1,1],
      [0,0,0,0],
      [0,0,0,0],
      [0,0,0,0],
     ],
     [
      [1,0,0,0],
      [1,0,0,0],
      [1,0,0,0],
      [1,0,0,0],
      ]
        ]

T_shape = [
           [
            [0,0,0],
            [0,1,0],
            [1,1,1],
            ],
           [
            [1,0,0],
            [1,1,0],
            [1,0,0],
            ],
           [
            [1,1,1],
            [0,1,0],
            [0,0,0],
            ],
            [
            [0,0,1],
            [0,1,1],
            [0,0,1],
            ]
           ]

L_shape1 = [
            [
             [0,0,0],
             [1,0,0],
             [1,1,1],
             ],
            [
             [1,1,0],
             [1,0,0],
             [1,0,0],
             ],
            [
             [1,1,1],
             [0,0,1],
             [0,0,0],
             ],
            [
             [0,0,1],
             [0,0,1],
             [0,1,1],
            ]
            ]

L_shape2 = [
            [
             [0,0,0],
             [0,0,1],
             [1,1,1],
             ],
            [
             [1,0,0],
             [1,0,0],
             [1,1,0],
             ],
            [
             [1,1,1],
             [1,0,0],
             [0,0,0],
             ],
            [
             [0,1,1],
             [0,0,1],
             [0,0,1],
             ]
            ]

Z_shape1 = [
            [
             [0,0,0],
             [0,1,1],
             [1,1,0],
             ],
            [
             [0,1,0],
             [0,1,1],
             [0,0,1],
             ]
            ]

Z_shape2 = [
            [[0,0,0],
             [1,1,0],
             [0,1,1],
             ],
            [
             [0,1,0],
             [1,1,0],
             [1,0,0],
             ]
           ]

all_shapes = [line, square, T_shape, L_shape1, L_shape2, Z_shape1, Z_shape2]
all_colors = [(0, 128, 128), (255,255,0), (255,0,255), (0,0,255), (255,165,0), (0,255,0), (255,0,0)]
class piece():
    def __init__(self):
        self.num = random.randint(0, 6)
        self.shape = all_shapes[self.num]
        self.y = -2
        self.x = 4
        self.rotation = 0
        self.color = all_colors[self.num]

class tetris():
    def __init__(self):
        self.lines = 0
        self.level = 1
        self.blocks_on_screen = []
        self.gameover = False
        self.paused = False

    def redraw_screen(self, screen, piece, next_piece):
        screen.fill((0,0,0))
        grid = self.draw_playing_area(screen, piece)
        self.draw_playing_area_boundaries(screen) 
        self.draw_next_piece(screen, next_piece)
        self.draw_sidebar_text(screen)
        pygame.display.update()
        return grid
        
    def draw_playing_area(self, screen, piece):
        pos = self.get_pos(piece)
        grid = [[(0,0,0) for x in range(10)] for y in range(20)]
        for position in pos:
            if position[0] >= 0:
                grid[position[0]][position[1]] = piece.color
        for position in self.blocks_on_screen:
            if position[0] >= 0:
                grid[position[0]][position[1]] = position[2]  
        y_axis = 0
        for x in grid:
            x_axis = 25
            y_axis += 25
            for color in x:
                pygame.draw.rect(screen, color, (x_axis, y_axis, 25, 25), 0)
                if color != (0,0,0):
                    self.draw_block_lines(screen, x_axis, y_axis)
                x_axis += 25
        return grid

    def draw_playing_area_boundaries(self, screen):
        pygame.draw.line(screen, (210,210,210),(25,25),(275,25))
        pygame.draw.line(screen, (210,210,210),(25,525),(275,525))
        pygame.draw.line(screen, (210,210,210),(25,25),(25,525))
        pygame.draw.line(screen, (210,210,210),(275,25),(275,525))  
    
    def draw_next_piece(self, screen, piece):
        piece_shape = [[i for i in row if (row != [0,0,0] or row != [0,0,0,0])] for row in piece.shape[0]]
        set_x_axis = 340 if piece.num == 0 else 360 if piece.num == 1 else 350
        y_axis = 140 if piece.num == 0 else 100
        for x in piece_shape:
            x_axis = set_x_axis
            y_axis += 25
            for y in x:
                if y == 1:
                       pygame.draw.rect(screen, piece.color, (x_axis, y_axis, 25, 25), 0)
                       self.draw_block_lines(screen, x_axis, y_axis)
                x_axis += 25

    def draw_sidebar_text(self, screen):
        font1 = pygame.font.Font(pygame.font.get_default_font(), 36)
        text1 = font1.render('Next', True, (255,255,255))
        text2 = font1.render('Lines', True, (255,255,255))
        text3 = font1.render(str(self.lines), True, (255,255,255))
        text4 = font1.render('Level', True, (255,255,255))
        text5 = font1.render(str(self.level), True, (255, 255, 255))
        screen.blit(text1, (385-text1.get_width()/2, 90)) 
        screen.blit(text2, (385-text2.get_width()/2, 235)) 
        screen.blit(text3, (385-text3.get_width()/2, 285))
        screen.blit(text4, (385-text4.get_width()/2, 340)) 
        screen.blit(text5, (385-text5.get_width()/2, 390))

    def draw_block_lines(self, screen, x_axis, y_axis):
        pygame.draw.line(screen, (210,210,210),(x_axis, y_axis),(x_axis+25, y_axis))
        pygame.draw.line(screen, (210,210,210),(x_axis, y_axis+25),(x_axis+25, y_axis+25))
        pygame.draw.line(screen, (210,210,210),(x_axis, y_axis),(x_axis, y_axis+25))
        pygame.draw.line(screen, (210,210,210),(x_axis+25,y_axis),(x_axis+25, y_axis+25))
        
    def get_pos(self, piece):
        pos = []
        for y, val in enumerate(piece.shape[piece.rotation]):
            for x, val2 in enumerate(val):
                if val2 == 1:
                    pos.append([y+piece.y, x+piece.x])
        pos = self.adjust_for_boundaries(pos, piece)
        return pos

    def adjust_for_boundaries(self, pos, piece):
        largest_num = 9
        smallest_num = 0
        for x in pos:
            if x[1] > largest_num:
                largest_num = x[1]
            if x[1] < smallest_num:
                smallest_num = x[1]
                
        if largest_num > 9:
            for x in pos:
                x[1] -= (largest_num-9)

        if smallest_num < 0:
            for x in pos:
                x[1] += abs(smallest_num)
        return pos
    
    def move_left(self, piece):
        blocks_on_screen_pos = [[x[0], x[1]] for x in self.blocks_on_screen]
        pos = self.get_pos(piece)
        for num in pos:
            if num[1] == 0:
                return
            elif [num[0], num[1]-1] in blocks_on_screen_pos:
                return
        piece.x -= 1

    def move_right(self, piece):
        blocks_on_screen_pos = [[x[0], x[1]] for x in self.blocks_on_screen]
        pos = self.get_pos(piece)
        for num in pos:
            if num[1] == 9:
                return
            elif [num[0], num[1]+1] in blocks_on_screen_pos:
                return
        piece.x += 1
        
    def rotate_piece(self, piece):
        blocks_on_screen_pos = [[x[0], x[1]] for x in self.blocks_on_screen]
        piece.rotation = 0 if piece.rotation == len(piece.shape)-1 else piece.rotation + 1
        pos = self.get_pos(piece)
        for x in pos:
            if x in blocks_on_screen_pos:
                piece.rotation = len(piece.shape)-1 if piece.rotation == 0 else piece.rotation - 1
                break

    def check_collision(self, piece):
        blocks_on_screen_pos = [[x[0], x[1]] for x in self.blocks_on_screen]
        pos = self.get_pos(piece)
        for x in pos:
            if x[0] == 19 or [x[0]+1, x[1]] in blocks_on_screen_pos:
                for x in pos:
                    self.blocks_on_screen.append([x[0], x[1], piece.color])
                return True
        return False

    def move_down(self, piece, fall_timer):
        if fall_timer >= 10:
            fall_timer = 0
            piece.y += 1
        return fall_timer
        
    def clear_rows(self):
        rows_to_delete = []
        row = [x[0] for x in self.blocks_on_screen]
        set_of_row = list(set(row))
        set_of_row.sort()
        for x in set_of_row:
            count = 0
            for y in row:
                if y == x:
                    count += 1
                    if count == 10:
                        rows_to_delete.append(x)
                        self.remove_row_from_list(x)
                        self.lines += 1
                        self.check_update_level()
                        continue
        if len(rows_to_delete) > 0:
            rows_to_delete.sort()
            self.adjust_rows(rows_to_delete)
            return True
            
    def remove_row_from_list(self, row):
        new_list = []
        for pos in self.blocks_on_screen:
            if pos[0] != row:
                new_list.append(pos)
        del self.blocks_on_screen[:]
        for x in new_list:
            self.blocks_on_screen.append(x)

    def adjust_rows(self, rows_to_delete):
        num = rows_to_delete[0]
        for x in self.blocks_on_screen:
            if x[0] < num:
                x[0] += len(rows_to_delete)

    def check_update_level(self):
        self.level = int(self.lines / 10)+1

    def check_gameover(self):
        for x in self.blocks_on_screen:
            if x[0] < 0:
                self.gameover = True
                return True

    def draw_gameover_screen(self, screen):
        screen.fill((0,0,0))
        font1 = pygame.font.Font(pygame.font.get_default_font(), 36)
        font2 = pygame.font.Font(pygame.font.get_default_font(), 28)
        text1 = font1.render("Gameover!", True, (255,255,255))
        text2 = font2.render("(Press 'r' to Restart)", True, (255,255,255))
        screen.blit(text1, (250-text1.get_width()/2, 210))
        screen.blit(text2, (250-text2.get_width()/2, 255))
        pygame.display.update()
        
    def get_fall_speed(self):
        fall_speed = self.level + 1 if self.level < 9 else 10
        return fall_speed

    def reset(self):
        self.lines = 0
        self.level = 1
        self.paused = False
        self.gameover = False
        del self.blocks_on_screen[:]
        
        
   #fall_time/1000 >= fall_speed:      
def main():
    pygame.mixer.pre_init(44100, -16, 1, 512) #used to fix sound delay
    pygame.init()
    pygame.mixer.music.load("sounds/theme.mp3")
    pygame.mixer.music.play(-1)
    pygame.display.set_caption('Tetris')
    pygame.display.set_icon(pygame.image.load('images/tetris_logo.png'))
    screen_height = 550
    screen_width = 500
    screen = pygame.display.set_mode((screen_width, screen_height))
    clear_row_sound = pygame.mixer.Sound("sounds/clear_row.wav")
    gameover_sound = pygame.mixer.Sound("sounds/gameover.wav")
    clock = pygame.time.Clock()
    game = tetris()
    game_running = True
    current_piece = [piece(), piece()]
    fall_timer = 0
    while game_running:
        clock.tick(10)
        fall_timer += game.get_fall_speed()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                game_running = False
        if game_running == False:
            break
        
        keys = pygame.key.get_pressed()
        if game.paused == True:
            if keys[pygame.K_p]:
                game.paused = False
            continue    

        if game.gameover == False:
            if keys[pygame.K_LEFT]:
                game.move_left(current_piece[0])
            if keys[pygame.K_RIGHT]:
                game.move_right(current_piece[0])
            if keys[pygame.K_SPACE]:
                game.rotate_piece(current_piece[0])
            if keys[pygame.K_p]:
                game.paused = True
            if keys[pygame.K_DOWN]:
                fall_timer += 10
            grid = game.redraw_screen(screen, current_piece[0], current_piece[1])
            collision = game.check_collision(current_piece[0])
            if collision == False:
                fall_timer = game.move_down(current_piece[0], fall_timer)
            else:
                del current_piece[0]
                current_piece.append(piece())
                
            if game.clear_rows() == True:
                pygame.mixer.Sound.play(clear_row_sound)
            if game.check_gameover() == True:
                pygame.mixer.Sound.play(gameover_sound)
        else:
            game.draw_gameover_screen(screen)
            if keys[pygame.K_r]:
                game.reset()
            
main()
