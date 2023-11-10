
import pygame
class Board:
    def __init__(self, width, height, rows, cols):
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.cells = [[None for _ in range(cols)] for _ in range(rows)]
        self.cell_width = self.width // self.cols
        self.cell_height = self.height // self.rows

    def draw(self, surface):
        surface.fill((0, 0, 0))
        self.x_offset = (surface.get_width() - self.width) // 2
        self.y_offset = (surface.get_height() - self.height) // 2
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.cell_width + self.x_offset
                y = row * self.cell_height + self.y_offset
                pygame.draw.rect(surface, (255, 255, 255), (x, y, self.cell_width, self.cell_height), 2)
                if self.cells[row][col] == 'X':
                    pygame.draw.line(surface, (255, 0, 0), (x + 10, y + 10), (x + self.cell_width - 10, y + self.cell_height - 10), 4)
                    pygame.draw.line(surface, (255, 0, 0), (x + self.cell_width - 10, y + 10), (x + 10, y + self.cell_height - 10), 4)
                elif self.cells[row][col] == 'O':
                    pygame.draw.circle(surface, (0, 0, 255), (x + self.cell_width // 2, y + self.cell_height // 2), self.cell_width // 2 - 10, 4)

    def get_cell(self, row, col):
        return self.cells[row][col]

    def set_cell(self, row, col, value):
        self.cells[row][col] = value

    def is_full(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cells[row][col] is None:
                    return False
        return True

    def get_winner(self):
        # Check rows
        for row in range(self.rows):
            if self.cells[row][0] is not None and all(self.cells[row][col] == self.cells[row][0] for col in range(1, self.cols)):
                return self.cells[row][0]
        # Check columns
        for col in range(self.cols):
            if self.cells[0][col] is not None and all(self.cells[row][col] == self.cells[0][col] for row in range(1, self.rows)):
                return self.cells[0][col]
        # Check diagonals
        if self.cells[0][0] is not None and all(self.cells[row][col] == self.cells[0][0] for row, col in zip(range(1, self.rows), range(1, self.cols))):
            return self.cells[0][0]
        if self.cells[0][self.cols - 1] is not None and all(self.cells[row][col] == self.cells[0][self.cols - 1] for row, col in zip(range(1, self.rows), range(self.cols - 2, -1, -1))):
            return self.cells[0][self.cols - 1]
        return None
    
    def reset_board(self):
        self.cells = [[None for _ in range(self.cols)] for _ in range(self.rows)]

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height + 100))
        pygame.display.set_caption('Tic Tac Toe')
        turn = 'X'
        running = True
        font = pygame.font.Font(None, 25)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.get_winner() is None and not self.is_full():
                        x, y = pygame.mouse.get_pos()
                        row = (y - self.y_offset) // self.cell_height
                        col = (x - self.x_offset) // self.cell_width
                        if self.get_cell(row, col) is None:
                            self.set_cell(row, col, turn)
                            if turn == 'X':
                                turn = 'O'
                            else:
                                turn = 'X'
                    elif event.button == 1 and 400 <= event.pos[0] <= 480 and 500 <= event.pos[1] <= 530:
                        self.reset_board()
                        turn = 'X'
            screen.fill((0, 0, 0))
            self.draw(screen)
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.width // 2 - 50, self.height + 60, 100, 30))
            reset_text = font.render("Reset", True, (255, 255, 255))
            screen.blit(reset_text, (self.width // 2 - 25, self.height + 70))
            winner = self.get_winner()
            if winner is not None:
                winner_text = font.render(f'{winner} wins!', True, (255, 255, 255))
                winner_text_rect = winner_text.get_rect(center=(self.width//2, 10))
                screen.blit(winner_text, winner_text_rect)
            elif self.is_full():
                tie_text = font.render('Tie!', True, (255, 255, 255))
                screen.blit(tie_text, (self.width // 2 - 20, self.height + 10))
            pygame.display.flip()
        pygame.quit()

if __name__ == '__main__':
    board = Board(300, 400, 3, 3)
    board.run()