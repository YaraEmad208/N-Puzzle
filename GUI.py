import pygame
import sys
import random
from pygame.locals import *
from copy import deepcopy
from queue import PriorityQueue
from Heuristic import Heuristic
from Board import Board



class GUI:
    # Create the constants (go ahead and experiment with different values)
    # BoardData is a class for datastructure of the board which all data is stored in it and retreved from it \\Kamel

    BoardData = Board(3)   # 3 is default board

    def __init__(self):
        self.solution = list() # [up,right,left,down]
        self.tree = {}
        self.Fronte = PriorityQueue()
        self.key = 0
        self.counter = 0
        self.Goal = self.BoardData.getGoal()
        self.CloseList = list()
        self.allMoves = list()
        self.solved = False
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.misplaced_tiles=0
        self.taxicab=0


    WINDOWWIDTH = 790
    WINDOWHEIGHT = 600
    XMARGIN = int((WINDOWWIDTH - (BoardData.getTILESIZE() * BoardData.getBOARDERSIZE() + (BoardData.getBOARDERSIZE() - 1))) / 2)
    YMARGIN = int((WINDOWHEIGHT - (BoardData.getTILESIZE() * BoardData.getBOARDERSIZE() + (BoardData.getBOARDERSIZE() - 1))) / 1.2)
    FPS = 35
    BLANK = None

    #this is color
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    DARKTURQUOISE = (255, 165, 0)
    GREEN = (0, 0, 0)
    BGCOLOR = WHITE  # background color
    TILECOLOR = GREEN
    TEXTCOLOR = WHITE
    BORDERCOLOR = DARKTURQUOISE
    BASICFONTSIZE = 20
    BUTTONCOLOR = WHITE
    BUTTONTEXTCOLOR = BLACK
    MESSAGECOLOR = WHITE
    #-------------------

    #move
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'
    #-------------

    def main(self):
        global mised_SURF,mised_RECT,FPSCLOCK, DISPLAYSURF, BASICFONT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT, S3_SURF, S3_RECT, S4_SURF, S4_RECT, S5_SURF, S5_RECT, Hamming_SURF, Hamming_RECT, Euclidean_SURF, Euclidean_RECT, Manhattan_SURF, Manhattan_RECT, Permutation_SURF, Permutation_RECT, LinearConflict_SURF, LinearConflict_RECT, counterTextSURF, counterTextRECT, counterSURF, counterRECT,taxicab_SURF,taxicab_RECT, resizeable

        resizeable = True  # variable to check wither the puzzle size is chosen or not to disaple updating it while working
        msg = 'Choose "Puzzle size" then press "New Game"'
        pygame.init()

        FPSCLOCK = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode(
            (self.WINDOWWIDTH, self.WINDOWHEIGHT))
        pygame.display.set_caption('N-Puzzle')
        BASICFONT = pygame.font.Font('freesansbold.ttf', self.BASICFONTSIZE)

        # Store the option buttons and their rectangles in OPTIONS.
        NEW_SURF, NEW_RECT = self.makeText(
            'New Game',self.WHITE, (117, 84, 161), 650,5)
        SOLVE_SURF, SOLVE_RECT = self.makeText(
            'Solve', self.WHITE, (117, 84, 161),580,5)
        S3_SURF, S3_RECT = self.makeText(
            '8-Puzzle', self.BLACK, (210, 210, 210), 580,50,180,30)
        S4_SURF, S4_RECT = self.makeText(
            '16-Puzzle', self.BLACK, (210, 210, 210),580,90,180,30)
        S5_SURF, S5_RECT = self.makeText(
            '24-Puzzle', self.BLACK, (210, 210, 210),580,130,180,30)
        Hamming_SURF, Hamming_RECT = self.makeText(
            '1-misplaced tiles', self.BLACK, self.WHITE,5,200,180,45)
        Euclidean_SURF, Euclidean_RECT = self.makeText(
            '2-Euclidean',self.BLACK, self.WHITE, 195, 200,160,45)
        Manhattan_SURF, Manhattan_RECT = self.makeText(
            '3-Manhattan', self.BLACK, self.WHITE,368, 200,160,45)
        Permutation_SURF, Permutation_RECT = self.makeText(
            '4-Permutation', self.BLACK, self.WHITE, 538, 200,160,45)
        LinearConflict_SURF, LinearConflict_RECT = self.makeText(
            '5-LinearConflict', self.BLACK, self.WHITE, 5, 260, 180, 45)
        counterTextSURF, counterTextRECT = self.makeText(
            "Moves : ", self.MESSAGECOLOR, (210, 210, 210), 5, 30,150,40)
        mised_SURF, mised_RECT = self.makeText(
            "mised", self.MESSAGECOLOR, (210, 210, 210), 5, 70, 150, 40)
        taxicab_SURF, taxicab_RECT=self.makeText(
            "taxicab distances", self.MESSAGECOLOR, (210, 210, 210), 6, 120, 230, 40)
        #-----------------------------------------------------------

        mainBoard = deepcopy(self.Goal)
        self.drawBoard(mainBoard, msg)  # Draw starting board as goal board
        # a solved board is the same as the board in a start state.
        SOLVEDBOARD = deepcopy(mainBoard)

        while True:  # main game loop
            slideTo = None  # the direction, if any, a tile should slide
            if mainBoard == SOLVEDBOARD and not resizeable:
                msg = 'Solved!'

            self.checkForQuit()
            for event in pygame.event.get():  # event handling loop
                if event.type == MOUSEBUTTONUP:
                    spotx, spoty = self.getSpotClicked(
                        event.pos[0], event.pos[1])

                    if (spotx, spoty) == (None, None):
                        # check if the user clicked on an option button
                        # Determine which button was clicked \\Kamel
                        if S3_RECT.collidepoint(event.pos) and resizeable:
                            self.BoardData = Board(3)
                            self.BoardData.resetMovCounter()
                            mainBoard = self.BoardData.getGoal()
                            self.Goal = self.BoardData.getGoal()
                            self.drawBoard(mainBoard, msg)
                        elif S4_RECT.collidepoint(event.pos) and resizeable:
                            self.BoardData = Board(4)
                            self.BoardData.resetMovCounter()
                            mainBoard = self.BoardData.getGoal()
                            self.Goal = self.BoardData.getGoal()
                            self.drawBoard(mainBoard, msg)
                        elif S5_RECT.collidepoint(event.pos) and resizeable:
                            self.BoardData = Board(5)
                            self.BoardData.resetMovCounter()
                            mainBoard = self.BoardData.getGoal()
                            self.Goal = self.BoardData.getGoal()
                            self.drawBoard(mainBoard, msg)
                        # Choosing the heuristic \\Kamel
                        elif Hamming_RECT.collidepoint(event.pos):
                            self.BestFirstSearch(
                                mainBoard, Heuristic().Hamming)
                            self.drawBoard(
                                mainBoard, "Solution Path Found using the total number of misplaced tiles press solve")
                        elif Euclidean_RECT.collidepoint(event.pos):
                            self.BestFirstSearch(
                                mainBoard, Heuristic().Euclidean)
                            self.drawBoard(
                                mainBoard, "Solution Path Found using Euclidean press solve")
                        elif Manhattan_RECT.collidepoint(event.pos):
                            self.BestFirstSearch(
                                mainBoard, Heuristic().Manhattan)
                            self.drawBoard(
                                mainBoard, "Solution Path Found using Manhattan press solve")
                        elif Permutation_RECT.collidepoint(event.pos):
                            self.BestFirstSearch(
                                mainBoard, Heuristic().Permutation)
                            self.drawBoard(
                                mainBoard, "Solution Path Found using placed tiles press solve")
                        elif LinearConflict_RECT.collidepoint(event.pos):
                            self.BestFirstSearch(
                                mainBoard, Heuristic().LinearConflict)
                            self.drawBoard(
                                mainBoard, "Solution Path Found using placed tiles press solve")


                        elif NEW_RECT.collidepoint(event.pos):
                            self.BoardData.resetMovCounter()
                            ss = self.BoardData.getRestPath()
                            ss.reverse()
                            self.BoardData.clearSolution()
                            self.resetAnimation(mainBoard, ss)
                            mainBoard = self.generateNewPuzzle(
                                random.randint(5, 15))  # clicked on New Game button
                            self.drawBoard(
                                mainBoard, "Choose heuristic to solve the puzzle using it")
                        elif SOLVE_RECT.collidepoint(event.pos):
                            resizeable = False
                            self.solved = True
                            solutionpath = self.BoardData.getSolution()
                            self.applysolution(mainBoard, solutionpath)
                            self.drawBoard(mainBoard, "solved")
                            solutionpath = list()
                            self.Fronte = PriorityQueue()
                            self.key = 0
                            self.CloseList = list()
                            self.tree = {}
                            resizeable = True
                            self.solved = False
                            self.misplaced_tiles=0
                            self.taxicab = 0

                    else:
                        # check if the clicked tile was next to the blank spot
                        blankx, blanky = self.getBlankPosition(mainBoard)
                        if spotx == blankx + 1 and spoty == blanky:
                            slideTo = self.LEFT
                        elif spotx == blankx - 1 and spoty == blanky:
                            slideTo = self.RIGHT
                        elif spotx == blankx and spoty == blanky + 1:
                            slideTo = self.UP
                        elif spotx == blankx and spoty == blanky - 1:
                            slideTo = self.DOWN

                elif event.type == KEYUP:
                    # check if the user pressed a key to slide a tile
                    if event.key in (K_LEFT, K_a) and self.isValidMove(mainBoard, self.LEFT):
                        slideTo = self.LEFT
                    elif event.key in (K_RIGHT, K_d) and self.isValidMove(mainBoard, self.RIGHT):
                        slideTo = self.RIGHT
                    elif event.key in (K_UP, K_w) and self.isValidMove(mainBoard, self.UP):
                        slideTo = self.UP
                    elif event.key in (K_DOWN, K_s) and self.isValidMove(mainBoard, self.DOWN):
                        slideTo = self.DOWN

            if slideTo:
                # show slide on screen
                self.slideAnimation(mainBoard, slideTo, msg, 10)
                self.makeMove(mainBoard, slideTo)
            pygame.display.update()
            FPSCLOCK.tick(self.FPS)

    def clearall(self):
        self.BoardData.clearSolution()
        self.solution.clear()
        self.Fronte = list()
        self.key = 0
        self.CloseList = list()
        self.tree = {}

    # def makeText(self, text, color, bgcolor, top, left, width=None, height=None, margin=0):
    #     import pygame
    #     pygame.init()

        # Assuming BASICFONT is defined somewhere in your code.
    def makeText(self, text, color, bgcolor, top, left, width=None, height=None, margin=0, border_size=2,border_color=(60, 60, 60)):
        # Create the Surface and Rect objects for some text.
        textSurf = BASICFONT.render(text, True, color, bgcolor)
        original_width, original_height = textSurf.get_width(), textSurf.get_height()
        # Set the width and height if specified, or use the size of the rendered text.
        width = width or original_width
        height = height or original_height
        # Add margin and border to the dimensions
        width_with_margin_border = width + 2 * (margin + border_size)
        height_with_margin_border = height + 2 * (margin + border_size)
        # Create a new surface with the desired background color and dimensions.
        newSurface = pygame.Surface((width_with_margin_border, height_with_margin_border), pygame.SRCALPHA)
        # Draw the background and border on the new surface.
        pygame.draw.rect(newSurface, bgcolor, (border_size, border_size, width + 2 * margin, height + 2 * margin))
        pygame.draw.rect(newSurface, border_color, (0, 0, width_with_margin_border, height_with_margin_border),
                         border_size)
        # Calculate the center position for the text.
        center_x = (width_with_margin_border - original_width) // 2
        center_y = (height_with_margin_border - original_height) // 2
        # Blit the original text surface onto the new surface at the center position.
        newSurface.blit(textSurf, (center_x + margin + border_size, center_y + margin + border_size))
        # Create the Rect object for the new surface.
        textRect = newSurface.get_rect()
        textRect.topleft = (top, left)
        return (newSurface, textRect)

    def terminate(self):
        pygame.quit()
        sys.exit()

    def checkForQuit(self):
        for event in pygame.event.get(QUIT):  # get all the QUIT events
            self.terminate()  # terminate if any QUIT events are present
        for event in pygame.event.get(KEYUP):  # get all the KEYUP events
            if event.key == K_ESCAPE:
                self.terminate()  # terminate if the KEYUP event was for the Esc key
            pygame.event.post(event)  # put the other KEYUP event objects back

    # Return the x and y of board coordinates of the blank space.
    def getBlankPosition(self, board):
        n = self.BoardData.getBOARDERSIZE()
        for x in range(n):
            for y in range(n):
                if board[x][y] == self.BLANK:
                    return (x, y)

    def makeMove(self, board, move):
        global counterSURF, counterRECT
        blankx, blanky = self.getBlankPosition(board)
        if move == self.UP:
            if self.solved:
                self.counter += 1
            board[blankx][blanky], board[blankx][blanky +1] = board[blankx][blanky + 1], board[blankx][blanky]
        elif move == self.DOWN:
            if self.solved:
                self.counter += 1
            board[blankx][blanky], board[blankx][blanky -1] = board[blankx][blanky - 1], board[blankx][blanky]
        elif move == self.LEFT:
            if self.solved:
                self.counter += 1
            board[blankx][blanky], board[blankx +1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
        elif move == self.RIGHT:
            if self.solved:
                self.counter += 1
            board[blankx][blanky], board[blankx -1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]
        return board



    def getRandomMove(self, board, lastMove=None):
        # start with a full list of all four moves
        validMoves = [self.UP, self.DOWN, self.LEFT, self.RIGHT]

        # remove moves from the list as they are disqualified
        if lastMove == self.UP or not self.isValidMove(board, self.DOWN):
            validMoves.remove(self.DOWN)
        if lastMove == self.DOWN or not self.isValidMove(board, self.UP):
            validMoves.remove(self.UP)
        if lastMove == self.LEFT or not self.isValidMove(board, self.RIGHT):
            validMoves.remove(self.RIGHT)
        if lastMove == self.RIGHT or not self.isValidMove(board, self.LEFT):
            validMoves.remove(self.LEFT)
        # return a random move from the list of remaining moves
        return random.choice(validMoves)

    def getLeftTopOfTile(self, tileX, tileY):
        """ this function give me left , top position the tile build in (x,y) """
        left = self.XMARGIN + (tileX * self.BoardData.getTILESIZE()) + (tileX - 1)
        top = self.YMARGIN +(tileY * self.BoardData.getTILESIZE()) + (tileY - 1)
        return (left, top)

    def getSpotClicked(self, x, y):
        # from the x & y pixel coordinates, get the x & y board coordinates
        for tileX in range(self.BoardData.getBOARDERSIZE()):
            for tileY in range(self.BoardData.getBOARDERSIZE()):
                left, top = self.getLeftTopOfTile(tileX, tileY)
                tileRect = pygame.Rect(
                    left, top, self.BoardData.getTILESIZE(), self.BoardData.getTILESIZE())
                if tileRect.collidepoint(x, y):
                    return (tileX, tileY)
        return (None, None)

    def drawTile(self, tilex, tiley, number, adjx=0, adjy=0):
        # draw a tile at board coordinates tilex and tiley, optionally a few
        # pixels over (determined by adjx and adjy)
        left, top = self.getLeftTopOfTile(tilex, tiley)
        #rectangle_rect = pygame.Rect(50, 50, 100, 80)  50 is x , 50 is y , 100 and 80 width and height
        #pygame.draw.rect(window, RED, rectangle_rect)
        pygame.draw.rect(DISPLAYSURF, (117, 84, 161),
                         (left + adjx, top + adjy, self.BoardData.getTILESIZE(), self.BoardData.getTILESIZE()))
        textSurf = BASICFONT.render(str(number), True, self.TEXTCOLOR)
        textRect = textSurf.get_rect()
        textRect.center = left + int(self.BoardData.getTILESIZE() / 2) + adjx, top + int(
            self.BoardData.getTILESIZE() / 2) + adjy
        DISPLAYSURF.blit(textSurf, textRect)




    def drawBoard(self, board, message):
        DISPLAYSURF.fill(self.BGCOLOR)  # set background color
        if message:
            textSurf, textRect = self.makeText(
                message, self.MESSAGECOLOR, (60, 60, 60), 5, 5)
            DISPLAYSURF.blit(textSurf, textRect)
        for tilex in range(self.BoardData.getBOARDERSIZE()):
            for tiley in range(self.BoardData.getBOARDERSIZE()):
                if board[tilex][tiley]:
                    self.drawTile(tilex, tiley, board[tilex][tiley])

        # Draw the board border (Blue line around the tiles) \\Kamel
        left, top = self.getLeftTopOfTile(0, 0)
        width = 250
        height = 250
        pygame.draw.rect(DISPLAYSURF, (240, 240, 240),
                         (left - 5, top - 5, width + 11, height + 11), 4)


        DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
        DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)
        DISPLAYSURF.blit(S3_SURF, S3_RECT)
        DISPLAYSURF.blit(S4_SURF, S4_RECT)
        DISPLAYSURF.blit(S5_SURF, S5_RECT)
        DISPLAYSURF.blit(Hamming_SURF, Hamming_RECT)
        DISPLAYSURF.blit(Euclidean_SURF, Euclidean_RECT)
        DISPLAYSURF.blit(Manhattan_SURF, Manhattan_RECT)
        DISPLAYSURF.blit(Permutation_SURF, Permutation_RECT)
        DISPLAYSURF.blit(LinearConflict_SURF, LinearConflict_RECT)
        DISPLAYSURF.blit(mised_SURF, mised_RECT)
        DISPLAYSURF.blit(counterTextSURF, counterTextRECT)
        DISPLAYSURF.blit(taxicab_SURF, taxicab_RECT)
        counterSURF, counterRECT = self.makeText(
            str(self.BoardData.getMovCounter()), self.MESSAGECOLOR, (210, 210, 210), 130, 40)
        DISPLAYSURF.blit(counterSURF, counterRECT)
        Cmised_SURF, Cmised_RECT = self.makeText(
            f"{self.misplaced_tiles}", self.MESSAGECOLOR, (210, 210, 210),130, 80)
        DISPLAYSURF.blit(Cmised_SURF, Cmised_RECT)
        sum_taxicab_SURF, sum_taxicab_RECT=self.makeText(
            f"{self.taxicab}", self.MESSAGECOLOR, (210, 210, 210),215, 130)
        DISPLAYSURF.blit(sum_taxicab_SURF, sum_taxicab_RECT)

    def slideAnimation(self, board, direction, message, animationSpeed):
        # Note: This function does not check if the move is valid.
        blankx, blanky = self.getBlankPosition(board)
        if direction == self.UP:
            movex = blankx
            movey = blanky + 1
        elif direction == self.DOWN:
            movex = blankx
            movey = blanky - 1
        elif direction == self.LEFT:
            movex = blankx + 1
            movey = blanky
        elif direction == self.RIGHT:
            movex = blankx - 1
            movey = blanky

        # prepare the base surface
        self.drawBoard(board, message)
        baseSurf = DISPLAYSURF.copy()
        # draw a blank space over the moving tile on the baseSurf Surface.
        moveLeft, moveTop = self.getLeftTopOfTile(movex, movey)
        pygame.draw.rect(baseSurf, self.BGCOLOR,
                         (moveLeft, moveTop, self.BoardData.getTILESIZE(), self.BoardData.getTILESIZE()))

        for i in range(0, self.BoardData.getTILESIZE(), animationSpeed):
            # animate the tile sliding over
            self.checkForQuit()
            DISPLAYSURF.blit(baseSurf, (0, 0))
            if direction == self.UP:
                self.drawTile(movex, movey, board[movex][movey], 0, -i)
            if direction == self.DOWN:
                self.drawTile(movex, movey, board[movex][movey], 0, i)
            if direction == self.LEFT:
                self.drawTile(movex, movey, board[movex][movey], -i, 0)
            if direction == self.RIGHT:
                self.drawTile(movex, movey, board[movex][movey], i, 0)

            pygame.display.update()
            DISPLAYSURF.blit(counterTextSURF, counterTextRECT)
            counterSURF, counterRECT = self.makeText(str(self.BoardData.getMovCounter()), self.MESSAGECOLOR,
                                                     self.BGCOLOR, 190, 30)
            DISPLAYSURF.blit(counterSURF, counterRECT)
            FPSCLOCK.tick(self.FPS)

    def generateNewPuzzle(self, numSlides):
        # From a starting configuration, make numSlides number of moves (and
        # animate these moves).
        self.BoardData.resetMovCounter()
        board = deepcopy(self.BoardData.getGoal())

        self.drawBoard(board, '')
        pygame.display.update()
        pygame.time.wait(500)  # pause 500 milliseconds for effect
        lastMove = None
        for i in range(numSlides):
            move = self.getRandomMove(board, lastMove)
            self.slideAnimation(board, move, 'Generating new puzzle...', animationSpeed=int(
                self.BoardData.getTILESIZE() / 3))
            self.makeMove(board, move)
            lastMove = move
        self.misplaced_tiles = Heuristic().Hamming(board)
        self.taxicab = Heuristic().Manhattan(board);
        return board

    def applysolution(self, board, moves):
        for move in moves:
            if self.isValidMove(board, move):
                self.BoardData.incMovCounter()
                self.slideAnimation(board, move, 'solving...', animationSpeed=int(
                    self.BoardData.getTILESIZE() / 2))
                self.makeMove(board, move)

    def resetAnimation(self, board, moves):
        # make all of the moves in allMoves in reverse.
        for move in moves:
            if move == self.UP and self.isValidMove(board, self.DOWN):
                oppositeMove = self.DOWN
            elif move == self.DOWN and self.isValidMove(board, self.UP):
                oppositeMove = self.UP
            elif move == self.RIGHT and self.isValidMove(board, self.LEFT):
                oppositeMove = self.LEFT
            elif move == self.LEFT and self.isValidMove(board, self.RIGHT):
                oppositeMove = self.RIGHT
            self.slideAnimation(board, oppositeMove, '', animationSpeed=int(
                self.BoardData.getTILESIZE() / 2))
            self.makeMove(board, oppositeMove)


    #-----------------------------------------------------------------

    def BestFirstSearch(self, board, heuristic, parent=-1, lastmove=None):
        solutionfound = False
        while not solutionfound:
            if board == self.Goal:
                self.tree.update({-2: [deepcopy(board), heuristic(board), lastmove, parent]})
                self.BoardData.setSearchSpace(self.tree)
                solutionfound = True
            else:
                if self.key == 0:  # this is root
                    self.tree.update({self.key: [deepcopy(board), heuristic(board), lastmove, parent]})
                    parent = self.key  # parent =0
                    self.key += 1
                self.CloseList.append(board)

                children = self.children_of_board(board, lastmove)
                for child in children:
                    if child[0] not in self.CloseList:
                        heuristicvalue = heuristic(child[0])
                        self.tree.update({self.key: [deepcopy(child[0]), heuristicvalue, child[1], parent]})
                        self.Fronte.put((heuristicvalue, self.key, child[1]))   # [[4,1,down], [3,2,'left'],[2,3,'right']]  // ]]
                        self.key += 1

                NextBoard = self.Fronte.get()  # [2,3,right]
                # print(NextState)
                # print("----------------------------")
                # ## nextstate (12, 1, 'up')
                #3: [[[1, 7, 5], [2, 8, 6], [None, 3, 4]], 9, 'down', 0],
                board = self.tree.get(NextBoard[1])[0]    #[1, 7, 5], [2, 8, 6], [None, 3, 4]
                parent = NextBoard[1]
                lastmove = NextBoard[2]

