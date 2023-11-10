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

        # Add buttons
        self.reset_button = pygame.Rect(50, 520, 100, 50)
        self.solve_button = pygame.Rect(350, 520, 100, 50)
        self.reset_text = self.font2.render("Reset", True, (0, 0, 0))
        self.solve_text = self.font2.render("Solve", True, (0, 0, 0))

    def reset_board(self):
        self.get_sudoku_board_from_api()

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
                    self.screen.blit(text1, (i * self.cell_width + 15, j * self.cell_width))
        # Draw lines horizontally and verticallyto form grid		 
        for i in range(10):
            if i % 3 == 0 :
                thick = 7
            else:
                thick = 1
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * self.cell_width), (500, i * self.cell_width), thick)
            pygame.draw.line(self.screen, (0, 0, 0), (i * self.cell_width, 0), (i * self.cell_width, 500), thick)

        # Draw buttons
        pygame.draw.rect(self.screen, (255, 0, 0), self.reset_button)
        pygame.draw.rect(self.screen, (255, 0, 0), self.solve_button)
        self.screen.blit(self.reset_text, (self.reset_button.x + 20, self.reset_button.y + 10))
        self.screen.blit(self.solve_text, (self.solve_button.x + 20, self.solve_button.y + 10))

    # Raise error when wrong value entered
    def raise_error1(self):
        text1 = self.font1.render("WRONG !!!", 1, (0, 0, 0))
        self.screen.blit(text1, (20, 570)) 
    def raise_error2(self):
        text1 = self.font1.render("Wrong !!! Not a valid Key", 1, (0, 0, 0))
        self.screen.blit(text1, (20, 570)) 


    def get_sudoku_board_from_api(self) -> None:
        
        # url = 'https://sudoku-api.vercel.app/api/dosuku?query={newboard(limit:1){grids{value}}}'
        # url = 'https://sudoku-api.vercel.app/api/dosuku'
        url = 'https://sudoku-api.vercel.app/api/dosuku?query={newboard(limit:1){grids{value}}}'
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

    def is_safe(self, row, col, num):
        for x in range(9):
            if self.board[row][x] == num or self.board[x][col] == num or self.board[(row - row % 3) + x // 3][(col - col % 3) + x % 3] == num:
                return False
        return True
        
    def run_game(self):
        run = True
        flag2 = 0

        # The loop thats keep the window running
        while run:
            
            # White color background
            self.screen.fill((255, 255, 255))
            # Loop through the events stored in event.get()
            for event in pygame.event.get():
                # Quit the game window
                if event.type == pygame.QUIT:
                    run = False
                # Get the number to be inserted if key pressed 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        flag2 = 1
                    if event.key == pygame.K_r:
                        self.reset_board()
                # Check if mouse is clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if mouse is clicked on the button
                    if self.reset_button.collidepoint(event.pos):
                        self.reset_board()
                    if self.solve_button.collidepoint(event.pos):
                        if self.solve():
                            print("Solved")

            self.draw() 

            # Update window
            pygame.display.update() 

        # Quit pygame window 
        pygame.quit()	 

    # Get a Sudoku board from the API
if __name__ == '__main__':
    new_board = Sudoku()
    new_board.get_sudoku_board_from_api()
