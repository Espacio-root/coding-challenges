from typing import List, Optional
import random
import time

class Board:

    def __init__(self, configuration, correct_configuration=None):
        self.c = configuration
        self.b = self._init_board(self.c) if type(self.c) == str else self.c
        self.s = len(self.b), len(self.b[0])
        self.m = correct_configuration if correct_configuration else [[chr(n) for n in range(m, m+self.s[0])] for m in range(65, 65+self.s[0]*self.s[1], self.s[1])]

        self.v = {'R':self.s[1], 'L':self.s[1], 'U':self.s[0], 'D':self.s[0]}
        self.v = {k: list(range(v)) for k,v in self.v.items()}
        self.moves = 0

    def _init_board(self, configuration) -> List[List[str]]:
        return [list(row) for row in configuration.split('\n')]

    def __str__(self) -> None:
        board = ''
        for i in range(self.s[0]):
            for j in range(self.s[1]):
                board += self.b[i][j] + ' '
            board += '\n'
        return board

    def is_solved(self) -> bool:
        return self.b == self.m

    def shuffle(self, num_moves=100) -> None:
        r_directions = random.choices(['R', 'L', 'U', 'D'], k=num_moves)
        r_moves = [f'{d}{random.choice(self.v[d])}' for d in r_directions]
        
        self.move(r_moves)

    def R(self, index) -> None:
        row = self.b[index].copy()
        for i, v in enumerate(row):
            self.b[index][(i+1)%self.s[1]] = v

    def L(self, index) -> None:
        row = self.b[index].copy()
        for i, v in enumerate(row):
            self.b[index][(i-1)%self.s[1]] = v

    def U(self, index) -> None:
        column = [row[index] for row in self.b].copy()
        for i, v in enumerate(column):
            self.b[(i-1)%self.s[0]][index] = v

    def D(self, index) -> None:
        column = [row[index] for row in self.b].copy()
        for i, v in enumerate(column):
            self.b[(i+1)%self.s[0]][index] = v

    def move(self, moves: List[str], verbose: bool = False) -> None:
        for move in moves:
            if len(move) == 2 and move[0] in 'RLUD' and move[1].isdigit() and int(move[1]) in self.v[move[0]]:
                getattr(self, move[0])(int(move[1]))   
                self.moves += 1
                if verbose: print(self)
            else:
                if verbose: print('Illegal move')
                return 'Illegal'

    def interactive(self):
        self.moves = 0
        print(self)
        while not self.is_solved():
            move = input(f'Enter your move [R<i> L<i> U<i> D<i>] / exit: ')
            if move.lower() == 'exit':
                break

            move = move.capitalize()
            self.move([move], True)
            if self.moves == 1:
                st_time = time.time()
            et_time = time.time() - st_time

            print(f'moves: {self.moves} | time: {int(et_time)//60:02d}:{int(et_time%60):02d} | mps: {self.moves/et_time:.2f}')
        print(f'Congradulations! You solved the puzzle in {self.moves} moves')


def loopover(mixed_up_board: List[List[str]], solved_board: List[List[str]]) -> Optional[List[str]]:
    return None


if __name__ == '__main__':
    config = 'ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY'
    board = Board(config)
    board.shuffle()
    board.interactive()