#------------------------------------------------------------------------------------

    def children_of_board(self, board, lastMove):
        validMoves = [ self.UP,self.DOWN, self.LEFT, self.RIGHT]
        children = []
        # remove moves from the list as they are disqualified
        if (lastMove == self.UP) or (not self.isValidMove(board, self.DOWN)):
            validMoves.remove(self.DOWN)
        if lastMove == self.DOWN or not self.isValidMove(board, self.UP):
            validMoves.remove(self.UP)
        if lastMove == self.LEFT or not self.isValidMove(board, self.RIGHT):
            validMoves.remove(self.RIGHT)
        if lastMove == self.RIGHT or not self.isValidMove(board, self.LEFT):
            validMoves.remove(self.LEFT)
        for move in validMoves:
            children.append([self.makeMove(deepcopy(board), move), move])  # [[1,2,3,0],up]
        return children
#-------------------------------------------------------------------------------
    def isValidMove(self, board, move):
        blankx, blanky = self.getBlankPosition(board)
        #[[1, None, 7], [2, 4, 8], [3, 5, 6]]
        # x=0 y=1
        print(board)
        print("blank",blankx,blanky)
        print("-----------------------------------")
        if move == self.UP:
            return blanky != len(board[0]) - 1  # 2
        elif move == self.DOWN:
            return blanky != 0
        elif move == self.LEFT:
            return blankx != len(board) - 1
        elif move == self.RIGHT:
            return blankx != 0
#----------------------------------------------------------------------------------

if __name__ == '__main__':
    GUI().main()
