import tkinter as tk
import random

CELL_SIZE = 25
GRID_WIDTH = 20
GRID_HEIGHT = 20
GAME_AREA_COLOR = "#000000"

#tetris shapes
Blocks = [[[2,2,2,2]], #I
          [[0,0,3],[0,0,3],[0,3,3]], #J
          [[4,4],[4,4]], #O
          [[5,0,0],[5,0,0],[5,5,0]], #L
          [[6,6,6],[0,6,0]], #T
          [[7,7,0],[0,7,7]], #Z
          [[0,8,8],[8,8,0]]  #S  
                             ]

#color of the blocks
COLORS = {
          2:'#e21988',
          3:'#BD97CB',
          4:'#B4F8C8',
          5:'#549efc',
          6:'#F8D210',
          7:'#189ab4',
          8:'#81B622'
          }

class TetrisGame(tk.Tk):

    def __init__(self):
        #executing the __init__ method of superclass as if it were a method defined in childclass.
        super().__init__()
        self.title('Tetris Game')

        #creating the main page
        self.canvas = tk.Canvas(self,width = GRID_WIDTH*CELL_SIZE ,
                                 height = GRID_HEIGHT*CELL_SIZE , bg = GAME_AREA_COLOR)
        self.canvas.pack()
        
        self.board_game = [[0]*GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.center_window(width = GRID_WIDTH*CELL_SIZE ,height = GRID_HEIGHT*CELL_SIZE )

        #game state
        self.game_over = False
        self.level = 1
        self.score = 0
        self.delay = 1000 #ms

        # Current piece variables
        self.current_piece = None
        self.current_color = None

        #game start
        self.new_piece() # initialize the first shape
        self.fall()
        self.bind("<Key>",self.key_presses)
        self.draw_board() # Draw the initial board and shape


    def center_window(self, width, height):
        """Center the window on the screen"""

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calculate position x and y coordinates from nw
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        self.geometry(f'{width}x{height}+{x}+{y}')


    def new_piece(self):
        block_idx = random.randint(0,len(Blocks)-1)
        self.current_piece = Blocks[block_idx]
        self.current_color = COLORS[block_idx+2] 

        self.shape_x = int(GRID_WIDTH//2) - len(self.current_piece[0])//2 #where the shape starts to come down.
        self.shape_y = 0

        # Game over if the new shape immediately collides
        if not self.check_if_collision(self.shape_x,self.shape_y,self.current_piece):
            self.game_over = True

        
    def fall(self):
        if self.game_over :
            self.draw_board()
            return
        
        if self.canmove(0, 1):
            self.shape_y += 1

        else : 
            self.add_to_board()
            self.remove_line()
            self.new_piece()
            
        # after = allows you to program the execution of your own function after a certain amount of time.
        self.after(self.delay,self.fall) #the falls will be due after the delay time.    
        self.draw_board()


    def canmove(self,dx,dy):
        #Check if the shape can move dx units without collision.(dx = +-1)
        new_x = self.shape_x + dx
        new_y = self.shape_y + dy
        return self.check_if_collision(new_x, new_y, self.current_piece) #return t or f


    def check_if_collision(self,shape_x,shape_y,Blocks):

        #Check if the shape can be placed at position (x, y) without colliding and finding in what position it is.
        #enumerate = index and value gets saved and we can tell with what number the index would be.

        for i,row in enumerate(Blocks): #i = num of lines of A block
            for j, cell in enumerate(row): #each column of the block

                #(x,y) the nw of a block
                #check if the shape can come lower.
                if cell !=0 :
                    board_x = shape_x+j
                    board_y = shape_y+i

                    #blocks staying on the screen and checking if the fallen piece can be moved to another place.
                    if board_x<0 or board_x>=GRID_WIDTH or board_y>=GRID_HEIGHT or self.board_game[board_y][board_x] != 0 :
                        return False
        return True
    

    def rotate(self):

        # zip() = an iterator of tuples where the 1and2 item get pair together.
        rotate_block = list(zip(*reversed(self.current_piece)))  # rotate clockwise
        # a = [[6,6,6],[0,6,0]]
        # *reversed = [[0, 6, 0] [6, 6, 6]]
        # zip = [(0, 6), (6, 6), (0, 6)]

        #check if the rotated shape will collide with anything.
        if self.check_if_collision(self.shape_x,self.shape_y,rotate_block):
            self.current_piece = rotate_block
       
        else:
            for dx in [-1,1]:  #we are moving to left or right as much as dx.
                if self.check_if_collision(self.shape_x+dx,self.shape_y,rotate_block):
                    self.current_piece = rotate_block
                    self.shape_x += dx
                    break  
        
        self.draw_board()


    def add_to_board(self):
        """Merge current piece into the board"""
        for i,row in enumerate(self.current_piece):
            for j,cell in enumerate(row):
                if cell != 0 :
                    self.board_game[self.shape_y+i][self.shape_x+j] = cell #fill
    

    def remove_line(self):
        lines_cleared = 0
        i = 0 #y

        #check lines
        for i in range (GRID_HEIGHT):
            #if the line is full
            if all( self.board_game[i] ):
                lines_cleared += 1
                del self.board_game[i]
                self.board_game.insert(0,[0]*GRID_WIDTH)
            else:
                i += 1

            if lines_cleared>0:
                self.update_scores(lines_cleared)


    def draw_a_cell(self,x,y,color):       
        self.canvas.create_rectangle(x*CELL_SIZE,y*CELL_SIZE,
                                     (x+1)*CELL_SIZE,(y+1)*CELL_SIZE,
                                     fill = color ,outline = 'black', width = 5)     


    def drawshape (self,shape,shape_x,shape_y,color):
        for i , row in enumerate(shape):
            for j , cell in enumerate(row):
                if cell :
                    x = (shape_x + j )*CELL_SIZE
                    y = (shape_y + i )*CELL_SIZE

                    self.canvas.create_rectangle(
                        x,y,x + CELL_SIZE,y + CELL_SIZE,fill = color , outline ='black')
                    #if shape_x,y = 2,3 for cell(1,1) and shape = [[1, 1], [0, 1]] we have rec (90, 120, 120, 150)
                    #all the recs together = block


    def draw_board(self):
        #redraw the game screen
        self.canvas.delete('all')

        # draw the board
        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                if self.board_game[i][j] != 0:
                    self.draw_a_cell(j,i,COLORS[self.board_game[i][j]])
                    
        self.drawshape(self.current_piece,self.shape_x,self.shape_y,self.current_color)  

        if self.game_over :
            self.canvas.create_text(250,250,anchor = 'center' , text = 'Game over',
                                      fill = '#18A558' , font = ('STENCIL',35))
            # self.canvas.create_text(250,250,anchor = 'center' , text = 'Game over',
            #                          fill = 'red' , font = ('Robus',35))
            
            #or do a def game_over.
        self.canvas.create_text(10, 5, anchor='nw', text=f'Level : {self.level}', fill='#18A558', font=('Gill Sans Ultra Bold Condensed', 15))        
        self.canvas.create_text(10, 30, anchor='nw', text=f'Score : {self.score}', fill='#18A558', font=('Gill Sans Ultra Bold Condensed', 15))


    def update_scores(self , lines_cleared):
        if lines_cleared > 0:
            self.score += 250 * self.level

        self.level = self.score//1000 + 1

        self.delay = max(100, 1000 - (self.level - 1) * 60) 


    def key_presses(self,event):
        if self.game_over :
            return
        
        #"symbols".(.keysym) is the corresponder(moteghabel) attribute of the Event object.
        if event.keysym == "Up":
            self.rotate()
        
        elif event.keysym == "Left":
            if self.canmove(-1,0):
                self.shape_x -= 1

        elif event.keysym == "Right":
            if self.canmove(1,0):
                self.shape_x += 1

        elif event.keysym == "Down":
            if self.canmove(0,1):
                self.shape_y += 1    
        
        elif event.keysym == "space": #hard drop
            while self.canmove(0,1):
                self.shape_y += 1

        self.draw_board() #if we make a change it will be redrawed and displayed.

    
#start of the program
if __name__ == "__main__" :
    app = TetrisGame()
    app.mainloop()   
