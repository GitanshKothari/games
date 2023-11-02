import pygame
import requests
from icecream import ic


class Sudoku:
    def __init__(self) -> None:
        self.board = []
        self.init_pygame()

    def init_pygame(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Sudoku")
        self.board_height = 600
        self.board_width = 500
        self.cell_width = self.board_width // 9
        self.cell_height = self.cell_width
        self.screen = pygame.display.set_mode((self.board_width, self.board_height))
        self.font1 = pygame.font.SysFont("comicsans", 40)
        self.font2 = pygame.font.SysFont("comicsans", 20)

        self.mouse_x = 0
        self.mouse_y = 0

        self.curr_row = 0
        self.curr_column = 0


    def get_mouse_cord(self, pos):
        self.x = pos[0]//self.cell_width
        self.y = pos[1]//self.cell_width

    def highlight_box(self):
        for i in range(2):
            pygame.draw.line(self.screen, (255, 0, 0), (self.curr_row * self.cell_width-3, (self.curr_column + i)*self.cell_width), (self.curr_row * self.cell_width + self.cell_width + 3, (self.curr_column + i)*self.cell_width), 7)
            pygame.draw.line(self.screen, (255, 0, 0), ( (self.curr_row + i)* self.cell_width, self.curr_column * self.cell_width ), ((self.curr_row + i) * self.cell_width, self.curr_column * self.cell_width + self.cell_width), 7)
    
    def draw(self):
        self.screen.fill((225, 225, 225))
        for i in range (9):
            for j in range (9):
                if self.board[i][j]!= 0:

                    # Fill blue color in already numbered grid
                    pygame.draw.rect(self.screen, (0, 153, 153), (i * self.cell_width, j * self.cell_width, self.cell_width + 1, self.cell_width + 1))

                    # Fill grid with default numbers specified
                    text1 = self.font1.render(str(self.board[i][j]), 1, (0, 0, 0))
                    self.screen.blit(text1, (i * self.cell_width + 15, j * self.cell_width + 15))
        # Draw lines horizontally and verticallyto form grid		 
        for i in range(10):
            if i % 3 == 0 :
                thick = 7
            else:
                thick = 1
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * self.cell_width), (500, i * self.cell_width), thick)
            pygame.draw.line(self.screen, (0, 0, 0), (i * self.cell_width, 0), (i * self.cell_width, 500), thick)

    def draw_val(self, val):
        text1 = self.font1.render(str(val), 1, (0, 0, 0))
        self.screen.blit(text1, (self.mouse_x * self.cell_width + 15, self.mouse_y * self.cell_height + 15)) 

    # Raise error when wrong value entered
    def raise_error1(self):
        text1 = self.font1.render("WRONG !!!", 1, (0, 0, 0))
        self.screen.blit(text1, (20, 570)) 
    def raise_error2(self):
        text1 = self.font1.render("Wrong !!! Not a valid Key", 1, (0, 0, 0))
        self.screen.blit(text1, (20, 570)) 


    def get_sudoku_board_from_api(self) -> None:
        # url = 'https://sudoku-api.vercel.app/api/dosuku?query={newboard(limit:1){grids{value}}}'
        url = 'https://sudoku-api.vercel.app/api/dosuku'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            ic(data)
            self.board = data['newboard']['grids'][0]['value']
            self.run_game()
        else:
            print(f"Failed to fetch Sudoku board. Status code: {response.status_code}")
            return None
    
   
    def solve(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    pygame.event.pump() 
                    for k in range(1, 10):
                        if self.is_safe(i, j, k):
                            self.board[i][j] = k
                            self.curr_row = i
                            self.curr_column = j
                            self.draw()
                            self.highlight_box()
                            pygame.display.update()
                            pygame.time.delay(20)
                            if self.solve():
                                return True
                            self.board[i][j] = 0
                            self.curr_row = i
                            self.curr_column = j
                            self.draw()
                            self.highlight_box()
                            pygame.display.update()
                            pygame.time.delay(20)
                    return False
        return True

    def get_solution(self):
        if self.solve():
            print('Backtracking Solution: ')
            self.print_board()
        else:
            print('No solution exists')

    def is_safe(self, row, col, num):
        for x in range(9):
            if self.board[row][x] == num or self.board[x][col] == num or self.board[(row - row % 3) + x // 3][(col - col % 3) + x % 3] == num:
                return False
        return True
        
    def run_game(self):
        run = True
        flag1 = 0
        flag2 = 0
        rs = 0
        error = 0
        # The loop thats keep the window running
        while run:
            
            # White color background
            self.screen.fill((255, 255, 255))
            # Loop through the events stored in event.get()
            for event in pygame.event.get():
                # Quit the game window
                if event.type == pygame.QUIT:
                    run = False
                # Get the mouse position to insert number 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    flag1 = 1
                    pos = pygame.mouse.get_pos()
                    self.get_cord(pos)
                # Get the number to be inserted if key pressed 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x-= 1
                        flag1 = 1
                    if event.key == pygame.K_RIGHT:
                        x+= 1
                        flag1 = 1
                    if event.key == pygame.K_UP:
                        y-= 1
                        flag1 = 1
                    if event.key == pygame.K_DOWN:
                        y+= 1
                        flag1 = 1
                    if event.key == pygame.K_1:
                        val = 1
                    if event.key == pygame.K_2:
                        val = 2
                    if event.key == pygame.K_3:
                        val = 3
                    if event.key == pygame.K_4:
                        val = 4
                    if event.key == pygame.K_5:
                        val = 5
                    if event.key == pygame.K_6:
                        val = 6
                    if event.key == pygame.K_7:
                        val = 7
                    if event.key == pygame.K_8:
                        val = 8
                    if event.key == pygame.K_9:
                        val = 9
                    if event.key == pygame.K_RETURN:
                        flag2 = 1
                    
            if flag2 == 1:
                if self.solve() == False:
                    error = 1
                else:
                    rs = 1
                flag2 = 0
            # if val != 0:	
                # draw_val(val)
                # # print(x)
                # # print(y)
                # if valid(grid, int(x), int(y), val)== True:
                #     grid[int(x)][int(y)]= val
                #     flag1 = 0
                # else:
                #     grid[int(x)][int(y)]= 0
                #     raise_error2() 
                # val = 0
            
        	 
            self.draw() 
            if flag1 == 1:
                self.highlight_box()	 

            # Update window
            pygame.display.update() 

        # Quit pygame window 
        pygame.quit()	 

    # Get a Sudoku board from the API
if __name__ == '__main__':
    new_board = Sudoku()
    new_board.get_sudoku_board_from_api()





