from board import Board
from Grphics import Chess_Game
import threading
import pickle
import copy
import time
copy = lambda obj: pickle.loads(pickle.dumps(obj))

def main():
    game = Chess_Game()
    game.start_game()
    
if __name__ == "__main__":
    t1 = threading.Thread(target=main)
    t1.start()
    
    for i in range(5):
        a =1

    t1.join()
    print('goodBay')
    quit()