"""
**************************************************************************
                               CONNECT FOUR
**************************************************************************
                                                By Krishnan

The below Python program is for the CONNECT FOUR Game using simple graphics.py
library and python 3.x core techniques. Since there is no use of extensive
graphical interfaces the game is simpler and code is bit extensive.

***************************************
            HOW TO PLAY
***************************************
This is a COMPUTER vs HUMAN Game.

1. When the turn comes click on the board where the coin needs to be put
2. If the cell clicked is a valid move then the repective coin is filled there.
3. Rules and winner are declared according to the rules of CONNECT FOUR.
"""
from graphics import *
import time
import random
import copy

# Global variables for use throughout the game
COMPUTER = 0
HUMAN = 1
TIE = 255
WIN = GraphWin("Connect Four", 1000, 800) # Window object created
HUMANTOKEN = Image(Point(930, 700), '4row_red.gif') # Human token
COMPTOKEN = Image(Point(75, 700), '4row_black.gif') # Computer Token
HUMWIN = Image(Point(500, 100), '4row_humanwinner.gif')
COMPWIN = Image(Point(500, 100), '4row_computerwinner.gif')
GAMETIE = Image(Point(500, 100), '4row_tie.gif')
MOVESDB = {} # Dictionary maintaining the moves database.
DIFFICULT = True

def draw_board():
    """
    This Method will draw the initial board for the game. By default
    it draws a 7 X 6 board as it is the default config of the game.
    """
    global MOVESDB
    movelist = []
    for i in range(2, 9):
        for j in range(2, 8):
            Image(Point(i*100,j*100), '4row_board.gif').draw(WIN)
            movelist.append((i*100, j*100))
    MOVESDB = dict.fromkeys(movelist) # Creates initial empty moves database
    HUMANTOKEN.draw(WIN) # Drawing Human token
    Text(Point(930, 760), "HUMAN").draw(WIN)
    COMPTOKEN.draw(WIN) # Drawing Computer token
    Text(Point(75, 760), "COMPUTER").draw(WIN)
    
def winchange():
    """
    A small method to change the background color everytime when Human plays.
    A small treat to eyes :)
    """
    WIN.setBackground(color_rgb(random.randint(0, 255),
                                random.randint(0, 255),
                                random.randint(0, 255)))
    
def show_text(text, vanish=True):
    """
    This is the common method which is use to show any text help on the board.
    The method will take in the text and print in on board for player's help.
    If vanish is made true the text disappears and vice versa.
    @param text: Text to be shown on board as help
    @param vanish: This Boolean variable decides whether text should vanish
                   or not
    """
    starttxt = Text(Point(500, 100), text)
    starttxt.undraw()
    starttxt.setFace('helvetica')
    starttxt.setSize(36)
    starttxt.draw(WIN)
    time.sleep(1)
    if vanish:
        starttxt.undraw()

def get_point(x, y):
    """
    This method is useful to convert the coordinates got from clicking the
    board to a multiple of 100. This is done for easy calculation and placement
    of tokens on board.
    Example: (256, 610) will be converted to (300, 600)
             (217, 603) will be converted to (200, 600)
    @param x: X coordinate which needs to be converted
    @param y: Y coordinate which needs to be converted
    """
    if x % 100 > 50:
        ptx = x + (100 -(x % 100))
    else:
        ptx = x - (x % 100)   # Rounding of the x point to nearest 100
    if y % 100 > 50:
        pty = y + (100 -(y % 100))
    else:
        pty = y - (y % 100)  # Rounding of the y point to nearest 100
    return ptx, pty

def validate_move(x, y, t):
    """
    This method is very important method which validates the move made.
    The method will check if the player has clicked outside the board or
    a cell where move cannot be made or a valid move.
    @param x: X coordinate of the move to be made
    @param y: Y coordinate of the move to be made
    @param t: Turn variable telling if it is Human or Computer
    """
    if MOVESDB[(x, y)] == None:
        if y == 700:
            MOVESDB[(x, y)] = t   # valid move is validated in database
            return True
        else:
            if MOVESDB[(x, y+100)] == None:
                show_text("CANNOT MAKE THAT MOVE")
            else:
                MOVESDB[(x, y)] = t # valid move is validated in database
                return True
    else:
        show_text("INVALID MOVE")
        
def get_move(x, y, t):
    """
    This method will get the move done by the Human or Computer, validates
    it and returns a Point object with the x and y coordinate to use it
    for making the move. This is the method which will round of coordinates
    and validates the move.
    @param x: X coordinate of the move to be made
    @param y: Y coordinate of the move to be made
    @param t: Turn variable telling if it is Human or Computer    
    """
    if x < 150 or y > 750 or x > 850 or y < 150:
        show_text("Clicked Outside the Board")  # Clicking outside is captured
    else:
        x, y = get_point(x, y)  # Rounding of coordinates
        ret = validate_move(x, y, t) # Validating the move made
        if ret:
            return Point(x, y)  # Returning Point object
    return False
          
