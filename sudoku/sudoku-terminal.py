import requests
from icecream import ic

class Sudoku:
    def __init__(self) -> None:
        self.board = []
    def get_sudoku_board_from_api(self) -> None:
        # url = 'https://sudoku-api.vercel.app/api/dosuku?query={newboard(limit:1){grids{value}}}'
        url = 'https://sudoku-api.vercel.app/api/dosuku'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            ic(data)
            self.board = data['newboard']['grids'][0]['value']
            print('Original board:')
            self.print_board()
            self.get_solution()
        else:
            print(f"Failed to fetch Sudoku board. Status code: {response.status_code}")
            return None
    
    def print_board(self):
        for i in range(9):
            for j in range(9):
                print(self.board[i][j], end=' ')
                if (j+1) % 3 == 0 and j != 8:
                    print('|', end = '')
            if (i+1) % 3 == 0:
                print('\n-------------------', end = '')

            print()
    
    def solve(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    for k in range(1, 10):
                        if self.is_safe(i, j, k):
                            self.board[i][j] = k
                            if self.solve():
                                return True
                            self.board[i][j] = 0
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
        


    # Get a Sudoku board from the API
if __name__ == '__main__':
    new_board = Sudoku()
    new_board.get_sudoku_board_from_api()



