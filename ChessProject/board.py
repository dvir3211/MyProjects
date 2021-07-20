from tkinter.constants import FALSE, TRUE
from typing import Coroutine
from termcolor import colored
from sty import fg, bg, ef, rs
import math
import pickle
copy = lambda obj: pickle.loads(pickle.dumps(obj))

class thret:
    def __init__(self, type, color,  x, y):
        self.type = type
        self.x = x
        self.y = y
        self.color = color

class Piece:
    def __init__(self, type, color,  x, y):
        self.type = type
        self.x = x
        self.y = y
        self.color = color
        self.thret_list = []

    def append_thret(self, type, color,  x, y):
        if x in range(8) and y in range(8):
            self.thret_list.append(thret(type, color,  x, y))
    def get_color(self):
        return self.color
    def get_type(self):
        return self.type

class Rook(Piece):
    def __init__(self, type, color, x, y,ever_move):
        self.ever_move = ever_move
        super().__init__(type, color, x, y)
        

class King(Piece):
    def __init__(self, type, color, x, y,ever_move):
        self.ever_move = ever_move
        super().__init__(type, color, x, y)
        

class Board:
    def __init__(self):
        self.board = [[0 for x in range(8)] for y in range(8)] 
        self.turn = True
        self.move_list = []
        self.pouns_moves = dict()
        for i in range(8): #define poun
            self.board[i][1] = Piece("poun","white",i,2)
            self.board[i][6] = Piece("poun","black",i,7)
        for x in range(8):
             for y  in range(2,6):
                self.board[x][y] = Piece("#"," ",i,2)
        #define rook
        self.board[0][0] = Rook("rook","white",0,0,False)
        self.board[7][0] = Rook("rook","white",7,0,False)
        self.board[0][7] = Rook("rook","black",0,7,False)
        self.board[7][7] = Rook("rook","black",7,7,False)
    
        #define knight
        self.board[1][0] = Piece("knight","white",1,0)
        self.board[6][0] = Piece("knight","white",6,0)
        self.board[1][7] = Piece("knight","black",1,7)
        self.board[6][7] = Piece("knight","black",6,7)
        
        #define bishop
        self.board[2][0] = Piece("bishop","white",2,0)
        self.board[5][0] = Piece("bishop","white",5,0)
        self.board[2][7] = Piece("bishop","black",2,7)
        self.board[5][7] = Piece("bishop","black",5,7)
        
        #define king
        self.board[4][0] = King("King","white",4,0,False)
        self.board[4][7] = King("King","black",4,7,False)
        
        #define queen
        self.board[3][0] = Piece("Queen","white",3,0)
        self.board[3][7] = Piece("Queen","black",3,7)
    
    """def __init__(self,board1:Board):
        self.__init__()
        for x in range(8):
            for y in range (8):
                    self.board[x][y].type = board1.board[x][y].type
                    self.board[x][y].x = board1.board[x][y].x
                    self.board[x][y].y = board1.board[x][y].y
                    self.board[x][y].color = board1.board[x][y].color
"""
    def clear_threts(self):
            for x in range(8):
                for y in range(8):
                    self.board[x][y].thret_list.clear()

    def copy_board(self,board):
        for x in range(8):
            for y in range(8):
                self.board[x][y] = board[x][y]

    def move_piece(self, x_from, y_from, x_to, y_to, real_move = True):
        if self.turn:
            turn_color = 'white'
        else :
            turn_color = 'black'
        if self.board[x_from][y_from].color != turn_color:
            print("Its not your piece\n")
            return False
        if not self.is_leagal_move( x_from, y_from, x_to, y_to,real_move)  :#The actual move of the piece is inside is_leagal_move func
            print("Cant play this move put another one!\n")
            return False
        elif real_move:
            self.turn = not self.turn
        self.threts()
        
        return True
        #self.set_piece(self.board[x_from][y_from],self.board[x_to][y_to])
 
    def set_piece(self,from_piece,to_piece):

        if from_piece.type == 'King':
            self.board[ to_piece.x][to_piece.y] = King('King',from_piece.color,from_piece.x,from_piece.y,True)
        elif from_piece.type == 'rook':
            self.board[ to_piece.x][to_piece.y] = Rook('rook',from_piece.color,from_piece.x,from_piece.y,True)
        else:
            to_piece.type =  from_piece.type
            to_piece.x =  from_piece.x
            to_piece.y =  from_piece.y
            to_piece.color =  from_piece.color

        from_piece.type = "#"
        from_piece.color = "#"
  
    def get_square_color(self,x,y):
        foo = bg.white
        if ((x +1) % 2) == 0 and ((y + 1) % 2) == 0 or ((x +1) % 2) != 0 and ((y + 1) % 2) != 0 :
            foo = bg.da_black
        return foo
    
    def is_leagal_move(self, x_from, y_from, x_to, y_to,real_move):
        # check the cordinates
        if x_from not in range(8) or y_from not in range(8) or x_to not in range(8) or y_to not in range(8):
            return False
        piece_type = self.board[x_from][y_from].type
        # check if the coordinates are empty
        if piece_type == "#":
            return False
        # check if is the same color
        if x_from == x_to and y_from == y_to:
            return False
        if self.board[x_from][y_from].color == self.board[x_to][y_to].color:
            return False
        #if (self.turn and self.board[x_from][y_from].color != "white" or not self.turn and self.board[x_from][y_from].color != "black") and real_move:
        #    print("Its not your piece!")
        #    return False
        bool = False
        if piece_type == "poun" :
            ret_val = self.poun_move(x_from, y_from, x_to, y_to)
            bool = ret_val[0]
            if self.is_check()[0]:
                if not self.is_block_check(x_from, y_from, x_to, y_to):
                    if real_move:
                        print("You cant move this piece you steel in check!")
                    return False
            elif self.is_pined(x_from, y_from, x_to, y_to):
                if real_move:
                    print("This piece is pined!")
                return False
            if bool and real_move:
                self.append_move()
                if ret_val[1] == "pasan":
                    self.board[x_to][y_from].color = "#"
                    self.board[x_to][y_from].type = "#"
                self.set_piece(self.board[x_from][y_from],self.board[x_to][y_to]) 
        elif piece_type == "rook" :
            bool =  self.rook_move(x_from, y_from, x_to, y_to)
            if self.is_check()[0]:
                if not self.is_block_check(x_from, y_from, x_to, y_to):
                    if real_move:
                        print("You cant move this piece you steel in check!")
                    return False
            elif self.is_pined(x_from, y_from, x_to, y_to):
                if real_move:
                    print("This piece is pined!")
                return False 
            if bool and real_move:
                self.append_move()
                self.board[x_from][y_from].ever_move = True
                self.set_piece(self.board[x_from][y_from],self.board[x_to][y_to])
        elif piece_type == "bishop" :
            bool = self.bishop_move(x_from, y_from, x_to, y_to)
            if self.is_check()[0]:
                if not self.is_block_check(x_from, y_from, x_to, y_to):
                    if real_move:
                        print("You cant move this piece you steel in check!")
                    return False
            elif self.is_pined(x_from, y_from, x_to, y_to):
                if real_move:
                    print("This piece is pined!")
                return False
            if bool and real_move:
                self.append_move()
                self.set_piece(self.board[x_from][y_from],self.board[x_to][y_to]) 
        elif piece_type == "knight" :
            bool = self.knight_move(x_from, y_from, x_to, y_to)
            if self.is_check()[0]:
                if not self.is_block_check(x_from, y_from, x_to, y_to):
                    if real_move:
                        print("You cant move this piece you steel in check!")
                    return False
            elif self.is_pined(x_from, y_from, x_to, y_to):
                if real_move:
                    if real_move:
                        print("You cant move this piece you steel in check!")
                return False
            if bool and real_move:
                self.set_piece(self.board[x_from][y_from],self.board[x_to][y_to])  
        elif piece_type == "King" :
            ret_val = self.king_move(x_from, y_from, x_to, y_to)
            bool = ret_val[0]
            if ret_val[1] != "none" and real_move:
                self.append_move()
                self.castel(ret_val[1],ret_val[2])
            elif bool and real_move:
                self.append_move()
                self.board[x_from][y_from].ever_move = True
                self.set_piece(self.board[x_from][y_from],self.board[x_to][y_to])          
        elif piece_type == "Queen" :

            bool = self.queen_move(x_from, y_from, x_to, y_to)
            if self.is_check()[0]:
                if not self.is_block_check(x_from, y_from, x_to, y_to):
                    if real_move:
                        print("You cant move this piece you steel in check!")
                    return False
            elif self.is_pined(x_from, y_from, x_to, y_to):
                if real_move:
                    print("This piece is pined!")
                return False 
            if bool and real_move:
                self.append_move()
                self.set_piece(self.board[x_from][y_from],self.board[x_to][y_to])    
       
        return bool 
    
    def poun_move(self, x_from, y_from, x_to, y_to):
        color = self.board[x_from][y_from].color
        if color == "black":
            if y_from < y_to:
                return (False,"none")
            if self.is_empty(x_to,y_to) :
                if y_from-y_to == 1 and abs(x_from-x_to)== 1 :
                    if self.board[x_to][y_from].type =="poun" and self.board[x_to][y_from].color =="white" and self.move_list[len(self.move_list)-1][x_to][1].type == "poun":
                        return (True,"pasan")
                if x_from != x_to or y_from - y_to > 2:
                    return (False,"none")
                if y_from - y_to == 2:
                    if y_from != 6:
                        return (False,"none")
                    if  not self.is_empty(x_to,y_to+1):
                        return (False,"none")
            elif y_from-y_to != 1 or abs(x_from-x_to)!= 1:
                    return (False,"none")
        elif color == "white":
            if y_from > y_to:
                return (False,"none")
            if self.is_empty(x_to,y_to) :
                if y_to - y_from == 1 and abs(x_from-x_to)== 1 :
                    if self.board[x_to][y_from].type =="poun" and self.board[x_to][y_from].color =="black" and self.move_list[len(self.move_list)-1][x_to][6].type == "poun":
                        return (True,"pasan")
                if x_from != x_to or y_to - y_from > 2:
                    return (False,"none")
                if y_to - y_from == 2:
                    if y_from != 1:
                        return (False,"none")
                    if  not self.is_empty(x_to,y_to-1):
                        return (False,"none") 
            elif y_to - y_from != 1 or abs(x_from-x_to)!= 1:
                    return (False,"none")    
        return (True,"none")
    
    def is_empty(self, x, y):
        if self.board[x][y].type == "#":
            return True
        return False

    def knight_move(self, x_from, y_from, x_to, y_to):
        
        if abs(x_to-x_from) == 1 and abs(y_to-y_from)==2 or abs(x_to-x_from) == 2 and abs(y_to-y_from)==1:
            return True
        return False
        
    def bishop_move(self, x_from, y_from, x_to, y_to):
        if abs(x_from-x_to) != abs(y_from-y_to):
            return False
        if x_from > x_to and y_from > y_to:
            for i in range (1, abs(x_from-x_to) + 1):
                if self.board[x_from - i][y_from -i].type != "#" and i != abs(x_from-x_to)  :
                    return False
        elif x_from > x_to and y_from < y_to:
            for i in range (1, abs(x_from-x_to) + 1):
                if self.board[x_from - i][y_from + i].type != "#" and i != abs(x_from-x_to):
                    return False
        elif x_from < x_to and y_from < y_to:
            for i in range (1, abs(x_from-x_to) + 1):
                if self.board[x_from + i][y_from + i].type != "#" and i != abs(x_from-x_to):
                    return False
        elif x_from < x_to and y_from > y_to:
            for i in range (1, abs(x_from-x_to) + 1):
                if self.board[x_from + i][y_from - i].type != "#" and i != abs(x_from-x_to):
                    return False
        return True
    
    def rook_move(self, x_from, y_from, x_to, y_to):
        if x_from != x_to and y_from != y_to:
            return False
        if x_from == x_to and y_from > y_to:
            for i in range(1,abs(y_from - y_to)+1):
                if self.board[x_from][y_from - i].type != "#" and i != abs(y_from - y_to):
                    return False
        elif x_from == x_to and y_from < y_to:
            for i in range(1,abs(y_from - y_to)+1):
                if self.board[x_from][y_from + i].type != "#" and i != abs(y_from - y_to):
                    return False
        elif x_from > x_to and y_from == y_to:
            for i in range(1,abs(x_from-x_to)+1):
                if self.board[x_from - i][y_from].type != "#" and i != abs(x_from-x_to):
                    return False
        elif x_from < x_to and y_from == y_to:
            for i in range(1,abs(x_from-x_to)+1):
                if self.board[x_from + i][y_from ].type != "#" and i != abs(x_from-x_to):
                    return False

        return True
    
    def king_move(self, x_from, y_from, x_to, y_to):
        self.threts()
        if self.board[x_from][y_from].type != "King":
            return (False,"none")
        if x_to not in range(8) or y_to not in range(8):
            return (False,"none")
        if self.board[x_to][y_to].color == self.board[x_from][y_from].color:
            return (False,"none")
        if abs(x_from-x_to)> 1 or abs(y_from-y_to)>1:
            if y_to != y_from or abs(x_from-x_to)!= 2:
                return (False,"none")
        if self.board[x_to][y_to].color == self.board[x_from][y_from].color:
           return (False,"none")
        for  x in self.board[x_to][y_to].thret_list:
            #print("thret color: ",x.color,"\nking color: ",self.board[x_from][y_from].color,f"x:{x.x},y:{x.y}")
            if x.color != self.board[x_from][y_from].color:
                return (False,"none")
            #check if castle avelible
        if self.is_check()[0]:
                if self.is_pined(x_from, y_from, x_to, y_to):
                    print("This piece is pined!")
                    return (False,"none")
        if (y_to == y_from) and abs(x_from - x_to) ==2  :
            if self.board[x_from][y_from].ever_move or self.is_check()[0]:
                return (False,"none")
            if y_from == 7: 
                if x_from > x_to:
                    if self.board[0][7].type != "rook":
                        return (False,"none")
                    if self.board[0][7].ever_move:
                        return (False,"none")
                    for i in range(1,4):
                        if self.board[x_from-i][y_from].color != "#":
                            return (False,"none")
                        if i <=2:
                            for  x in self.board[x_from-i][y_from].thret_list:
                                if x.color != self.board[x_from][y_from].color:
                                    return (False,"none")
                    return (True,self.board[x_from][y_from].color,"long")
                elif x_from < x_to:
                    if self.board[7][7].type != "rook":
                        return (False,"none")
                    if self.board[7][7].ever_move:
                        return (False,"none")
                    for i in range(1,3):
                        if self.board[x_from+i][y_from].color != "#":
                            return (False,"none")
                        for  x in self.board[x_from+i][y_from].thret_list:
                            if x.color != self.board[x_from][y_from].color:
                                return (False,"none")
                    return (True,self.board[x_from][y_from].color,"short")
            elif y_from == 0:
                if x_from > x_to:
                    if self.board[0][0].type != "rook":
                        return (False,"none")
                    if self.board[0][0].ever_move:
                        return (False,"none")
                    for i in range(1,4):
                        if self.board[x_from-i][y_from].color != "#":
                            return (False,"none")
                        if i <=2:
                            for  x in self.board[x_from-i][y_from].thret_list:
                                if x.color != self.board[x_from][y_from].color:
                                    return (False,"none")
                    return (True,self.board[x_from][y_from].color,"long")
                elif x_from < x_to:
                    if self.board[7][0].type != "rook":
                        return (False,"none")
                    if self.board[7][0].ever_move:
                        return (False,"none")
                    for i in range(1,3):
                        if self.board[x_from+i][y_from].color != "#":
                            return (False,"none")
                        for  x in self.board[x_from+i][y_from].thret_list:
                            if x.color != self.board[x_from][y_from].color:
                                return (False,"none")   
                    return (True,self.board[x_from][y_from].color,"short")
        return (True,"none")

    def castel(self,color,type):
        if color == "black":
            if type == "long":
                self.set_piece(self.board[4][7],self.board[2][7])#king
                self.set_piece(self.board[0][7],self.board[3][7])#rook
            elif type == "short":
                self.set_piece(self.board[4][7],self.board[6][7])#king
                self.set_piece(self.board[7][7],self.board[5][7])#rook
        elif color == "white":
            if type == "long":
                self.set_piece(self.board[4][0],self.board[2][0])#king
                self.set_piece(self.board[0][0],self.board[3][0])#rook
            elif type == "short":
                self.set_piece(self.board[4][0],self.board[6][0])#king
                self.set_piece(self.board[7][0],self.board[5][0])#rook

    def queen_move(self, x_from, y_from, x_to, y_to):
        if self.bishop_move( x_from, y_from, x_to, y_to) or self.rook_move(x_from, y_from, x_to, y_to):
            #self.set_piece(self.board[x_from][y_from],self.board[x_to][y_to])
            return True
        return False

    def count_threts(self,x,y):
        threts = 0
        piece_type = self.board[x][y].type
        piece_color = self.board[x][y].color
        if piece_type == "poun" :
            if piece_color == "white":
                if (x + 1)  in range(8) and (y + 1)  in range(8):
                    threts += 1
                if (x - 1)  in range(8) and (y + 1)  in range(8):
                    threts += 1
            elif piece_color == "black":
                if (x + 1)  in range(8) and (y - 1)  in range(8):
                    threts += 1
                if (x - 1)  in range(8) and (y - 1)  in range(8):
                    threts += 1  
        elif piece_type == "rook" :
                    for i in range(x+1,8):
                        if self.board[i][y].type !="#":
                            threts += 1
                            break
                        threts += 1
                    for i in range(x-1,-1,-1):
                        if self.board[i][y].type !="#":
                            threts += 1
                            break
                        threts += 1
                    for i in range(y+1,8):
                        if self.board[x][i].type !="#":
                            threts += 1
                            break
                        threts += 1
                    for i in range(y-1,-1,-1):
                        if self.board[x][i].type !="#":
                            threts += 1
                            break
                        threts += 1
        elif piece_type == "bishop" :
                    for i in range(1,8):
                        if (x + i) not in range(8) or (y + i) not in range(8):
                            break
                        if self.board[x+i][y+i].type !="#":
                            threts += 1
                            break
                        threts += 1
                    for i in range(1,8):
                        if (x - i) not in range(8) or (y - i) not in range(8):
                            break
                        if self.board[x-i][y-i].type !="#":
                            threts += 1
                            break
                        threts += 1
                    for i in range(1,8):
                        if (x + i) not in range(8) or (y - i) not in range(8):
                            break
                        if self.board[x+i][y-i].type !="#":
                            threts += 1
                            break
                        threts += 1
                    for i in range(1,8):
                        if (x - i) not in range(8) or (y + i) not in range(8):
                            break
                        if self.board[x-i][y+i].type !="#":
                            threts += 1
                            break
                        threts += 1
        elif piece_type == "knight" :
                    if (x + 1)  in range(8) and (y + 2)  in range(8):
                        threts += 1
                    
                    if (x + 1) in range(8) and (y - 2)  in range(8):
                        threts += 1
                    
                    if (x + 2)  in range(8) and (y + 1)  in range(8):
                        threts += 1
                    
                    if (x + 2)  in range(8) and (y - 1)  in range(8):
                        threts += 1
                    
                    if (x - 1) in range(8) and (y + 2)  in range(8):
                       threts += 1
                    if (x - 1) in range(8) and (y - 2) in range(8):
                        threts += 1
                    if (x - 2) in range(8) and (y + 1)  in range(8):
                       threts += 1
                    
                    if (x - 2) in range(8) and (y - 1)  in range(8):
                        threts += 1
        elif piece_type == "King" :
                    if (x + 1)  in range(8) and (y + 1)  in range(8):
                       threts += 1
                    
                    if (x)  in range(8) and (y - 1) in range(8):
                        threts += 1
                    
                    if (x)  in range(8) and (y + 1)  in range(8):
                       threts += 1
                    if (x + 1)  in range(8) and (y)  in range(8):
                        threts += 1
                    
                    if (x - 1)  in range(8) and (y) in range(8):
                        threts += 1
                    
                    if (x - 1)  in range(8) and (y - 1)  in range(8):
                        threts += 1
                    if (x - 1) in range(8) and (y + 1)  in range(8):
                        threts += 1
                    
                    if (x + 1)  in range(8) and (y - 1) in range(8):
                        threts += 1
        elif piece_type == "Queen" :
                    for i in range(1,8):
                        if (x + i) not in range(8) or (y + i) not in range(8):
                            break
                        if self.board[x+i][y+i].type !="#":
                            threts += 1
                            break
                        threts += 1
                    for i in range(1,8):
                        if (x - i) not in range(8) or (y - i) not in range(8):
                            break
                        if self.board[x-i][y-i].type !="#":
                            threts += 1
                            break
                        threts += 1
                    for i in range(1,8):
                        if (x + i) not in range(8) or (y - i) not in range(8):
                            break
                        if self.board[x+i][y-i].type !="#":
                            threts += 1
                            break
                        threts += 1
                    for i in range(1,8):
                        if (x - i) not in range(8) or (y + i) not in range(8):
                            break
                        if self.board[x-i][y+i].type !="#":
                            threts += 1
                            break
                        threts += 1
                    for i in range(1,8):
                        if (x + i) not in range(8) or (y - i) not in range(8):
                            break
                        if self.board[x+i][y-i].type !="#":
                            threts += 1
                            break
                        threts += 1 
                    for i in range(x+1,8):
                        if self.board[i][y].type !="#":
                            threts += 1
                            break
                        threts += 1
                    for i in range(x-1,-1,-1):
                        if self.board[i][y].type !="#":
                            threts += 1
                            break
                        threts += 1
                    for i in range(y+1,8):
                        if self.board[x][i].type !="#":
                            threts += 1
                            break
                        threts += 1
                    for i in range(y-1,-1,-1):
                        if self.board[x][i].type !="#":
                            threts += 1
                            break
                        threts += 1
        return threts

    def threts(self):
        self.clear_threts()
        for x in range(8):
            for y in range(8):
                square = self.board[x][y]
                piece_type = square.type
                piece_color =square.color
                
                if piece_type == "poun" :
                    if piece_color == "white":
                        if (x + 1)  in range(8) and (y + 1)  in range(8):
                            self.board[x+1][y+1].append_thret(piece_type,piece_color,x,y)
                        if (x - 1)  in range(8) and (y + 1)  in range(8):
                            self.board[x-1][y+1].append_thret(piece_type,piece_color,x,y)
                    elif piece_color == "black":
                        if (x + 1)  in range(8) and (y - 1)  in range(8):
                            self.board[x+1][y-1].append_thret(piece_type,piece_color,x,y)
                        if (x - 1)  in range(8) and (y - 1)  in range(8):
                            self.board[x-1][y-1].append_thret(piece_type,piece_color,x,y)  
                elif piece_type == "rook" :
                    for i in range(x+1,8):
                        if self.board[i][y].type !="#":
                            self.board[i][y].append_thret(piece_type,piece_color,x,y)
                            break
                        self.board[i][y].append_thret(piece_type,piece_color,x,y)
                    for i in range(x-1,-1,-1):
                        if self.board[i][y].type !="#":
                            self.board[i][y].append_thret(piece_type,piece_color,x,y)
                            break
                        self.board[i][y].append_thret(piece_type,piece_color,x,y)
                    for i in range(y+1,8):
                        if self.board[x][i].type !="#":
                            self.board[x][i].append_thret(piece_type,piece_color,x,y)
                            break
                        self.board[x][i].append_thret(piece_type,piece_color,x,y)
                    for i in range(y-1,-1,-1):
                        if self.board[x][i].type !="#":
                            self.board[x][i].append_thret(piece_type,piece_color,x,y)
                            break
                        self.board[x][i].append_thret(piece_type,piece_color,x,y)      
                elif piece_type == "bishop" :
                    for i in range(1,8):
                        if (x + i) not in range(8) or (y + i) not in range(8):
                            break
                        if self.board[x+i][y+i].type !="#":
                            self.board[x+i][y+i].append_thret(piece_type,piece_color,x,y)
                            break
                        self.board[x+i][y+i].append_thret(piece_type,piece_color,x,y)
                    for i in range(1,8):
                        if (x - i) not in range(8) or (y - i) not in range(8):
                            break
                        if self.board[x-i][y-i].type !="#":
                            self.board[x-i][y-i].append_thret(piece_type,piece_color,x,y)
                            break
                        self.board[x-i][y-i].append_thret(piece_type,piece_color,x,y)
                    for i in range(1,8):
                        if (x + i) not in range(8) or (y - i) not in range(8):
                            break
                        if self.board[x+i][y-i].type !="#":
                            self.board[x+i][y-i].append_thret(piece_type,piece_color,x,y)
                            break
                        self.board[x+i][y-i].append_thret(piece_type,piece_color,x,y)
                    for i in range(1,8):
                        if (x - i) not in range(8) or (y + i) not in range(8):
                            break
                        if self.board[x-i][y+i].type !="#":
                            self.board[x-i][y+i].append_thret(piece_type,piece_color,x,y)
                            break
                        self.board[x-i][y+i].append_thret(piece_type,piece_color,x,y)      
                elif piece_type == "knight" :
                    if (x + 1)  in range(8) and (y + 2)  in range(8):
                        self.board[x+1][y+2].append_thret(piece_type,piece_color,x,y)
                    
                    if (x + 1) in range(8) and (y - 2)  in range(8):
                        self.board[x+1][y-2].append_thret(piece_type,piece_color,x,y)
                    
                    if (x + 2)  in range(8) and (y + 1)  in range(8):
                        self.board[x+2][y+1].append_thret(piece_type,piece_color,x,y)
                    
                    if (x + 2)  in range(8) and (y - 1)  in range(8):
                        self.board[x+2][y-1].append_thret(piece_type,piece_color,x,y)
                    
                    if (x - 1) in range(8) and (y + 2)  in range(8):
                        self.board[x-1][y+2].append_thret(piece_type,piece_color,x,y)
                    
                    if (x - 1) in range(8) and (y - 2) in range(8):
                        self.board[x-1][y-2].append_thret(piece_type,piece_color,x,y)
                    
                    if (x - 2) in range(8) and (y + 1)  in range(8):
                        self.board[x-2][y+1].append_thret(piece_type,piece_color,x,y)
                    
                    if (x - 2) in range(8) and (y - 1)  in range(8):
                        self.board[x - 2][y -1].append_thret(piece_type,piece_color,x,y)
                elif piece_type == "King" :
                    if (x + 1)  in range(8) and (y + 1)  in range(8):
                        self.board[x+1][y+1].append_thret(piece_type,piece_color,x,y)
                    
                    if (x)  in range(8) and (y - 1) in range(8):
                        self.board[x][y-1].append_thret(piece_type,piece_color,x,y)
                    
                    if (x)  in range(8) and (y + 1)  in range(8):
                        self.board[x][y+1].append_thret(piece_type,piece_color,x,y)
                    
                    if (x + 1)  in range(8) and (y)  in range(8):
                        self.board[x+1][y].append_thret(piece_type,piece_color,x,y)
                    
                    if (x - 1)  in range(8) and (y) in range(8):
                        self.board[x-1][y].append_thret(piece_type,piece_color,x,y)
                    
                    if (x - 1)  in range(8) and (y - 1)  in range(8):
                        self.board[x-1][y-1].append_thret(piece_type,piece_color,x,y)
                    
                    if (x - 1) in range(8) and (y + 1)  in range(8):
                        self.board[x-1][y+1].append_thret(piece_type,piece_color,x,y)
                    
                    if (x + 1)  in range(8) and (y - 1) in range(8):
                        self.board[x+1][y-1].append_thret(piece_type,piece_color,x,y)
                elif piece_type == "Queen" :
                    for i in range(1,8):
                        if (x + i) not in range(8) or (y + i) not in range(8):
                            break
                        if self.board[x+i][y+i].type !="#":
                            self.board[x+i][y+i].append_thret(piece_type,piece_color,x,y)
                            break
                        self.board[x+i][y+i].append_thret(piece_type,piece_color,x,y)
                    for i in range(1,8):
                        if (x - i) not in range(8) or (y - i) not in range(8):
                            break
                        if self.board[x-i][y-i].type !="#":
                            self.board[x-i][y-i].append_thret(piece_type,piece_color,x,y)
                            break
                        self.board[x-i][y-i].append_thret(piece_type,piece_color,x,y)
                    for i in range(1,8):
                        if (x + i) not in range(8) or (y - i) not in range(8):
                            break
                        if self.board[x+i][y-i].type !="#":
                            self.board[x+i][y-i].append_thret(piece_type,piece_color,x,y)
                            break
                        self.board[x+i][y-i].append_thret(piece_type,piece_color,x,y)
                    for i in range(1,8):
                        if (x - i) not in range(8) or (y + i) not in range(8):
                            break
                        if self.board[x-i][y+i].type !="#":
                            self.board[x-i][y+i].append_thret(piece_type,piece_color,x,y)
                            break
                        self.board[x-i][y+i].append_thret(piece_type,piece_color,x,y) 
                    for i in range(1,8):
                        if (x + i) not in range(8) or (y - i) not in range(8):
                            break
                        if self.board[x+i][y-i].type !="#":
                            self.board[x+i][y-i].append_thret(piece_type,piece_color,x,y)
                            break
                        self.board[x+i][y-i].append_thret(piece_type,piece_color,x,y) 
                    for i in range(x+1,8):
                        if self.board[i][y].type !="#":
                            self.board[i][y].append_thret(piece_type,piece_color,x,y)
                            break
                        self.board[i][y].append_thret(piece_type,piece_color,x,y)
                    for i in range(x-1,-1,-1):
                        if self.board[i][y].type !="#":
                            self.board[i][y].append_thret(piece_type,piece_color,x,y)
                            break
                        self.board[i][y].append_thret(piece_type,piece_color,x,y)
                    for i in range(y+1,8):
                        if self.board[x][i].type !="#":
                            self.board[x][i].append_thret(piece_type,piece_color,x,y)
                            break
                        self.board[x][i].append_thret(piece_type,piece_color,x,y)
                    for i in range(y-1,-1,-1):
                        if self.board[x][i].type !="#":
                            self.board[x][i].append_thret(piece_type,piece_color,x,y)
                            break
                        self.board[x][i].append_thret(piece_type,piece_color,x,y)        
  
    def print_board(self):
        print("Black Side:")
        
        for y in range(7,-1,-1):
            foo = fg.red 
            print(y," ", end="", flush=True)
            for x  in range(0,8):
                if self.board[x][y].color == "white":
                    #foo = fg.blue + self.get_square_color(x,y) + self.board[x][y].type[0] + bg.rs + fg.rs
                    foo = fg.white + self.board[x][y].type[0] + fg.rs
                elif  self.board[x][y].color == "black": 
                    #foo = fg.green + self.get_square_color(x,y) + self.board[x][y].type[0] + bg.rs + fg.rs
                    foo = fg.black  + self.board[x][y].type[0] + fg.rs
                else  : 
                    foo = fg.black + self.get_square_color(x,y) + " " + bg.rs + fg.rs
                
                print(foo,"  ", end="", flush=True)
            print("")
        for x  in range(0,8):
            print("  ", x, end="", flush=True)
        print("\nWhite Side:")
        print(" ")
    
    def is_pined(self, x_from, y_from, x_to, y_to):
        color_from = self.board[x_from][y_from].color
        type_from = self.board[x_from][y_from].type
        color_to = self.board[x_to][y_to].color
        type_to = self.board[x_to][y_to].type

        self.set_piece(self.board[x_from][y_from],self.board[x_to][y_to])

        x = self.is_check()

        self.set_piece(self.board[x_to][y_to],self.board[x_from][y_from])
        self.board[x_to][y_to].color = color_to
        self.board[x_to][y_to].type = type_to


        #print("turn:",self.turn,"x[0]:",x[0],"x[1]:",x[1])
        #print("color: ",color_from,"type:  ",type_from)
        if self.turn and x[0] and x[1] == "white":
            return True
            
        elif not self.turn and x[0] and x[1] == "black":
            return True   
        return False
    
    def leagal_moves(self,x_from,y_from):
        leagal = []
        for x in range(8):
            for y in range(8):
                if self.is_leagal_move(x_from,y_from,x,y,False):
                    leagal.append([x,y])
        return leagal
                
    def is_block_check(self, x_from, y_from, x_to, y_to):

        color = self.board[x_to][y_to].color
        type = self.board[x_to][y_to].type
        self.board[x_to][y_to].type = self.board[x_from][y_from].type
        self.board[x_to][y_to].color = self.board[x_from][y_from].color
        

        x = self.is_check()

        self.board[x_to][y_to].type = type
        self.board[x_to][y_to].color = color
        #print("turn:",self.turn,"x[0]:",x[0],"x[1]:",x[1])
        if self.turn and x[0] and x[1] == "white":
            return False
            
        elif not self.turn and x[0] and x[1] == "black":
            return False   
        return True
    
    def is_check(self):
        self.threts()
        for x in range(8):
            for y in range(8):
                if self.board[x][y].type == "King":
                    for  i in self.board[x][y].thret_list:
                        if i.color != self.board[x][y].color:
                            return (True,self.board[x][y].color)
        return (False, "none")

    def get_squere(self,x,y):
        return self.board[x][y]
    
    def set_new_piece(self,x,y,type,color):
        self.board[x][y].type = type
        self.board[x][y].color = color
        self.board[x][y].x = x
        self.board[x][y].y = y

    def undo(self):
        print(len(self.move_list))
        if  len(self.move_list) > 0:
            a = self.move_list.pop()
            #a.print_board()
            for x in range(8):
                for y in range(8):
                    #self.set_new_piece(x,y,a[x][y].get_type(),a[x][y].get_color())
                    self.board[x][y].color = a[x][y].get_color()
                    self.board[x][y].type = a[x][y].get_type()
                    
            self.turn = not self.turn

    def is_check_mate(self,color):
        
        #This function called after there is check
        pos = self.king_pos(color)
        #print("x:  ",pos[0],"y:  ", pos[1],"color:  ", color)
        x,y = pos[0],pos[1]
        if self.is_king_can_move(x,y):
            return False
        self.pouns()
        #The king cant move
        i = 1
        for thret in self.board[x][y].thret_list:
            if thret.color == color:
                continue
            if thret.type == "rook":
                if thret.x == x:
                    if thret.y > y:
                        for t in range(1,abs(thret.y - y)+1):
                            for a in self.board[x][y+t].thret_list:
                                if a.color == color and a.type != "King" and a.type != "poun":
                                    if not self.is_pined(a.x,a.y,x,y+t):
                                        return False
                                if x == thret.x and y+t == thret.y and a.type == "poun":
                                    if not self.is_pined(a.x,a.y,x,y+t):
                                        return False
                                if (x,y+t) in self.pouns_moves:
                                    if not self.is_pined(self.pouns_moves[(x,y+t)][0],self.pouns_moves[(x,y+t)][1],x,y+t):
                                        return False
                    elif thret.y < y:
                        for t in range(1,abs(thret.y - y)+1):
                            for a in self.board[x][y-t].thret_list:
                                if a.color == color and a.type != "King" and a.type != "poun":
                                    if not self.is_pined(a.x,a.y,x,y-t):
                                        return False
                                if x == thret.x and y-t == thret.y and a.type == "poun":
                                    if not self.is_pined(a.x,a.y,x,y-t):
                                        return False
                                if (x,y-t) in self.pouns_moves:
                                    if not self.is_pined(self.pouns_moves[(x,y-t)][0],self.pouns_moves[(x,y-t)][1],x,y-t):
                                        return False
                elif thret.y == y:
                    if thret.x > x:
                        for t in range(1,abs(thret.x - x)+1):
                            for a in self.board[x+t][y].thret_list:
                                if a.color == color and a.type != "King" and a.type != "poun":
                                    if not self.is_pined(a.x,a.y,x+t,y):
                                        return False
                                if x+t == thret.x and y == thret.y and a.type == "poun":
                                    if not self.is_pined(a.x,a.y,x+t,y):
                                        return False
                                if (x+t,y) in self.pouns_moves:
                                    if not self.is_pined(self.pouns_moves[(x+t,y)][0],self.pouns_moves[(x+t,y)][1],x+t,y):
                                        return False
                    elif thret.x < x:
                        for t in range(1,abs(thret.x - x)+1):
                            for a in self.board[x-t][y].thret_list:
                                if a.color == color and a.type != "King" and a.type != "poun":
                                    if not self.is_pined(a.x,a.y,x-t,y):
                                        return False
                                if x-t == thret.x and y == thret.y and a.type == "poun":
                                    if not self.is_pined(a.x,a.y,x-t,y):
                                        return False
                                if (x-t,y) in self.pouns_moves:
                                    if not self.is_pined(self.pouns_moves[(x-t,y)][0],self.pouns_moves[(x-t,y)][1],x-t,y):
                                        return False 
            elif thret.type == "bishop":
                if thret.x > x and thret.y > y:
                    for t in range(1,abs(thret.y - y)+1):
                            for a in self.board[x+t][y+t].thret_list:
                                if a.color == color and a.type != "King" and a.type != "poun"  :
                                    if not self.is_pined(a.x,a.y,x+t,y+t):
                                        return False
                                if x+t == thret.x and y+t == thret.y and a.type == "poun":
                                    if not self.is_pined(a.x,a.y,x+t,y+t):
                                        return False
                                if (x+t,y+t) in self.pouns_moves:
                                    print("poun x: ",self.pouns_moves[(x+t,y+t)][0],"poun y: ",self.pouns_moves[(x+t,y+t)][1])
                                    if not self.is_pined(self.pouns_moves[(x+t,y+t)][0],self.pouns_moves[(x+t,y+t)][1],x+t,y+t):
                                        return False
                elif thret.x < x and thret.y < y:
                    for t in range(1,abs(thret.y - y)+1):
                            for a in self.board[x-t][y-t].thret_list:
                                if a.color == color and a.type != "King" and a.type != "poun":
                                    if not self.is_pined(a.x,a.y,x-t,y-t):
                                        return False   
                                if x-t == thret.x and y-t == thret.y and a.type == "poun":
                                    if not self.is_pined(a.x,a.y,x-t,y-t):
                                        return False
                                if (x-t,y-t) in self.pouns_moves:
                                    if not self.is_pined(self.pouns_moves[(x-t,y-t)][0],self.pouns_moves[(x-t,y-t)][1],x-t,y-t):
                                        return False
                elif thret.x > x and thret.y < y:
                    for t in range(1,abs(thret.y - y)+1):
                            for a in self.board[x+t][y-t].thret_list:
                                if a.color == color and a.type != "King" and a.type != "poun":
                                    if not self.is_pined(a.x,a.y,x+t,y-t):
                                        return False
                                if x+t == thret.x and y-t == thret.y and a.type == "poun":
                                    if not self.is_pined(a.x,a.y,x+t,y-t):
                                        return False
                                if (x+t,y-t) in self.pouns_moves:
                                    if not self.is_pined(self.pouns_moves[(x+t,y-t)][0],self.pouns_moves[(x+t,y-t)][1],x+t,y-t):
                                        return False
                elif thret.x < x and thret.y > y:
                    for t in range(1,abs(thret.y - y)+1):
                            for a in self.board[x-t][y+t].thret_list:
                                if a.color == color and a.type != "King" and a.type != "poun":
                                    if not self.is_pined(a.x,a.y,x-t,y+t):
                                        return False
                                if x-t == thret.x and y+t == thret.y and a.type == "poun":
                                    if not self.is_pined(a.x,a.y,x-t,y+t):
                                        return False
                                if (x-t,y+t) in self.pouns_moves:
                                    if not self.is_pined(self.pouns_moves[(x-t,y+t)][0],self.pouns_moves[(x-t,y+t)][1],x-t,y+t):
                                        return False
            elif thret.type == "Queen":
                if thret.x == x:
                    if thret.y > y:
                        for t in range(1,abs(thret.y - y)+1):
                            for a in self.board[x][y+t].thret_list:
                                if a.color == color and a.type != "King" and a.type != "poun":
                                    if not self.is_pined(a.x,a.y,x,y+t):
                                        return False
                                if x == thret.x and y+t == thret.y and a.type == "poun":
                                    if not self.is_pined(a.x,a.y,x,y+t):
                                        return False
                                if (x,y+t) in self.pouns_moves:
                                    if not self.is_pined(self.pouns_moves[(x,y+t)][0],self.pouns_moves[(x,y+t)][1],x,y+t):
                                        return False
                    elif thret.y < y:
                        for t in range(1,abs(thret.y - y)+1):
                            for a in self.board[x][y-t].thret_list:
                                if a.color == color and a.type != "King" and a.type != "poun":
                                    if not self.is_pined(a.x,a.y,x,y-t):
                                        return False
                                if x == thret.x and y-t == thret.y and a.type == "poun":
                                    if not self.is_pined(a.x,a.y,x,y-t):
                                        return False
                                if (x,y-t) in self.pouns_moves:
                                    if not self.is_pined(self.pouns_moves[(x,y-t)][0],self.pouns_moves[(x,y-t)][1],x,y-t):
                                        return False
                elif thret.y == y:
                    if thret.x > x:
                        for t in range(1,abs(thret.x - x)+1):
                            for a in self.board[x+t][y].thret_list:
                                if a.color == color and a.type != "King" and a.type != "poun":
                                    if not self.is_pined(a.x,a.y,x+t,y):
                                        return False
                                if x+t == thret.x and y == thret.y and a.type == "poun":
                                    if not self.is_pined(a.x,a.y,x+t,y):
                                        return False
                                if (x+t,y) in self.pouns_moves:
                                    if not self.is_pined(self.pouns_moves[(x+t,y)][0],self.pouns_moves[(x+t,y)][1],x+t,y):
                                        return False
                    elif thret.x < x:
                        for t in range(1,abs(thret.x - x)+1):
                            for a in self.board[x-t][y].thret_list:
                                if a.color == color and a.type != "King" and a.type != "poun":
                                    if not self.is_pined(a.x,a.y,x-t,y):
                                        return False
                                if x-t == thret.x and y == thret.y and a.type == "poun":
                                    if not self.is_pined(a.x,a.y,x-t,y):
                                        return False
                                if (x-t,y) in self.pouns_moves:
                                    if not self.is_pined(self.pouns_moves[(x-t,y)][0],self.pouns_moves[(x-t,y)][1],x-t,y):
                                        return False
                elif thret.x > x and thret.y > y:
                    for t in range(1,abs(thret.y - y)+1):
                            for a in self.board[x+t][y+t].thret_list:
                                if a.color == color and a.type != "King" and a.type != "poun"  :
                                    if not self.is_pined(a.x,a.y,x+t,y+t):
                                        return False
                                if x+t == thret.x and y+t == thret.y and a.type == "poun":
                                    if not self.is_pined(a.x,a.y,x+t,y+t):
                                        return False
                                if (x+t,y+t) in self.pouns_moves:
                                    print("poun x: ",self.pouns_moves[(x+t,y+t)][0],"poun y: ",self.pouns_moves[(x+t,y+t)][1])
                                    if not self.is_pined(self.pouns_moves[(x+t,y+t)][0],self.pouns_moves[(x+t,y+t)][1],x+t,y+t):
                                        return False
                elif thret.x < x and thret.y < y:
                    for t in range(1,abs(thret.y - y)+1):
                            for a in self.board[x-t][y-t].thret_list:
                                if a.color == color and a.type != "King" and a.type != "poun":
                                    if not self.is_pined(a.x,a.y,x-t,y-t):
                                        return False   
                                if x-t == thret.x and y-t == thret.y and a.type == "poun":
                                    if not self.is_pined(a.x,a.y,x-t,y-t):
                                        return False
                                if (x-t,y-t) in self.pouns_moves:
                                    if not self.is_pined(self.pouns_moves[(x-t,y-t)][0],self.pouns_moves[(x-t,y-t)][1],x-t,y-t):
                                        return False
                elif thret.x > x and thret.y < y:
                    for t in range(1,abs(thret.y - y)+1):
                            for a in self.board[x+t][y-t].thret_list:
                                if a.color == color and a.type != "King" and a.type != "poun":
                                    if not self.is_pined(a.x,a.y,x+t,y-t):
                                        return False
                                if x+t == thret.x and y-t == thret.y and a.type == "poun":
                                    if not self.is_pined(a.x,a.y,x+t,y-t):
                                        return False
                                if (x+t,y-t) in self.pouns_moves:
                                    if not self.is_pined(self.pouns_moves[(x+t,y-t)][0],self.pouns_moves[(x+t,y-t)][1],x+t,y-t):
                                        return False
                elif thret.x < x and thret.y > y:
                    for t in range(1,abs(thret.y - y)+1):
                            for a in self.board[x-t][y+t].thret_list:
                                if a.color == color and a.type != "King" and a.type != "poun":
                                    if not self.is_pined(a.x,a.y,x-t,y+t):
                                        return False
                                if x-t == thret.x and y+t == thret.y and a.type == "poun":
                                    if not self.is_pined(a.x,a.y,x-t,y+t):
                                        return False
                                if (x-t,y+t) in self.pouns_moves:
                                    if not self.is_pined(self.pouns_moves[(x-t,y+t)][0],self.pouns_moves[(x-t,y+t)][1],x-t,y+t):
                                        return False    
            elif thret.type == "knight":
                for a in self.board[thret.x][thret.y].thret_list:
                    if a.color == color and a.type != "King":
                        if not self.is_pined(a.x,a.y,thret.x,thret.x):
                            return False
            elif thret.type == "poun":
                for a in self.board[thret.x][thret.y].thret_list:
                    if a.color == color and a.type != "King":
                        if not self.is_pined(a.x,a.y,thret.x,thret.x):
                            return False
            if i > 1:
                return True
            if thret.color != self.board[x][y].color:
                i +=1
        return True

    def append_move(self):
        b  = [[0 for x in range(8)] for y in range(8)] 
        for x in range(8):
            for y in range(8):
                b[x][y] = Piece(self.board[x][y].get_type(),self.board[x][y].get_color(),x,y)
        self.move_list.append(b)

    def pouns(self):
        self.pouns_moves.clear()
        for x in range(8):
            for y in range(8):
                if self.board[x][y].type == "poun" :
                    if self.board[x][y].color == "white"  :
                        if self.board[x][y+1].type == "#":
                            self.pouns_moves.update({(x,y+1):(x,y)})
                            if y == 1 :
                                if self.board[x][y+2].type == "#":
                                    self.pouns_moves.update({(x,y+2):(x,y)})
                    elif self.board[x][y].color == "black" and self.is_pined(x,y,x-1,y-1) :
                        if self.board[x][y-1].type == "#":
                            self.pouns_moves.update({(x,y-1):(x,y)})
                            if y == 7 :
                                if self.board[x][y-2].type == "#":
                                    self.pouns_moves.update({(x,y-2):(x,y)})

    def is_king_can_move(self,x,y):
        self.threts()
        if self.king_move(x,y,x+1,y+1)[0]:
            return True
        elif self.king_move(x,y,x-1,y-1)[0]:
            return True
        elif self.king_move(x,y,x-1,y+1)[0]:
            return True
        elif self.king_move(x,y,x+1,y-1)[0]:
            return True
        elif self.king_move(x,y,x,y+1)[0]:
            return True
        elif self.king_move(x,y,x,y-1)[0]:
            return True
        elif self.king_move(x,y,x-1,y)[0]:
            return False
        elif self.king_move(x,y,x+1,y)[0]:
            return True
        return False

    def is_pat(self,color):
        return False

    def find_best_move(self,board,dapth,color):
        best_move = list()
        best_move.append([1,1])
        best_move.append([2,2])
        board_ =  Board()
        board_ = copy(board)
        best_value = -1000
        if color:
            best_value = -1000
            str_color = 'white'
        else :
            str_color = 'black'
            best_value = 1000
        val = -9999
        for x in range(8):
            for y in range(8):
                #print(board_.board[x][y].color,x,y)
                if board_.board[x][y].color == str_color:
                    moves = board_.leagal_moves(x,y)
                    for move in moves:
                        board_ = copy(board)
                        board_.is_leagal_move(x,y,move[0],move[1],True)
                        val = self.min_max(board_,dapth,-10000,10000,  not color)
                        #print('value:',val,'From (x,y)',x,y,'To (x,y)', move,' ', best_move[1])

                        if val >= best_value and color:
                            best_value = val 
                            best_move[0][0] = x
                            best_move[0][1] = y
                            best_move[1][0] = move[0]
                            best_move[1][1] = move[1]
                            if val > 400:
                                return best_move
                        elif val <= best_value and not color:
                            best_value = val 
                            best_move[0][0] = x
                            best_move[0][1] = y
                            best_move[1][0] = move[0]
                            best_move[1][1] = move[1]
                            if val < -400:
                                return best_move

        return best_move

    def min_max(self,board,dapth,alpha,beta,color):
        best_move = 10000
        board_ =  Board()
        board_ = copy(board)
        check =  board.is_check()
        if check[0]:
            if board.is_check_mate(check[1]):
                return board_.evaluate_pos()
        if dapth == 0:
            return board_.evaluate_pos()
        if color:
            best_move = -10000
            for x in range(8):
                for y in range(8):
                    if board_.board[x][y].color == 'white':
                        moves = board_.leagal_moves(x,y)
                        for move in moves:
                            board_ = copy(board)
                            board_.is_leagal_move(x,y,move[0],move[1],True)
                            best_move = max(best_move,board_.min_max(board_,dapth-1,alpha,beta,not color))
                            alpha = max(best_move,alpha)
                            if beta <= alpha:
                                return best_move
            return best_move
        else :
            for x in range(8):
                for y in range(8):
                    if board_.board[x][y].color == 'black':
                        moves = board.leagal_moves(x,y)
                        for move in moves:
                            board_ = copy(board)
                            board_.is_leagal_move(x,y,move[0],move[1],True)
                            best_move = min(best_move,board_.min_max(board_,dapth-1,alpha,beta,not color))
                            beta = min(best_move,beta)
                            if beta <= alpha:
                                return best_move
            return best_move

    def evaluate_pos(self):
        sum = 0.0
        for x in range(8):
            for y in  range(8):
                res = 0.0
                if self.board[x][y].get_type == "rook":
                    res = 5 + 0.0005 * self.count_threts(x,y)
                elif self.board[x][y].type == "knight":
                    res = 3 + 0.0005 * self.count_threts(x,y)
                elif self.board[x][y].type == "poun":
                    res = 1 + 0.0005 * self.count_threts(x,y)
                elif self.board[x][y].type == "bishop":
                    res = 3.005 + 0.0005 * self.count_threts(x,y)
                elif self.board[x][y].type == "king":
                    res = 5 + 0.0005 * self.count_threts(x,y)
                elif self.board[x][y].type == "queen":
                    res = 10 + 0.0005 * self.count_threts(x,y)
                if self.board[x][y].color == "black":
                    res *= -1
                sum += res
        check =  self.is_check()
        if check[0]:
            if self.is_check_mate(check[1]):
                if check[1] == 'white':
                    sum -= 1000
                elif check[1] == 'black':
                    sum += 1000
        return sum

    def king_pos(self,color):
        for x in range(8):
            for y in range(8):
                if self.board[x][y].type == "King" and self.board[x][y].color == color:
                    return (x,y)

