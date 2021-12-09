import random
import re

choice = 0
isXgo = True

class TicTacToeBrain:

    def __init__(self, player='X'):
        self.board = {}
        self._winningCombos = (
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6])

    def createBoard(self, str):
        for i in range(9):
            self.board[i] = str[i]

    def getAvailableMoves(self):
        self._availableMoves = []
        for i in range(9):
            if self.board[i] == '_':
                self._availableMoves.append(i)
        return self._availableMoves

    def makeMove(self, position, player):
        self.board[position] = player

    def complete(self):
        if '_' not in self.board.values():
            return True
        if self.getWinner() != None:
            return True
        return False

    def getWinner(self):
        for player in ('X', 'O'):
            for combos in self._winningCombos:
                if self.board[combos[0]] == player and self.board[combos[1]] == player and self.board[combos[2]] == player:
                    return player
        if '_' not in self.board.values():
            return "tie"
        return None

    def getEnemyPlayer(self, player):
        if player == 'X':
            return 'O'
        return 'X'

    def minimax(self, player, depth=0):
        if player == 'O':
            best = -10
        else:
            best = 10

        if self.complete():
            if self.getWinner() == 'X':
                return -10 + depth, None
            elif self.getWinner() == "tie":
                return 0, None
            elif self.getWinner() == 'O':
                return 10 - depth, None
        for move in self.getAvailableMoves():
            self.makeMove(move, player)
            val, _ = self.minimax(self.getEnemyPlayer(player), depth + 1)
            # print(val)
            self.makeMove(move, '_')
            if player == 'O':
                if val > best:
                    best, bestMove = val, move
            else:
                if val < best:
                    best, bestMove = val, move
        return best, bestMove

def draw(s):
    k = 0
    line = "---------\n"
    for i in range(3):
        line += "| "
        for j in range(3):
            line += f"{s[k]} "
            k += 1
        line += "|\n"
    line += "---------"
    print(line)

def ia(s, level, attack):
    ch_x = sum_chars(s, 'X')
    ch_o = sum_chars(s, 'O')
    r, c = -1, -1
    if level == 'medium':
        for i in range(8):
            if ch_x[i] == 2 and ch_o[i] == 0:
                if i < 3:
                    r = i // 3
                    for j in range(3):
                        if s[r * 3 + j] == '_':
                            c = j
                elif i < 6:
                    c = i // 3
                    for j in range(3):
                        if s[j * 3 + c] == '_':
                            r = j
                elif i == 6:
                    for j in range(3):
                        if s[j * 3 + j] == '_':
                            r = j
                            c = j
                else:
                    for j in range(3):
                        if s[j * 3 + 2 - j] == '_':
                            r = j
                            c = 2 - j
                if r >= 0 and c >= 0:
                    break
    if level == 'easy' or r < 0 or c < 0:
        while True:
            k = random.randint(0, 8)
            if s[k] == '_':
                break
        r = k // 3
        c = k % 3
    return f"{r + 1} {c + 1}"

def sum_chars(s, ch):
    """
    Return array of the char counts in rows, cols and diagonals
    :param s: string
    :param ch:
    :return: m[0..8], where 0..2 - count ch in rows,
    2..5 - count ch in cols, 6..7 -  count ch in diagonals
    """
    m = [0 for c in s]
    for i in range(3):
        for j in range(3):
            if s[i * 3 + j] == ch:
                m[i] += 1
                m[j + 3] += 1
                if i == j:
                    m[6] += 1
                if j == 2 - i:
                    m[7] += 1
    return m

def is_game_over(s):
    ch_x = sum_chars(s, 'X')
    ch_o = sum_chars(s, 'O')
    cnt_x = ch_x[0] + ch_x[1] + ch_x[2]
    cnt_o = ch_o[0] + ch_o[1] + ch_o[2]
    is_x_win = 3 in ch_x
    is_o_win = 3 in ch_o
    if abs(cnt_x - cnt_o) > 1 or is_x_win and is_o_win:
        print("Impossible")
    elif is_x_win:
        print("X wins")
    elif is_o_win:
        print("O wins")
    elif cnt_x + cnt_o == 9:
        print("Draw")
    else:
        return False
    return True

def next_move(t, ch):
    g.createBoard(t)
    val, bestMove = g.minimax(ch)
    r = bestMove // 3
    c = bestMove % 3
    return f"{r + 1} {c + 1}"

def game(first, second):
    t = "_________"
    # t = "O_XX__XOO"
    isXgo = True
    while True:
        if isXgo:
            if first == 'user':
                digs = input("Enter the coordinates: ")
            else:
                print(f'Making move level "{first}"')
                if first == 'hard':
                    digs = next_move(t, 'X')
                else:
                    digs = ia(t, first, isXgo)
        else:
            if second == 'user':
                digs = input("Enter the coordinates: ")
            else:
                print(f'Making move level "{second}"')
                if second == 'hard':
                    digs = next_move(t, 'O')
                else:
                    digs = ia(t, second, isXgo)

        if re.match("[1-9] +[1-9]", digs) is None:
            print("You should enter numbers!")
            continue
        elif re.match("[1-3] +[1-3]", digs) is None:
            print("Coordinates should be from 1 to 3!")
            continue
        else:
            row, col = digs.split()
            k = 3 * (int(row) - 1) + int(col) - 1
            if t[k] == '_':
                ch = "X" if isXgo else "O"
                t = t[:k] + ch + t[k + 1:]
                isXgo = not isXgo
            else:
                print("This cell is occupied! Choose another one!")
                continue
        draw(t)
        if is_game_over(t):
            print()
            break


# t = input("Enter the cells: ")
t = "_________"
cmds = {'user', 'easy', 'medium', 'hard'}
g = TicTacToeBrain()

while True:
    cmd = input('Input command: ')
    if cmd == 'exit':
        break
    cmd = cmd.split()
    if len(cmd) < 3 or cmd[0] != 'start' or cmd[1] not in cmds or cmd[2] not in cmds:
        print('Bad parameters!')
        continue
    draw(t)
    game(cmd[1], cmd[2])


