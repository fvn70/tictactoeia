import re
from random import shuffle

win_combos = (
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6])


def minimax(board, player, depth=0):
    if player == 'O':
        best = -10
    else:
        best = 10

    _win = get_winner(board)
    if _win == 'X':
        return -10 + depth, None
    elif _win == "Draw":
        return 0, None
    elif _win == 'O':
        return 10 - depth, None

    _moves = [i for i in range(9) if board[i] == '_']
    for k in _moves:
        board = board[:k] + player + board[k + 1:]
        _player = 'O' if player == 'X' else 'X'
        val, _ = minimax(board, _player, depth + 1)
        board = board[:k] + '_' + board[k + 1:]
        if player == 'O':
            if val > best:
                best, best_move = val, k
        else:
            if val < best:
                best, best_move = val, k
    return best, best_move


def get_winner(board):
    win = None
    for player in ('X', 'O'):
        for combos in win_combos:
            if board[combos[0]] == player \
                    and board[combos[1]] == player \
                    and board[combos[2]] == player:
                if win is None:
                    win = player
                elif win != player:
                    win = "Impossible"
    if win is not None:
        return win
    if '_' not in board:
        return "Draw"
    return None


def draw(board):
    k = 0
    line = "---------\n"
    for i in range(3):
        line += "| "
        for j in range(3):
            line += f"{board[k]} "
            k += 1
        line += "|\n"
    line += "---------"
    print(line)


def analyze(board):
    win = get_winner(board)
    if win is None:
        return True
    if win in ('X', 'O'):
        print(win + " wins")
    else:
        print(win)
    return False


def next_medium(board, ch):
    _moves = [i for i, c in enumerate(board) if c == '_']
    _ch = 'O' if ch == 'X' else 'X'
    print('Making move level "medium"')
    for k in _moves:
        t = board[:k] + ch + board[k + 1:]
        _t = board[:k] + _ch + board[k + 1:]
        if get_winner(t) == ch:
            return t
        elif get_winner(_t) == _ch:
            return t
    shuffle(_moves)
    k = _moves[0]
    t = board[:k] + ch + board[k + 1:]
    return t


def next_easy(board, ch):
    _moves = [i for i, c in enumerate(board) if c == '_']
    shuffle(_moves)
    k = _moves[0]
    t = board[:k] + ch + board[k + 1:]
    print('Making move level "easy"')
    return t


def next_hard(board, ch):
    val, k = minimax(board, ch)
    t = board[:k] + ch + board[k + 1:]
    print('Making move level "hard"')
    return t


def next_user(t, ch):
    while True:
        digs = input("Enter the coordinates: ")
        if not re.match("[1-9] +[1-9]", digs):
            print("You should enter numbers!")
        elif not re.match("[1-3] +[1-3]", digs):
            print("Coordinates should be from 1 to 3!")
        else:
            row, col = digs.split()
            k = 3 * (int(row) - 1) + int(col) -1
            if t[k] == '_':
                t = t[:k] + ch + t[k + 1:]
                return t
            else:
                print("This cell is occupied! Choose another one!")


def game(first, second):
    t = "_________"
    while True:
        if first == 'user':
            t = next_user(t, 'X')
        elif first == 'easy':
            t = next_easy(t, 'X')
        elif first == 'medium':
            t = next_medium(t, 'X')
        else:
            t = next_hard(t, 'X')
        draw(t)
        if not analyze(t):
            break
        if second == 'user':
            t = next_user(t, 'O')
        elif second == 'easy':
            t = next_easy(t, 'O')
        elif second == 'medium':
            t = next_medium(t, 'O')
        else:
            t = next_hard(t, 'O')
        draw(t)
        if not analyze(t):
            break


def main():
    t_board = "_________"
    cmds = {'user', 'easy', 'medium', 'hard'}
    while True:
        cmd = input('Input command: ')
        if cmd == 'exit':
            break
        cmd = cmd.split()
        if len(cmd) < 3 or cmd[0] != 'start' \
                or cmd[1] not in cmds or cmd[2] not in cmds:
            print('Bad parameters!')
            continue
        draw(t_board)
        game(cmd[1], cmd[2])
        break


if __name__ == "__main__":
    main()
