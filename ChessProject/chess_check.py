from board import Board
import math
import copy
def check(board):
    board.print_board() 
    board.move_piece(3,1,3,2)
    board.print_board()
    board.move_piece(2,6,2,5)
    board.print_board()
    board.move_piece(6,0,5,2)
    board.print_board()
    board.move_piece(3,7,0,4)
    board.print_board()

def check_castel(board):
    board.print_board() 
    board.move_piece(4,1,4,3)
    board.print_board()
    board.move_piece(4,6,4,5)
    board.print_board()
    board.move_piece(5,0,2,3)
    board.print_board()
    board.move_piece(5,7,2,4)
    board.print_board()
    board.move_piece(6,0,5,2)
    board.print_board()
    board.move_piece(6,7,5,5)
    board.print_board()
    board.move_piece(4,0,5,0)
    board.print_board()
    board.move_piece(4,7,5,7)
    board.print_board()
def main():
    board = Board()
    board.print_board()
    while True:
        if board.turn:
            """x_from = int(input())
            y_from = int(input())
            x_to = int(input())
            y_to  = int(input())"""
            x_from = 30
            if x_from == 30:
                #a = board.find_best_move(board,0,True)
                a = board.find_best_move(board,0,True)
                print(a[0][0],a[0][1],a[1][0],a[1][1])
                board.move_piece(a[0][0],a[0][1],a[1][0],a[1][1],True)
            else:
                continue
                #board.move_piece(x_from,y_from,x_to,y_to,True)
        else :
            print ("black to play:")
            """x_from = int(input())
            y_from = int(input())
            x_to = int(input())
            y_to  = int(input())"""
            x_from = 30
            if x_from == 30:
                #a = board.find_best_move(board,0,True)
                a = board.find_best_move(board,0,False)
                print(a[0][0],a[0][1],a[1][0],a[1][1])
                board.move_piece(a[0][0],a[0][1],a[1][0],a[1][1],True)
            else:
                continue
                #board.move_piece(x_from,y_from,x_to,y_to,True)


        

        board.print_board()
if __name__ == "__main__":
    main()
