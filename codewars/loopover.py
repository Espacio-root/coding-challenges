from typing import List, Optional
import random
import time

class Board:

    def __init__(self, configuration, correct_configuration=None, verbose=False):
        self.c = configuration
        self.b = self._init_board(self.c)
        self.s = len(self.b), len(self.b[0])
        self.m = self._init_board(correct_configuration) if correct_configuration else [[chr(n) for n in range(m, m+self.s[0])] for m in range(65, 65+self.s[0]*self.s[1], self.s[1])]
        self.w = None
        self.v = {'R':self.s[0], 'L':self.s[0], 'U':self.s[1], 'D':self.s[1]}
        self.v = {k: list(range(v)) for k,v in self.v.items()}

        self.moves = []
        self.verbose = verbose

    def _init_board(self, configuration) -> List[List[str]]:
        return [list(row) for row in configuration.split('\n')] if type(configuration) == str else configuration

    def __str__(self) -> None:
        board = ''
        for i in range(self.s[0]):
            for j in range(self.s[1]):
                board += self.b[i][j] + ' '
            board += '\n'
        return board

    def _get_index(self, board, v):
        for r in range(len(board)):
            for c in range(len(board[r])):
                if board[r][c] == v:
                    return (r, c)

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

    def move(self, moves: List[str]) -> None:
        for move in moves:
            if len(move) == 2 and move[0] in 'RLUD' and move[1].isdigit() and int(move[1]) in self.v[move[0]]:
                getattr(self, move[0])(int(move[1]))   
                self.moves.append(move)
                if self.verbose: print(self)
            else:
                if self.verbose: print(f'Illegal move: {move}')

    def interactive(self):
        # self.moves = []
        self.verbose = True
        print(self)
        st_time = time.time()
        while not self.is_solved():
            move = input(f'Enter your move [R<i> L<i> U<i> D<i>] / exit: ')
            if move.lower() == 'exit':
                break

            move = move.capitalize()
            self.move([move])
            if self.moves == 1:
                st_time = time.time()
            et_time = time.time() - st_time
            if self.is_solved():
                break

            print(f'moves: {len(self.moves)} | time: {int(et_time)//60:02d}:{int(et_time%60):02d} | mps: {len(self.moves)/et_time:.2f}')
        print(f'Congradulations! You solved the puzzle in {len(self.moves)} moves')

    def solve(self):
        self.moves = []
        if self.is_solved(): return ['R0', 'L0']
        s0, s1 = self.s[0]-1, self.s[1]-1
        idx = [r for r in range(self.s[0]) if self.b[r][:-1] != self.m[r][:-1]]
        min_idx = min(idx) if len(idx) > 0 else max(s0, s1)
        for i in range(min_idx, s0):
            for j in range(s1):
                x,y = self._get_index(self.b, self.m[i][j])
                if x == i:
                    if y == s1: self.move([f'L{i}']); continue
                    else: x+=1; self.move([f'D{y}', f'R{x}', f'U{y}']); y+=1
                self.move([f'R{x}']*(s1-y))
                if i-x > 0: self.move([f'D{s1}']*(i-x))
                if i-x < 0: self.move([f'U{s1}']*(x-i))
                self.move([f'L{i}'])

        def solve_last_row(i):
            x,y = self._get_index(self.b, self.m[-1][i])
            if x == s0:
                if y != i: 
                    if y == s1: self.move([f'R{s0}', f'D{s1}', f'L{s0}', f'U{s1}'])
                    else: self.move([f'R{s0}']*(s1-y-1) + [f'D{s1}', f'R{s0}', f'U{s1}'])
                    self.move([f'R{s0}']*(y-i))
                    self.move([f'D{s1}'] + [f'L{s0}']*(s1-i) + [f'U{s1}'])
            else:
                self.move([f'R{s0}']*(s1-i) + [f'D{s1}']*(s0-x) + [f'L{s0}']*(s1-i) + [f'U{s1}']*(s0-x))


        def solve_last_column(i):
            x,y = self._get_index(self.b, self.m[i][-1])
            if y == s1:
                if x != i:
                    if x == s0: self.move([f'D{s1}', f'R{s0}', f'U{s1}', f'L{s0}'])
                    else: self.move([f'D{s1}']*(s0-x-1) + [f'R{s0}', f'D{s1}', f'L{s0}'])
                    self.move([f'D{s1}']*(x-i))
                    self.move([f'R{s0}'] + [f'U{s1}']*(s0-i) + [f'L{s0}'])
            else:
                self.move([f'D{s1}']*(s0-i) + [f'R{s0}']*(s1-y) + [f'U{s1}']*(s0-i) + [f'L{s0}']*(s1-y))


        # self.verbose = True
        'LULD - 2nd last row'
        'LURD DLDR'
        'DLDR - 2nd lost col'
        'DLUR RDRU'
        for i in range(max(s0, s1)):
            if i < s1: solve_last_row(i)
            if i < s0: solve_last_column(i)

        if not self.is_solved() and s1 <= s0:
            if s0 % 2 == 1:
                [self.move([move]) for move in [f'D{s1-1}', f'L{s0}', f'D{s1-1}', f'R{s0}']*(s0+1) if not self.is_solved()]
            else:
                self.move([f'D{s1-1}', f'L{s0}', f'U{s1-1}', f'R{s0}'])
                [self.move([move]) for move in [f'R{s0}', f'D{s1-1}', f'R{s0}', f'U{s1-1}']*(s0+1) if not self.is_solved()]
        elif not self.is_solved() and s1 > s0:
            if s1 % 2 == 1:
                [self.move([move]) for move in [f'L{s0-1}', f'U{s1}', f'L{s0-1}', f'D{s1}']*(s1+1) if not self.is_solved()]
            else:
                self.move([f'L{s0-1}', f'U{s1}', f'R{s0-1}', f'D{s1}'])
                [self.move([move]) for move in [f'D{s1}', f'L{s0-1}', f'D{s1}', f'R{s0-1}']*(s1+1) if not self.is_solved()]
        return self.moves if self.is_solved() else None


