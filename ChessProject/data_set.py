import chess.pgn



def convert_move(move):
    y = -1
    for i in range(move):
        if i % 8 == 0:
            y += 1
    if y % 2 == 0 and move <= 32:
        return move - (y * 8) - 1 , y
    elif  move <= 32:
        return 8 - (move - y * 8), y

    if y % 2 == 0 and move > 32:
        return move - (y * 8) , y
    elif  move > 32:
        return 8 - (move - y * 8) + 1, y

if __name__ == "__main__":
    x = 0
    while x!= 70:
        x = int(input())
        a,b = convert_move(x)
        print('x: ',a,'y: ',b)
    quit()
    print ('dvir')
    for i in range(1,2):
        print (i)
        with open(f'data/{i}.pgn','r') as f:
            game = chess.pgn.read_game(f)
            board = game.board()
            print (game.mainline_moves())
            for move in game.mainline_moves():
                board.push(move)
                print(move.from_square,move.to_square)