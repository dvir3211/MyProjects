from board import Board
def evaluate_pos(board):
    sum = 0.0
    for x in range(8):
        for y in  range(8):
            res = 0.0
            if board.board[x][y].get_type == "rook":
                res = 5 + 0.05 * board.count_threts(x,y)
            elif board.board[x][y].type == "knight":
                res = 3 + 0.05 * board.count_threts(x,y)
            elif board.board[x][y].type == "poun":
                res = 1 + 0.05 * board.count_threts(x,y)
            elif board.board[x][y].type == "bishop":
                res = 3.005 + 0.05 * board.count_threts(x,y)
            elif board.board[x][y].type == "king":
                res = 5 + 0.05 * board.count_threts(x,y)
            elif board.board[x][y].type == "queen":
                res = 10 + 0.05 * board.count_threts(x,y)
            if board.board[x][y].color == "black":
                res *= -1
            sum += res
    return sum


if __name__ == "__main__":

    
    board = Board()
    board.print_board()
    while True:
        print("postion value:  ",evaluate_pos(board))
        if board.turn:
            print ("White to play:")
        else :
            print ("Black to play:")
        x_from = int(input())
        if x_from == 10:
            board.undo()
            continue
        y_from = int(input())
        x_to = int(input())
        y_to  = int(input())
        print(x_from,y_from,x_to,y_to)
        board.move_piece(x_from,y_from,x_to,y_to)
        board.print_board()