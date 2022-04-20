def print_the_board(bd, older_bd):
    whtieCircle = '\u26AA'
    blackCircle = '\u26AB'
    w_sqr = '\u2B1C'
    b_sqr = '\u2B1B'
    line = '\u23E4'

    for i in range(bd.size):
        for j in range(bd.size):

            if bd.board[i][j].value == 'B' and older_bd.board[i][j].value == "_":
                print(blackCircle, end='  ')
            elif bd.board[i][j].value == 'B' and older_bd.board[i][j].value == 'B':
                print(b_sqr, end='  ')

            elif bd.board[i][j].value == 'W' and older_bd.board[i][j].value == 'W':
                print(w_sqr, end='  ')

            elif bd.board[i][j].value == 'W' and older_bd.board[i][j].value == "_":
                print(whtieCircle, end='  ')
            else:
                print(line, end='')
                print(line, end='')
                print(end='  ')

        print()
        print()
