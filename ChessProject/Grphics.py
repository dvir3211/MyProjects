from board import Board
import time
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import tkinter.simpledialog
class Cordinates():
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

class Chess_Game():
    def __init__(self):
        self.chose_piece = (False,Cordinates(-1,-1),"none")
        self.root = Tk()
        self.w = Canvas(self.root, width=500, height=500)
        self.root.title("chess board")
        self.image_dict = dict()
        self.last_tap = Cordinates(-1,-1)
        self.board = Board()
        self.image_delete_dict = dict()
        self.w.bind('<Button-1>', self.getxy)

        self.set_imeges()
        self.new_piece = False
        
    def set_imeges(self):
        black_rook = Image.open("piece_images\Black_rook.png")
        black_rook = black_rook.resize((40,40)) #resize image
        black_rook =  ImageTk.PhotoImage(black_rook)
        self.image_dict.update({"black_rook": black_rook})
        
        black_poun = Image.open("piece_images\Black_poun.png")
        black_poun = black_poun.resize((40,40)) #resize image
        black_poun =  ImageTk.PhotoImage(black_poun)
        self.image_dict.update({"black_poun": black_poun})

        black_knight = Image.open("piece_images\Black_knight.png")
        black_knight = black_knight.resize((40,40)) #resize image
        black_knight =  ImageTk.PhotoImage(black_knight)
        self.image_dict.update({"black_knight": black_knight})

        black_bishop = Image.open("piece_images\Black_bishop.png")
        black_bishop = black_bishop.resize((40,40)) #resize image
        black_bishop =  ImageTk.PhotoImage(black_bishop)
        self.image_dict.update({"black_bishop": black_bishop})

        black_queen = Image.open("piece_images\Black_queen.png")
        black_queen = black_queen.resize((40,40)) #resize image
        black_queen =  ImageTk.PhotoImage(black_queen)
        self.image_dict.update({"black_Queen": black_queen})

        black_king = Image.open("piece_images\Black_king.png")
        black_king = black_king.resize((40,40)) #resize image
        black_king =  ImageTk.PhotoImage(black_king)
        self.image_dict.update( {"black_King": black_king})


        white_rook = Image.open("piece_images\white_rook.png")
        white_rook = white_rook.resize((40,40)) #resize image
        white_rook =  ImageTk.PhotoImage(white_rook)
        self.image_dict.update({"white_rook": white_rook})
        
        white_knight = Image.open("piece_images\white_knight.png")
        white_knight = white_knight.resize((40,40)) #resize image
        white_knight =  ImageTk.PhotoImage(white_knight)
        self.image_dict.update({"white_knight": white_knight})

        white_bishop = Image.open("piece_images\white_bishop.png")
        white_bishop = white_bishop.resize((40,40)) #resize image
        white_bishop =  ImageTk.PhotoImage(white_bishop)
        self.image_dict.update({"white_bishop": white_bishop})

        white_queen = Image.open("piece_images\white_queen.png")
        white_queen = white_queen.resize((40,40)) #resize image
        white_queen =  ImageTk.PhotoImage(white_queen)
        self.image_dict.update({"white_Queen": white_queen})

        white_king = Image.open("piece_images\white_king.png")
        white_king = white_king.resize((40,40)) #resize image
        white_king =  ImageTk.PhotoImage(white_king)
        self.image_dict.update( {"white_King": white_king})

        white_poun = Image.open("piece_images\white_poun.png")
        white_poun = white_poun.resize((40,40)) #resize image
        white_poun =  ImageTk.PhotoImage(white_poun)
        self.image_dict.update({"white_poun": white_poun})

        white_pieces = Image.open("piece_images\white_pieces.png")
        white_pieces = white_pieces.resize((240,70)) #resize image
        white_pieces =  ImageTk.PhotoImage(white_pieces)
        self.image_dict.update({"white_pieces": white_pieces})

        black_pieces = Image.open("piece_images\Black_pieces.png")
        black_pieces = black_pieces.resize((240,70)) #resize image
        black_pieces =  ImageTk.PhotoImage(black_pieces)
        self.image_dict.update({"black_pieces": black_pieces})

        black_win = Image.open("piece_images\Black_win.png")
        black_win = black_win.resize((500,150)) #resize image
        black_win =  ImageTk.PhotoImage(black_win)
        self.image_dict.update({"black_win": black_win})

        white_win = Image.open("piece_images\white_win.png")
        white_win = white_win.resize((500,150)) #resize image
        white_win =  ImageTk.PhotoImage(white_win)
        self.image_dict.update({"white_win": white_win})


    def start_game(self):
        print("im here")
        original = Image.open("chess.png")
        original = original.resize((500,500)) #resize image
        img = ImageTk.PhotoImage(original)
        self.w.create_image(0, 0, image=img, anchor="nw")
        self.w.pack()
        

        for y in range(8):
            for x in range(8):
                if self.board.get_squere(x,y).get_color() == "black":
                    self.w.create_image(27 + x*60,430- y*60 ,image=self.image_dict["black_{}".format(self.board.get_squere(x,y).get_type())], anchor="nw")
                elif self.board.get_squere(x,y).get_color() == "white":
                    self.w.create_image(27 + x*60,430 -y*60 ,image=self.image_dict["white_{}".format(self.board.get_squere(x,y).get_type())], anchor="nw")
        """if self.board.turn:
            move = self.board.find_best_move(self.board,5,True)
            self.board.move_piece(move[0][0],move[0][1],move[1][0],move[1][1],True)
            for y in range(8):
                for x in range(8):
                    if self.board.get_squere(x,y).get_color() == "black":
                        self.w.create_image(27 + x*60,430- y*60 ,image=self.image_dict["black_{}".format(self.board.get_squere(x,y).get_type())], anchor="nw")
                    elif self.board.get_squere(x,y).get_color() == "white":
                        self.w.create_image(27 + x*60,430 -y*60 ,image=self.image_dict["white_{}".format(self.board.get_squere(x,y).get_type())], anchor="nw")
            while True:
                self.root.update()"""
        if self.board.is_check()[0]:
                if self.board.is_check_mate(self.board.is_check()[1]):
                    print("checkmate")
                    if self.board.is_check()[1] == "white":
                        self.w.create_image(0,175 ,image=self.image_dict["black_win"], anchor="nw")
                        while True:
                            self.root.update()
                    elif self.board.is_check()[1] == "black":
                        self.w.create_image(0,175 ,image=self.image_dict["white_win"], anchor="nw")
                        while True:
                            self.root.update()
        
        while 1:
            self.root.update()
       
    def getxy(self,event):    
        print("Position = ({0},{1})".format(event.x, event.y))
        x = 0
        y = 0
        if self.new_piece:
            print("hay")
        if event.x in range(0,40) and event.y in range(480,497):
            self.board.undo()
            self.start_game()
        elif event.x in range(17,77):
            x = 0
            #self.w.delete(2)
            #self.w.create_image(250,250,image=self.image_dict["black_rook"], anchor="nw")
            #self.root.update()
        elif event.x in range(77,137):
            x = 1
        elif event.x in range(137,197):
            x = 2
        elif event.x in range(197,257):
            x = 3
        elif event.x in range(257,317):
            x = 4 
        elif event.x in range(317,377):
            x = 5
        elif event.x in range(377,437):
            x = 6
        elif event.x in range(437,497):
            x = 7

        if event.y + 10 in range(17,77):
            y = 7
        elif event.y + 10 in range(77,137):
            y = 6
        elif event.y + 10 in range(137,197):
            y = 5
        elif event.y + 10 in range(197,257):
            y = 4
        elif event.y + 10 in range(257,317):
            y = 3
        elif event.y + 10 in range(317,377):
            y = 2
        elif event.y + 10 in range(377,437):
            y = 1
        elif event.y + 10 in range(437,497):
            y = 0
        
        if self.chose_piece[0]:
            if event.x in range(136,196) and event.y in range(18,88):
                self.board.set_new_piece(self.chose_piece[1].get_x(),self.chose_piece[1].get_y(),"Queen",self.chose_piece[2])
                self.chose_piece = (False,Cordinates(-1,-1),"none")
                self.start_game()
            elif event.x in range(196,256):
                self.board.set_new_piece(self.chose_piece[1].get_x(),self.chose_piece[1].get_y(),"rook",self.chose_piece[2])
                self.chose_piece = (False,Cordinates(-1,-1),"none")
                self.start_game()
            elif event.x in range(256,316):
                self.board.set_new_piece(self.chose_piece[1].get_x(),self.chose_piece[1].get_y(),"bishop",self.chose_piece[2])
                self.chose_piece = (False,Cordinates(-1,-1),"none")
                self.start_game()
            elif event.x in range(316,374):
                self.board.set_new_piece(self.chose_piece[1].get_x(),self.chose_piece[1].get_y(),"knight",self.chose_piece[2])
                self.chose_piece = (False,Cordinates(-1,-1),"none")
                self.start_game()
        
        print ("x: ",x," y: ",y)
        #print("type:  ",self.board.get_squere(x,y).get_type(),"color:  ",self.board.get_squere(x,y).get_color())
        if self.board.move_piece(self.last_tap.x, self.last_tap.y, x, y,False) and not self.chose_piece[0] :
            self.board.move_piece(self.last_tap.x, self.last_tap.y, x, y,True)
            print(self.board.is_check()[0],"  ",self.board.is_check()[1])
            if self.board.board[x][y].type == "poun":
                if not self.board.turn and y == 7:
                    self.w.create_image(136,18 ,image=self.image_dict["white_pieces"], anchor="nw")
                    self.chose_piece = (True, Cordinates(x,y),"white")
                    while True:
                        self.root.update()
                elif  self.board.turn and y == 0:
                    self.w.create_image(136,18 ,image=self.image_dict["black_pieces"], anchor="nw")
                    self.chose_piece = (True, Cordinates(x,y),"black")
                    while True:
                        self.root.update()
            
            self.start_game()
            self.last_tap.x = -5
            self.last_tap.y = -5
            
        else:
            self.last_tap.x = x
            self.last_tap.y = y
        #print("!!!!  ",self.board.get_squere(x,y).get_color(),"  !!!!!")

    def root_main(self):
        self.root.update()

