import time
import pygame
from random import random

########################################################################################################################
##################################################### Constants ########################################################
########################################################################################################################

BACKGROUND_COLOR = (255,255,255)
BLACK = (0, 0, 0)
RED = (255,0,0)
GREEN = (0,255,0)

SELECTED_RED = (255,180,2)
CHOSEN_RED = (236, 33, 37)

########################################################################################################################
##################################################### Variables ########################################################
########################################################################################################################

coordinates_into_XorO = {}
for x in range(0,3):
        for y in range(0,3):
            coordinates_into_XorO[x,y] = None
pygame.init()

########################################################################################################################
################################################## Functions for game ##################################################
########################################################################################################################

def createDisplay(size,name):
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption(name)

    screen.fill(BACKGROUND_COLOR)

    pygame.display.flip()

    return screen

def drawWindow(screen):
    # Draw horizontal lines
    for x in range(75,550,150):pygame.draw.line(screen, BLACK, (x,75), (x,525), 2)

    # Draw vertical lines
    for y in range(75,550,150):pygame.draw.line(screen, BLACK, (75, y), (525, y), 2)


    pygame.display.flip()

    return screen

def place_box(screen, coordinates, XorO):
    x = coordinates[0]
    y = coordinates[1]

    real_x = 150 + (150 * x)
    real_y = 150 + (150 * y)

    font = pygame.font.Font('freesansbold.ttf', 100)

    text = font.render(XorO, True, BLACK, BACKGROUND_COLOR)
    textRect = text.get_rect()

    textRect.center = (real_x, real_y)
    screen.blit(text, textRect)
    pygame.display.flip()

    coordinates_into_XorO[coordinates] = XorO

def show_text(screen, txt, position, color, font_size):

    font = pygame.font.Font('freesansbold.ttf', font_size)

    text = font.render(txt, True, color, BACKGROUND_COLOR)

    textRect = text.get_rect()
    textRect.center = position
    screen.blit(text, textRect)
    pygame.display.flip()

def show_coordinates():
    font = pygame.font.Font('freesansbold.ttf', 40)
    for x in range(0,3):
        for y in range(0,3):
            text = font.render(str(x)+","+str(y), True, BLACK, BACKGROUND_COLOR)
            textRect = text.get_rect()
            real_x = 150 + (150 * x)
            real_y = 150 + (150 * y)
            textRect.center = (real_x, real_y)
            screen.blit(text, textRect)
            pygame.display.flip()

def check(json=coordinates_into_XorO):

    def check_if_all_same(line):
        XandOs_set = set()

        for coordinates in line:
            XorO = json[coordinates]
            if XorO: XandOs_set.add(XorO)
            else: return False

        if len(XandOs_set)==1: return next(iter(XandOs_set))

    # Check for horizontal lines
    for y in range(0,3):
        line = []
        for x in range(0,3):
            line.append((x,y))

        answer = check_if_all_same(line)
        if answer: return answer+" Wins!"
        line.clear()

    # Check for vertical lines
    for x in range(0,3):
        line = []
        for y in range(0,3):
            line.append((x,y))

        answer = check_if_all_same(line)
        if answer: return answer + " Wins!"
        line.clear()

    # Check for diagonally lines
    diagonals = [[(0, 0), (1, 1), (2, 2)],[(2, 0), (1, 1), (0, 2)]]
    for line in diagonals:
        answer = check_if_all_same(line)
        if answer: return answer + " Wins!"

    # Check for draw
    if not None in json.values(): return "Draw!"


########################################################################################################################
################################################# Functions for player #################################################
########################################################################################################################

def interact(coordinates):
    if not coordinates_into_XorO[coordinates]:
        place_box(screen,coordinates,PLAYER)
        return True
    else:
        return False

########################################################################################################################
########################################################## AI ##########################################################
########################################################################################################################

