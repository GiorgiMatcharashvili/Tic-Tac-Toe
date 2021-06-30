import json
import time
import pygame
from random import choice
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
    def __init__(self):
        self.turn = 0
        self.get_moves()
        self.moves_which_i_did = {}

    def get_moves(self):
        with open("moves.json", ) as f:
            self.moves = json.load(f)

    def set_moves(self):
        with open('moves.json', 'w') as f:
            json.dump(self.moves, f, indent=4, separators=None)

    def position_filter(self,my_list):
        ban_list = []
        players_set = set()
        test_env = dict(coordinates_into_XorO)

        # Check if computer can win at first turn
        for coordinates in my_list:
            test_env[coordinates] = OPPONENT
            result = check(test_env)
            if result:
                if OPPONENT in result:
                    return [coordinates]
                elif "Draw" in result:
                    return [coordinates]
            else:
                # Check if Player can win at second turn
                for second_c in self.generate_possible_moves(test_env):
                    test_env[second_c] = PLAYER
                    result2 = check(test_env)
                    if result2:
                        if PLAYER in result2:
                            ban_list.append(coordinates)
                    test_env[second_c] = None

            test_env = dict(coordinates_into_XorO)
        for banned in ban_list:
            if banned in my_list:
                my_list.remove(banned)
        return my_list




    def play(self):
        if self.get_player_positions()==[]:
            self.turn += 1
        else:
            self.turn += 2
        my_id, possible_moves = self.record_or_not()

        print("in play, my_id: ",my_id," filtered moves: ",possible_moves)

        position = choice(possible_moves)

        self.make_move(position, my_id)

    def get_computer_positions(self):
        send_list = []

        for coordinates in coordinates_into_XorO:
            if coordinates_into_XorO[coordinates] == OPPONENT:
                send_list.append(coordinates)

        return send_list

    def get_player_positions(self):
        send_list = []
        for coordinates in coordinates_into_XorO:
            if coordinates_into_XorO[coordinates] == PLAYER:
                send_list.append(coordinates)

        return send_list

    def generate_possible_moves(self,json=coordinates_into_XorO):
        send_list = []

        for coordinates in json:
            if not json[coordinates]:
                send_list.append(coordinates)

        return send_list

    def generate_id(self,json):
        id = ""

        id += str(json["turn"])

        for c in json["computer's positions"]:
            for each in c:
                id += str(each)

        for p in json["player's positions"]:
            for each in p:
                id += str(each)

        return id

    def record_or_not(self):
        send_json = {
            "turn": self.turn,
            "computer's positions": self.get_computer_positions(),
            "player's positions": self.get_player_positions(),
            "possible moves": self.position_filter(self.generate_possible_moves())
        }

        self.get_moves()

        new_id = self.generate_id(send_json)

        self.moves_which_i_did = {}

        if not new_id in self.moves.keys():
            self.moves[new_id] = send_json

            with open('moves.json', 'w') as f:
                json.dump(self.moves, f, indent=4, separators=None)
            self.moves_which_i_did[new_id] = []

            return (new_id, send_json["possible moves"])
        else:
            self.moves_which_i_did[new_id] = []
            if self.moves[new_id]["possible moves"]:
                return (new_id, self.moves[new_id]["possible moves"])
            else:
                return (new_id, send_json["possible moves"])

    def make_move(self, position, my_id):
        position = (position[0],position[1])
        place_box(screen,position,OPPONENT)

        self.moves_which_i_did[my_id].append(position)

    def lost(self):
        # Punish
        self.get_moves()

        for move_id in self.moves_which_i_did:
            move = self.moves_which_i_did[move_id][0]
            print("Moves_which_i_did",self.moves_which_i_did)
            move = [move[0],move[1]]

            self.moves[move_id]['possible moves'].remove(move)
            print("remove: ",move_id,move)

        self.set_moves()

    def win(self):
        # Reward
        self.get_moves()

        for move_id in self.moves_which_i_did:
            move = self.moves_which_i_did[move_id]
            print("Moves_which_i_did", self.moves_which_i_did)
            move = [move[0], move[1]]

            self.moves[move_id]['possible moves'].append(move)
            print("add: ",move_id, move)

        self.set_moves()

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
            time.sleep(1)
            plays = PLAYER
            computer.play()

        result = check()
        if result:
            if PLAYER in result:
                show_text(screen, f"        {result}         ", (300, 50), GREEN, 33)
                computer.lost()
            elif OPPONENT in result:
                show_text(screen, f"        {result}         ", (300, 50), RED, 33)
                computer.win()
            else:
                show_text(screen, f"        {result}         ", (300, 50), BLACK, 33)

            time.sleep(1)
            running = False

game()