def check_winner(t, movedict):
    """
    This method checks the board for a potential winner in all possibilities
    @param t: Turn variable telling whose turn it is
    @param movedict: The dictionary of moves where search needs to be done
    """
    for i in range(2, 6):   # Searching for a winner horizontally
        for j in range(2, 8):
            if movedict[(i*100, j*100)] == t and movedict[((i*100)+100, j*100)] == t and movedict[((i*100)+200, j*100)] == t and movedict[((i*100)+300, j*100)] == t:
                return True
                
    for i in range(2, 9):  # Searching for a winner Vertically
        for j in range(7, 4, -1):
            if movedict[(i*100, j*100)] == t and movedict[(i*100, (j*100)-100)] == t and movedict[(i*100, (j*100)-200)] == t and movedict[(i*100, (j*100)-300)] == t:
                return True
              
    for i in range(2, 6):  # Searching for a winner diagonally /
        for j in range(2, 5):
            if movedict[(i*100, j*100)] == t and movedict[((i*100)+100, (j*100)+100)] == t and movedict[((i*100)+200, (j*100)+200)] == t and movedict[((i*100)+300, (j*100)+300)] == t:
                return True
                
    for i in range(8, 4, -1):  # Searching for a winner diagonally \
        for j in range(2, 5):
            if movedict[(i*100, j*100)] == t and movedict[((i*100)-100, (j*100)+100)] == t and movedict[((i*100)-200, (j*100)+200)] == t and movedict[((i*100)-300, (j*100)+300)] == t:
                return True                
                
def is_board_full():
    """
    This method checks if the board is full
    """
    for each in MOVESDB.keys():
        if MOVESDB[each] == None:
            return False
    return True

def declare_winner(t):
    """
    This Method Declares a Winner
    @param t: Turn variable says who has won the contest.
    """
    if t == HUMAN:
        HUMWIN.draw(WIN)
    elif t == TIE:
        GAMETIE.draw(WIN)
    else:
        COMPWIN.draw(WIN)
    if WIN.getMouse():
        WIN.close()

def possible_moves():
    """
    This Method searches the Moves Database and gets the next possible moves
    for the computer to make. Then makes a random choice from the list and
    returns it.
    """
    pmvlist = []
    pdict = {}
    emplist = []
    for each in MOVESDB.keys():
        if MOVESDB[each] == None:
            emplist.append(each)
    for ele in sorted(emplist):
        if ele[0] in pdict:
            pdict[ele[0]].append(ele)
        else:
            pdict[ele[0]] = [ele]
    for key in pdict.keys():
        pmvlist.append(sorted(pdict[key])[-1])
        
    move = choose_best_mv(pmvlist) # Making a Random choice
    return move

def choose_best_mv(plist):
    """
    This method will be choosing the move to be made by computer.
    """
    move = []
    if DIFFICULT:
        for each in plist:
            copydict = copy.deepcopy(MOVESDB)
            copydict[each] == HUMAN
            if check_winner(HUMAN, copydict):
                move.append(each)
    if move:
        ch = random.choice(move)
    else:
        ch = random.choice(plist)
    return ch
"""       
def animate_move(t, m):
    if t == HUMAN:
        i = 700
        img = Image(Point(930, 700), '4row_red.gif')
        img.draw(WIN)
        while i > 100:
            img.move(930, i)
            i = i - 5
        img.move(m.x, i)
        img.move(m.x, m.y)
    else:
        i = 700
        img = Image(Point(75, 700), '4row_black.gif')
        img.draw(WIN)
        while i > 100:
            img.move(930, i)
            i = i - 5
        img.move(m.x, i)
        img.move(m.x, m.y)
"""    
def play():
    """
    The Main method that controls the game play after the Board is drawn.
    Initially the first turn is chosen by random and play carries forward till
    a result is achevied.
    """
    # Start playing
    show_text("Start Playing")
    if random.randint(0, 1) == 0: # Choosing the first one to play
        turn = COMPUTER
    else:
        turn = HUMAN
    while True:
        mv = False
        if turn == COMPUTER:
            ch = possible_moves()
            mv = get_move(ch[0], ch[1], turn)
            Image(mv, '4row_black.gif').draw(WIN)
            if check_winner(turn, MOVESDB):
                declare_winner(turn)
                break
            turn = HUMAN
        else:
            show_text("Click on the token to make a move")
            winchange()
            while not mv:
                show_text("HUMAN TO PLAY")
                var = WIN.getMouse()
                mv = get_move(var.x, var.y, turn)
            Image(mv, '4row_red.gif').draw(WIN)
            if check_winner(turn, MOVESDB):
                declare_winner(turn)
                break
            turn = COMPUTER
        if is_board_full():
            declare_winner(TIE)
            break
        
def main():
    """
    The Main method triggering the game.
    """
    # Draw the initial Board needed
    draw_board()
    # Initiating the game
    play()

if __name__ == '__main__':
    main()
