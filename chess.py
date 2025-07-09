import pygame
from pygame.locals import *
import random

from piece import Piece
from utils import Utils

import time


class Chess(object):
    def __init__(self, screen, pieces_src, square_coords, square_length):
        # display surface
        self.screen = screen
        # create an object of class to show chess pieces on the board
        self.chess_pieces = Piece(pieces_src, cols=6, rows=2)
        # store coordinates of the chess board squares
        self.board_locations = square_coords
        # length of the side of a chess board square
        self.square_length = square_length
        # dictionary to keeping track of player turn
        self.turn = {"white": 1,
                     "black": 0}

        # list containing possible moves for the selected piece
        self.moves = []
        #
        self.utils = Utils()

        # mapping of piece names to index of list containing piece coordinates on spritesheet
        self.pieces = {
            "white_pawn":   5,
            "white_knight": 3,
            "white_bishop": 2,
            "white_rook":   4,
            "white_king":   0,
            "white_queen":  1,
            "black_pawn":   11,
            "black_knight": 9,
            "black_bishop": 8,
            "black_rook":   10,
            "black_king":   6,
            "black_queen":  7
        }

        # list containing captured pieces
        self.captured = []
        #
        self.winner = ""

        self.reset()

    def reset(self):
        self.moves = []
        self.captured = []
        self.winner = ""

        self.piece_location = {}
        x = 0
        for i in range(97, 105):  # 'a' to 'h'
            a = 8
            y = 0
            self.piece_location[chr(i)] = {}
            while a > 0:
                self.piece_location[chr(i)][a] = ["", False, [x, y]]
                a -= 1
                y += 1
            x += 1

        # === Generate Chess960 Starting Position ===
        back_rank = [None] * 8

        # 1. Place bishops on opposite-colored squares
        bishop1 = random.choice([0, 2, 4, 6])
        bishop2 = random.choice([1, 3, 5, 7])
        back_rank[bishop1] = "bishop"
        back_rank[bishop2] = "bishop"

        # 2. Place queen in one of the remaining slots
        remaining = [i for i in range(8) if back_rank[i] is None]
        queen = random.choice(remaining)
        back_rank[queen] = "queen"

        # 3. Place knights in two of the remaining slots
        remaining = [i for i in range(8) if back_rank[i] is None]
        knight1, knight2 = random.sample(remaining, 2)
        back_rank[knight1] = "knight"
        back_rank[knight2] = "knight"

        # 4. Place rooks and king such that king is between the rooks
        remaining = [i for i in range(8) if back_rank[i] is None]
        remaining.sort()
        rook1, king, rook2 = remaining[0], remaining[1], remaining[2]
        back_rank[rook1] = "rook"
        back_rank[king] = "king"
        back_rank[rook2] = "rook"

        # === Place pieces on board ===
        for idx, piece in enumerate(back_rank):
            file_char = chr(97 + idx)  # 'a' to 'h'
            # White pieces on rank 1 and 2
            self.piece_location[file_char][1][0] = "white_" + piece
            self.piece_location[file_char][2][0] = "white_pawn"
            # Black pieces on rank 8 and 7
            self.piece_location[file_char][8][0] = "black_" + piece
            self.piece_location[file_char][7][0] = "black_pawn"

        # Reset turn to white
        self.turn = {"white": 1, "black": 0}

    #

    def play_turn(self):
        # white color
        white_color = (255, 255, 255)
        # create fonts for texts
        small_font = pygame.font.SysFont("comicsansms", 20)
        # create text to be shown on the game menu
        if self.turn["black"]:
            turn_text = small_font.render("Turn: Black", True, white_color)
        elif self.turn["white"]:
            turn_text = small_font.render("Turn: White", True, white_color)

        # show welcome text
        self.screen.blit(turn_text,
                         ((self.screen.get_width() - turn_text.get_width()) // 2,
                          10))

        # let player with black piece play
        if (self.turn["black"]):
            self.move_piece("black")
        # let player with white piece play
        elif (self.turn["white"]):
            self.move_piece("white")

        # After turn, check for checkmate or stalemate
        current = "white" if self.turn["white"] else "black"
        if not self.has_legal_moves(current):
            if self.is_in_check(current):
                self.winner = "Black" if current == "white" else "White"
                print(f"{self.winner} wins by checkmate!")
            else:
                self.winner = "Draw"
                print("Stalemate!")

    # method to draw pieces on the chess board
    def draw_pieces(self):
        transparent_green = (0, 194, 39, 170)
        transparent_blue = (28, 21, 212, 170)

        # create a transparent surface
        surface = pygame.Surface(
            (self.square_length, self.square_length), pygame.SRCALPHA)
        surface.fill(transparent_green)

        surface1 = pygame.Surface(
            (self.square_length, self.square_length), pygame.SRCALPHA)
        surface1.fill(transparent_blue)

        # loop to change background color of selected piece
        for val in self.piece_location.values():
            for value in val.values():
                # name of the piece in the current location
                piece_name = value[0]
                # x, y coordinates of the current piece
                piece_coord_x, piece_coord_y = value[2]

                # change background color of piece if it is selected
                if value[1] and len(value[0]) > 5:
                    # if the piece selected is a black piece
                    if value[0][:5] == "black":
                        self.screen.blit(
                            surface, self.board_locations[piece_coord_x][piece_coord_y])
                        if len(self.moves) > 0:
                            for move in self.moves:
                                x_coord = move[0]
                                y_coord = move[1]
                                if x_coord >= 0 and y_coord >= 0 and x_coord < 8 and y_coord < 8:
                                    self.screen.blit(
                                        surface, self.board_locations[x_coord][y_coord])
                    # if the piece selected is a white piece
                    elif value[0][:5] == "white":
                        self.screen.blit(
                            surface1, self.board_locations[piece_coord_x][piece_coord_y])
                        if len(self.moves) > 0:
                            for move in self.moves:
                                x_coord = move[0]
                                y_coord = move[1]
                                if x_coord >= 0 and y_coord >= 0 and x_coord < 8 and y_coord < 8:
                                    self.screen.blit(
                                        surface1, self.board_locations[x_coord][y_coord])

        # draw all chess pieces
        for val in self.piece_location.values():
            for value in val.values():
                # name of the piece in the current location
                piece_name = value[0]
                # x, y coordinates of the current piece
                piece_coord_x, piece_coord_y = value[2]
                # check if there is a piece at the square
                if (len(value[0]) > 1):
                    # draw piece on the board
                    self.chess_pieces.draw(self.screen, piece_name,
                                           self.board_locations[piece_coord_x][piece_coord_y])

    # method to find the possible moves of the selected piece

    def possible_moves(self, piece_name, piece_coord, simulate=False):
        # list to store possible moves of the selected piece
        positions = []
        # find the possible locations to put a piece
        if len(piece_name) > 0:
            # get x, y coordinate
            x_coord, y_coord = piece_coord
            # calculate moves for bishop
            if piece_name[6:] == "bishop":
                positions = self.diagonal_moves(
                    positions, piece_name, piece_coord)

            # calculate moves for pawn
            elif piece_name[6:] == "pawn":
                # convert list index to dictionary key
                columnChar = chr(97 + x_coord)
                rowNo = 8 - y_coord

                # calculate moves for white pawn
                if piece_name == "black_pawn":
                    if y_coord + 1 < 8:
                        # get row in front of black pawn
                        rowNo = rowNo - 1
                        front_piece = self.piece_location[columnChar][rowNo][0]

                        # pawns cannot move when blocked by another another pawn
                        if (front_piece[6:] != "pawn"):
                            positions.append([x_coord, y_coord+1])
                            # black pawns can move two positions ahead for first move
                            if y_coord < 2:
                                positions.append([x_coord, y_coord+2])

                        # EM PASSANT
                        # diagonal to the left
                        if x_coord - 1 >= 0 and y_coord + 1 < 8:
                            x = x_coord - 1
                            y = y_coord + 1

                            # convert list index to dictionary key
                            columnChar = chr(97 + x)
                            rowNo = 8 - y
                            to_capture = self.piece_location[columnChar][rowNo]

                            if (to_capture[0][:5] == "white"):
                                positions.append([x, y])

                        # diagonal to the right
                        if x_coord + 1 < 8 and y_coord + 1 < 8:
                            x = x_coord + 1
                            y = y_coord + 1

                            # convert list index to dictionary key
                            columnChar = chr(97 + x)
                            rowNo = 8 - y
                            to_capture = self.piece_location[columnChar][rowNo]

                            if (to_capture[0][:5] == "white"):
                                positions.append([x, y])

                # calculate moves for white pawn
                elif piece_name == "white_pawn":
                    if y_coord - 1 >= 0:
                        # get row in front of black pawn
                        rowNo = rowNo + 1
                        front_piece = self.piece_location[columnChar][rowNo][0]

                        # pawns cannot move when blocked by another another pawn
                        if (front_piece[6:] != "pawn"):
                            positions.append([x_coord, y_coord-1])
                            # black pawns can move two positions ahead for first move
                            if y_coord > 5:
                                positions.append([x_coord, y_coord-2])

                        # EM PASSANT
                        # diagonal to the left
                        if x_coord - 1 >= 0 and y_coord - 1 >= 0:
                            x = x_coord - 1
                            y = y_coord - 1

                            # convert list index to dictionary key
                            columnChar = chr(97 + x)
                            rowNo = 8 - y
                            to_capture = self.piece_location[columnChar][rowNo]

                            if (to_capture[0][:5] == "black"):
                                positions.append([x, y])

                        # diagonal to the right
                        if x_coord + 1 < 8 and y_coord - 1 >= 0:
                            x = x_coord + 1
                            y = y_coord - 1

                            # convert list index to dictionary key
                            columnChar = chr(97 + x)
                            rowNo = 8 - y
                            to_capture = self.piece_location[columnChar][rowNo]

                            if (to_capture[0][:5] == "black"):
                                positions.append([x, y])

            # calculate moves for rook
            elif piece_name[6:] == "rook":
                # find linear moves
                positions = self.linear_moves(
                    positions, piece_name, piece_coord)

            # calculate moves for knight
            elif piece_name[6:] == "knight":
                # left positions
                if (x_coord - 2) >= 0:
                    if (y_coord - 1) >= 0:
                        positions.append([x_coord-2, y_coord-1])
                    if (y_coord + 1) < 8:
                        positions.append([x_coord-2, y_coord+1])
                # top positions
                if (y_coord - 2) >= 0:
                    if (x_coord - 1) >= 0:
                        positions.append([x_coord-1, y_coord-2])
                    if (x_coord + 1) < 8:
                        positions.append([x_coord+1, y_coord-2])
                # right positions
                if (x_coord + 2) < 8:
                    if (y_coord - 1) >= 0:
                        positions.append([x_coord+2, y_coord-1])
                    if (y_coord + 1) < 8:
                        positions.append([x_coord+2, y_coord+1])
                # bottom positions
                if (y_coord + 2) < 8:
                    if (x_coord - 1) >= 0:
                        positions.append([x_coord-1, y_coord+2])
                    if (x_coord + 1) < 8:
                        positions.append([x_coord+1, y_coord+2])

            # calculate movs for king
            elif piece_name[6:] == "king":
                if (y_coord - 1) >= 0:
                    # top spot
                    positions.append([x_coord, y_coord-1])

                if (y_coord + 1) < 8:
                    # bottom spot
                    positions.append([x_coord, y_coord+1])

                if (x_coord - 1) >= 0:
                    # left spot
                    positions.append([x_coord-1, y_coord])
                    # top left spot
                    if (y_coord - 1) >= 0:
                        positions.append([x_coord-1, y_coord-1])
                    # bottom left spot
                    if (y_coord + 1) < 8:
                        positions.append([x_coord-1, y_coord+1])

                if (x_coord + 1) < 8:
                    # right spot
                    positions.append([x_coord+1, y_coord])
                    # top right spot
                    if (y_coord - 1) >= 0:
                        positions.append([x_coord+1, y_coord-1])
                    # bottom right spot
                    if (y_coord + 1) < 8:
                        positions.append([x_coord+1, y_coord+1])

            # calculate movs for queen
            elif piece_name[6:] == "queen":
                # find diagonal positions
                positions = self.diagonal_moves(
                    positions, piece_name, piece_coord)

                # find linear moves
                positions = self.linear_moves(
                    positions, piece_name, piece_coord)

            # list of positions to be removed
            to_remove = []

            # remove positions that overlap other pieces of the current player
            for pos in positions:
                x, y = pos

                # convert list index to dictionary key
                columnChar = chr(97 + x)
                rowNo = 8 - y

                # find the pieces to remove
                des_piece_name = self.piece_location[columnChar][rowNo][0]
                if (des_piece_name[:5] == piece_name[:5]):
                    to_remove.append(pos)

            # remove position from positions list
            for i in to_remove:
                positions.remove(i)
        if not simulate and piece_name[6:] != "king":
            legal_positions = []
            for move in positions:
                from_file = chr(97 + piece_coord[0])
                from_rank = 8 - piece_coord[1]
                backup = self._simulate_move(from_file, from_rank, move)
                if not self.is_in_check(piece_name[:5]):
                    legal_positions.append(move)
                self._undo_simulation(from_file, from_rank, move, backup)
            positions = legal_positions

        # return list containing possible moves for the selected piece
        return positions

    def move_piece(self, turn):
        # get the coordinates of the square selected on the board
        square = self.get_selected_square()

        # if a square was selected
        if square:
            # get name of piece on the selected square
            piece_name = square[0]
            # color of piece on the selected square
            piece_color = piece_name[:5]
            # board column character
            columnChar = square[1]
            # board row number
            rowNo = square[2]

            # get x, y coordinates
            x, y = self.piece_location[columnChar][rowNo][2]

            # if there's a piece on the selected square
            if (len(piece_name) > 0) and (piece_color == turn):
                # find possible moves for thr piece
                self.moves = self.possible_moves(piece_name, [x, y])

            # checkmate mechanism
            p = self.piece_location[columnChar][rowNo]

            for i in self.moves:
                if i == [x, y]:
                    if (p[0][:5] == turn) or len(p[0]) == 0:
                        self.validate_move([x, y])
                    else:
                        self.capture_piece(turn, [columnChar, rowNo], [x, y])

            # only the player with the turn gets to play
            if (piece_color == turn):
                # change selection flag from all other pieces
                for k in self.piece_location.keys():
                    for key in self.piece_location[k].keys():
                        self.piece_location[k][key][1] = False

                # change selection flag of the selected piece
                self.piece_location[columnChar][rowNo][1] = True

    def get_selected_square(self):
        # get left event
        left_click = self.utils.left_click_event()

        # if there's a mouse event
        if left_click:
            # get mouse event
            mouse_event = self.utils.get_mouse_event()

            for i in range(len(self.board_locations)):
                for j in range(len(self.board_locations)):
                    rect = pygame.Rect(self.board_locations[i][j][0], self.board_locations[i][j][1],
                                       self.square_length, self.square_length)
                    collision = rect.collidepoint(
                        mouse_event[0], mouse_event[1])
                    if collision:
                        selected = [rect.x, rect.y]
                        # find x, y coordinates the selected square
                        for k in range(len(self.board_locations)):
                            #
                            try:
                                l = None
                                l = self.board_locations[k].index(selected)
                                if l != None:
                                    # reset color of all selected pieces
                                    for val in self.piece_location.values():
                                        for value in val.values():
                                            # [piece name, currently selected, board coordinates]
                                            if not value[1]:
                                                value[1] = False

                                    # get column character and row number of the chess piece
                                    columnChar = chr(97 + k)
                                    rowNo = 8 - l
                                    # get the name of the
                                    piece_name = self.piece_location[columnChar][rowNo][0]

                                    return [piece_name, columnChar, rowNo]
                            except:
                                pass
        else:
            return None

    def capture_piece(self, turn, chess_board_coord, piece_coord):
        # get x, y coordinate of the destination piece
        x, y = piece_coord

        # get chess board coordinate
        columnChar, rowNo = chess_board_coord

        p = self.piece_location[columnChar][rowNo]

        if p[0] == "white_king":
            self.winner = "Black"
            print("Black wins")
        elif p[0] == "black_king":
            self.winner = "White"
            print("White wins")

        # add the captured piece to list
        self.captured.append(p)
        # move source piece to its destination
        self.validate_move(piece_coord)

    def validate_move(self, destination):
        desColChar = chr(97 + destination[0])
        desRowNo = 8 - destination[1]

        for k in self.piece_location.keys():
            for key in self.piece_location[k].keys():
                board_piece = self.piece_location[k][key]

                if board_piece[1]:
                    # unselect the source piece
                    self.piece_location[k][key][1] = False
                    # get the name of the source piece
                    piece_name = self.piece_location[k][key][0]
                    # move the source piece to the destination piece
                    self.piece_location[desColChar][desRowNo][0] = piece_name

                    src_name = self.piece_location[k][key][0]
                    # remove source piece from its current position
                    self.piece_location[k][key][0] = ""

                    # change turn
                    if (self.turn["black"]):
                        self.turn["black"] = 0
                        self.turn["white"] = 1
                    elif ("white"):
                        self.turn["black"] = 1
                        self.turn["white"] = 0

                    src_location = k + str(key)
                    des_location = desColChar + str(desRowNo)
                    print("{} moved from {} to {}".format(
                        src_name,  src_location, des_location))

    # helper function to find diagonal moves

    def diagonal_moves(self, positions, piece_name, piece_coord):
        # reset x and y coordinate values
        x, y = piece_coord
        # find top left diagonal spots
        while (True):
            x = x - 1
            y = y - 1
            if (x < 0 or y < 0):
                break
            else:
                positions.append([x, y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

        # reset x and y coordinate values
        x, y = piece_coord
        # find bottom right diagonal spots
        while (True):
            x = x + 1
            y = y + 1
            if (x > 7 or y > 7):
                break
            else:
                positions.append([x, y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

        # reset x and y coordinate values
        x, y = piece_coord
        # find bottom left diagonal spots
        while (True):
            x = x - 1
            y = y + 1
            if (x < 0 or y > 7):
                break
            else:
                positions.append([x, y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

        # reset x and y coordinate values
        x, y = piece_coord
        # find top right diagonal spots
        while (True):
            x = x + 1
            y = y - 1
            if (x > 7 or y < 0):
                break
            else:
                positions.append([x, y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

        return positions

    # helper function to find horizontal and vertical moves

    def linear_moves(self, positions, piece_name, piece_coord):
        # reset x, y coordniate value
        x, y = piece_coord
        # horizontal moves to the left
        while (x > 0):
            x = x - 1
            positions.append([x, y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

        # reset x, y coordniate value
        x, y = piece_coord
        # horizontal moves to the right
        while (x < 7):
            x = x + 1
            positions.append([x, y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

        # reset x, y coordniate value
        x, y = piece_coord
        # vertical moves upwards
        while (y > 0):
            y = y - 1
            positions.append([x, y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

        # reset x, y coordniate value
        x, y = piece_coord
        # vertical moves downwards
        while (y < 7):
            y = y + 1
            positions.append([x, y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

        return positions

    def is_in_check(self, color):
        king_pos = None
        for file in self.piece_location:
            for rank in self.piece_location[file]:
                piece = self.piece_location[file][rank][0]
                if piece == f"{color}_king":
                    king_pos = self.piece_location[file][rank][2]
                    break
        if not king_pos:
            return True  # king missing = game over

        opponent = "white" if color == "black" else "black"
        for file in self.piece_location:
            for rank in self.piece_location[file]:
                piece = self.piece_location[file][rank][0]
                if piece.startswith(opponent):
                    from_x, from_y = self.piece_location[file][rank][2]
                    moves = self.possible_moves(
                        piece, [from_x, from_y], simulate=True)
                    if king_pos in moves:
                        return True
        return False

    def has_legal_moves(self, color):
        for file in self.piece_location:
            for rank in self.piece_location[file]:
                piece = self.piece_location[file][rank][0]
                if piece.startswith(color):
                    from_x, from_y = self.piece_location[file][rank][2]
                    moves = self.possible_moves(piece, [from_x, from_y])
                    for move in moves:
                        backup = self._simulate_move(file, rank, move)
                        if not self.is_in_check(color):
                            self._undo_simulation(file, rank, move, backup)
                            return True
                        self._undo_simulation(file, rank, move, backup)
        return False

    def _simulate_move(self, file, rank, move):
        des_col = chr(97 + move[0])
        des_row = 8 - move[1]
        piece = self.piece_location[file][rank][0]
        captured = self.piece_location[des_col][des_row][0]

        self.piece_location[des_col][des_row][0] = piece
        self.piece_location[file][rank][0] = ""
        return captured

    def _undo_simulation(self, file, rank, move, captured_piece):
        des_col = chr(97 + move[0])
        des_row = 8 - move[1]
        piece = self.piece_location[des_col][des_row][0]

        self.piece_location[file][rank][0] = piece
        self.piece_location[des_col][des_row][0] = captured_piece
