X = "X"
O = "O"
EMPTY = ""

# returns starting state of the board
def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

# returns player who has the next turn on a board
def player(board):
    if board == initial_state():
        return X
    
    no_x = 0
    no_o = 0
    for i in board:
        for j in i:
            if j == X:
                no_x += 1
            elif j == O:
                no_o += 1
    
    if no_x > no_o:
        return O
    return X

# pretty prints the board in its current state
def show_board(board):
    for i in board:
        for j in i:
            if j == EMPTY: j = '-'
            print(j, end=' ')
        print()
    print()

# returns set of all possible actions (i, j) available on the board
def actions(board):
    actions = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                actions.add((i, j))
    return actions

# returns the board that results from making move (i, j) on the board
def result(board, action):
    i, j = action
    if board[i][j] != EMPTY:
        return None
    board_copy = list(board)
    board_copy[i][j] = player(board)
    return board_copy

# returns the winner of the game, if there is one
def winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]:
            if board[i][0] == X:
                return X
            elif board[i][0] == O:
                return O

        if board[0][i] == board[1][i] == board[2][i]:
            if board[0][i] == X:
                return X
            elif board[0][i] == O:
                return O

    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == X:
            return X
        elif board[0][0] == O:
            return O

    if board[2][0] == board[1][1] == board[0][2]:
        if board[2][0] == X:
            return X
        elif board[2][0] == O:
            return O

    return EMPTY

# returns True if game is over, False otherwise
def terminal(board):
    for i in board:
        if EMPTY in i:
            break
    else:
        return True

    if winner(board) != EMPTY:
        return True

    return False

# returns 1 if X has won the game, -1 if O has won, 0 otherwise
def utility(board):
    winner_ = winner(board)
    if winner_ == X:
        return 1
    elif winner_ == O:
        return -1
    return 0

# returns the optimal action for the current player on the board
def minimax(board):
    if terminal(board):
        return None
    
    if board == initial_state():
        return (1, 1)

    best = -1000 if player(board) == X else 1000
    for i, j in actions(board):
        if player(board) == X:
            board[i][j] = X
            val = min_value(board, best)
            board[i][j] = ''
            if val > best:
                best = val
                action = (i, j)
        else:
            board[i][j] = O
            val = max_value(board, best)
            board[i][j] = ''
            if val < best:
                best = val
                action = (i, j)
    return action


def max_value(board, best):
    if terminal(board):
        return utility(board)
    
    best = -1000
    for i, j in actions(board):
        board[i][j] = X
        val = min_value(board, best)
        board[i][j] = ''
        best = max(best, val)
    return best

def min_value(board, best):
    if terminal(board):
        return utility(board)
    
    best = 1000
    for i, j in actions(board):
        board[i][j] = O
        val = max_value(board, best)
        board[i][j] = ''
        best = min(best, val)
    return best

while True:
    board = initial_state()
    while True:
        player_ = input('Do you want to play as X or O? (X/O) ')[0].upper()
        if player_ in [X, O]:
            break
        print('Please choose X or O.')
    show_board(board)

    while not terminal(board):
        print(f"{player(board)}'s turn")
        if player_ == player(board):
            while True:
                move = eval(input('Enter move: (row, column) ')) 
                try:
                    i, j = move
                except TypeError:
                    print('Invalid move!')
                    continue
                if not 0<i<=3 or not 0<j<=3:
                    print('Invalid move!')
                    continue
                temp = result(board, (i-1, j-1))
                if temp is None:
                    print('Invalid move!')
                    continue
                board = temp
                break
        else:
            board = result(board, minimax(board))
        show_board(board)

    winner_ = utility(board)
    if winner_ == 1:
        print('X wins!')
    elif winner_ == 0:
        print('Draw!')
    elif winner_ == -1:
        print('O wins!')

    c = input('Play again? (Y/N) ')[0].lower()
    if c == 'n':
        break