def loopover(mixed_up_board: List[List[str]], solved_board: List[List[str]]) -> Optional[List[str]]:
    return Board(mixed_up_board, solved_board).solve()

def test_random():
    s_board = 'MEOK\nFHCI\nABPL\nJDGN'
    m_board = 'ABCD\nEFGH\nIJKL\nMNOP'
    board = Board(s_board, m_board)
    board.shuffle(100)
    print(board.solve())
    # if board.solve() == None:
    #     return board
    


if __name__ == '__main__':
    test0 = ['12\n34', '12\n34']
    test1 = ['42\n31', '12\n34']
    test2 = ['CWMFJ\nAORDB\nNKGLY\nPHSVE\nXTQUI', 'ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY']
    test3 = ['ACDBE\nFGHIJ\nKLMNO\nPQRST', 'ABCDE\nFGHIJ\nKLMNO\nPQRST']
    test4 = ['WCMDJ0\nORFBA1\nKNGLY2\nPHVSE3\nTXQUI4\nZ56789', 'ABCDEF\nGHIJKL\nMNOPQR\nSTUVWX\nYZ0123\n456789']
    test5 = ['ACDBE\nFGHIJ\nKLMNO\nPQRST\nUVWXY', 'ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY']
    test6 = ['ABCDE\nKGHIJ\nPLMNO\nFQRST\nUVWXY', 'ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY']
    test7 = ['NOFMB\nJLIAG\nEHCKD', 'ABCDE\nFGHIJ\nKLMNO']
    test8 = ['ULNI\nRZAb\nMFKV\nCGaB\nJYTX\nHEQD\nPWSO', 'ABCD\nEFGH\nIJKL\nMNOP\nQRST\nUVWX\nYZab']
    test9 = ['WCMDJ\nORFBA\nKNGLY\nPHVSE\nTXQUI', 'ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY'] # No solution
    test10 = ['JiMa\nSThj\nPDNF\nHUVZ\nOLYW\nEfcR\ngdXA\nCBIQ\nbKGe', 'ABCD\nEFGH\nIJKL\nMNOP\nQRST\nUVWX\nYZab\ncdef\nghij']
    test11 = ['CFE\nDAB', 'ABC\nDEF']
    print(loopover(*test11))
    # test_random()
    # res = []
    # for x in range(100):
    #     res.append(test_random())
    # print(res.count(None))