class AI:
    def make_move(self, position):
        position = (position[0],position[1])
        place_box(screen,position,OPPONENT)

    def minimax(self, test_env, alpha, beta,isMaximizing):

        result = check(test_env)

        if result:
            if OPPONENT in result:
                return 1
            elif PLAYER in result:
                return -1
            elif "Draw" in result:
                return 0

        if isMaximizing:
            bestScore = -800
            for coordinates in test_env.keys():
                if test_env[coordinates] == None:
                    test_env[coordinates] = OPPONENT
                    score = self.minimax(test_env, alpha, beta,False)
                    test_env[coordinates] = None
                    bestScore = max(bestScore,score)
                    alpha = max(alpha,score)
                    if beta <= alpha:break
            return bestScore

        else:
            bestScore = 800
            for coordinates in test_env.keys():
                if test_env[coordinates] == None:
                    test_env[coordinates] = PLAYER
                    score = self.minimax(test_env, alpha, beta, True)
                    test_env[coordinates] = None
                    bestScore = min(bestScore,score)
                    beta = min(beta,score)
                    if beta <= alpha: break
            return bestScore

    def play(self):
        bestScore = -800
        bestMove = 0

        test_env = dict(coordinates_into_XorO)

        for coordinates in coordinates_into_XorO:
            if coordinates_into_XorO[coordinates] == None:
                test_env[coordinates] = OPPONENT
                score = self.minimax(test_env, -800, 800, False)
                test_env[coordinates] = None
                if (score > bestScore):
                    bestScore = score
                    bestMove = coordinates

        self.make_move(bestMove)
        return

########################################################################################################################
####################################################### Flow ###########################################################
########################################################################################################################

def choose_window():
    is_selected = None

    # Prepare choose between X or O UI
    screen = createDisplay((600, 600), "Tic-Tac-Toe")

    show_text(screen,"Double click to Choose:", (300,150), BLACK, 32)

    show_text(screen, "X", (180, 300), BLACK, 100)

    show_text(screen, "O", (420, 300), BLACK, 100)

    running = True

    while running:
        events = pygame.event.get()

        if events != []:
            for event in events:
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos


                    if x in range(118,254) and y in range(225,357):
                        if is_selected == "X":
                            show_text(screen, "X", (180, 300), CHOSEN_RED, 100)
                            time.sleep(0.2)
                            return screen, "X"
                        else:
                            show_text(screen, "X", (180, 300), SELECTED_RED, 100)
                            show_text(screen, "O", (420, 300), BLACK, 100)
                            is_selected = "X"
                    elif x in range(361,479) and y in range(230,354):
                        if is_selected == "O":
                            show_text(screen, "O", (420, 300), CHOSEN_RED, 100)
                            time.sleep(0.2)
                            return screen, "O"
                        else:
                            show_text(screen, "X", (180, 300), BLACK, 100)
                            show_text(screen, "O", (420, 300), SELECTED_RED, 100)
                            is_selected = "O"

def game():
    global PLAYER,OPPONENT,screen
    screen, PLAYER = choose_window()

    if PLAYER == "X":OPPONENT="O"
    elif PLAYER == "O":OPPONENT="X"

    computer = AI()

    screen.fill(BACKGROUND_COLOR)
    drawWindow(screen)

    plays = "X"

    running = True

    while running:
        #show_coordinates()
        events = pygame.event.get()

        show_text(screen, " "+str(plays)+" turn to Play!", (300, 50), BLACK, 32)

        if plays == PLAYER:
            if events != []:
                for event in events:
                    if event.type == pygame.QUIT:
                        running = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos

                        row = None
                        column = None

                        # detect row
                        if x in range(75, 225):
                            row = 0
                        elif x in range(225, 375):
                            row = 1
                        elif x in range(375, 525):
                            row = 2

                        # detect column
                        if y in range(75, 225):
                            column = 0
                        elif y in range(225, 375):
                            column = 1
                        elif y in range(375, 525):
                            column = 2

                        if row is not None and column is not None:
                            is_placed = interact((row,column))

                            if is_placed: plays = OPPONENT

        elif plays == OPPONENT:
            time.sleep(random())
            plays = PLAYER
            computer.play()

        result = check()
        if result:
            if PLAYER in result:
                show_text(screen, f"        {result}         ", (300, 50), GREEN, 33)
            elif OPPONENT in result:
                show_text(screen, f"        {result}         ", (300, 50), RED, 33)
            else:
                show_text(screen, f"        {result}         ", (300, 50), BLACK, 33)

            time.sleep(1)
            running = False

game()