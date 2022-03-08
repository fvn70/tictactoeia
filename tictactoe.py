import re
from random import shuffle

win_combos = (
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6])


def get_winner(board):
    win = None
    if abs(board.count('X') - board.count('O')) > 1:
        return "Impossible"
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


def next_comp(t, ch):
    moves = [i for i, c in enumerate(t) if c == '_']
    shuffle(moves)
    k = moves[0]
    t = t[:k] + ch + t[k + 1:]
    print('Making move level "easy"')
    draw(t)
    return t


def next_user(t, ch):
    while True:
        digs = input("Enter the coordinates: ")
        if not re.match("[1-9] [1-9]", digs):
            print("You should enter numbers!")
        elif not re.match("[1-3] [1-3]", digs):
            print("Coordinates should be from 1 to 3!")
        else:
            row, col = digs.split()
            k = 3 * (int(row) - 1) + int(col) -1
            if t[k] == '_':
                # ch = "X" if isXgo else "O"
                t = t[:k] + ch + t[k + 1:]
                # isXgo = not isXgo
                draw(t)
                return t
            else:
                print("This cell is occupied! Choose another one!")


def main():
    t_board = "_________"
    draw(t_board)
    while True:
        t_board = next_user(t_board, 'X')
        if not analyze(t_board):
            break
        t_board = next_comp(t_board, 'O')


if __name__ == "__main__":
    main()
