from typing import *

class Piece:
    white_color = '#f0f0f0'
    black_color = '#b58863'
    is_queen = False

    def __init__(self, color, row, col):
        self.color = color.lower() if color is not None else None
        if self.color is not None:
            self.vis_color = self.white_color if color == 'white' else self.black_color
        else:
            self.vis_color = None
        self.row = row
        self.col = col
        self.options = []
        self.best_option = None

    def add_option(self,
                   new_position,
                   is_capture=False,
                   is_queen=False):
        self.options.append({
            'position': new_position,
            'is_capture': is_capture,
            'is_queen': is_queen
        })

    @property
    def score(self):
        score = []
        for option in self.options:
            if option['is_capture']:
                score.append(8)
            else:
                score.append(1 + self.col_eff)
        if len(self.options) > 0:
            self.best_option = self.options[score.index(max(score))]
        return max(score) if len(score) > 0 else 0

    @property
    def col_eff(self):
        if self.color == 'white':
            return self.row
        else:
            return 7 - self.row


    def __repr__(self):
        return f'{self.color} piece at {self.row}, {self.col}'

    def __getitem__(self, item):
        if item == 0:
            return self.row
        elif item == 1:
            return self.col
        else:
            raise IndexError('Index out of range')



class Checkers:
    is_initialized = False
    def __init__(self):
        self.initialize_board()
        self.current_player = 'White'

    def initialize_board(self):
        self._board = [[None] * 8 for _ in range(8)]
        for row in range(8):
            for col in range(8):
                if row % 2 != col % 2:
                    if row < 3:
                        self._board[row][col] = Piece('black', col, row)
                    elif row > 4:
                        self._board[row][col] = Piece('white', col, row)
                    else:
                        self._board[row][col] = Piece(None, col, row)
                else:
                    self._board[row][col] = Piece(None, col, row)
        self.is_initialized = True

    @property
    def board(self):
        assert self.is_initialized, 'Board is not initialized'
        return_board = [[None] * 8 for _ in range(8)]
        for row in range(8):
            for col in range(8):
                return_board[row][col] = self._board[row][col].vis_color
        return return_board

    def next(self, board, player):
        self.set_board(board)
        self.current_player = player

        # Check player valid moves
        player_pieces = self.get_player_pieces(self.current_player)
        scores = []
        for piece in player_pieces:
            piece.options = []
            if self.current_player == 'white':
                if not piece.is_queen:
                    if piece.row - 1 >= 0 and piece.col - 1 >= 0 and self._board[piece.row - 1][piece.col - 1].color == None:
                        piece.add_option((piece.row - 1, piece.col - 1), is_capture=False)
                    if piece.row - 1 >= 0 and piece.col + 1 <= 7 and self._board[piece.row - 1][piece.col + 1].color == None:
                        piece.add_option((piece.row - 1, piece.col + 1), is_capture=False)
                    if piece.row - 2 >= 0 and piece.col - 2 >= 0 and self._board[piece.row - 1][piece.col - 1].color == 'black' and self._board[piece.row - 2][piece.col - 2].color == None:
                        piece.add_option((piece.row - 2, piece.col - 2), is_capture=True)
                    if piece.row - 2 >= 0 and piece.col + 2 <= 7 and self._board[piece.row - 1][piece.col + 1].color == 'black' and self._board[piece.row - 2][piece.col + 2].color == None:
                        piece.add_option((piece.row - 2, piece.col + 2), is_capture=True)
                else:
                    pass

            else:
                if not piece.is_queen:
                    if piece.row + 1 <= 7 and piece.col - 1 >= 0 and self._board[piece.row + 1][piece.col - 1].color == None:
                        piece.add_option((piece.row + 1, piece.col - 1), is_capture=False)
                    if piece.row + 1 <= 7 and piece.col + 1 <= 7 and self._board[piece.row + 1][piece.col + 1].color == None:
                        piece.add_option((piece.row + 1, piece.col + 1), is_capture=False)
                    if piece.row + 2 <= 7 and piece.col - 2 >= 0 and self._board[piece.row + 1][piece.col - 1].color == 'white' and self._board[piece.row + 2][piece.col - 2].color == None:
                        piece.add_option((piece.row + 2, piece.col - 2), is_capture=True)
                    if piece.row + 2 <= 7 and piece.col + 2 <= 7 and self._board[piece.row + 1][piece.col + 1].color == 'white' and self._board[piece.row + 2][piece.col + 2].color == None:
                        piece.add_option((piece.row + 2, piece.col + 2), is_capture=True)

        for piece in player_pieces:
            scores.append(piece.score)
        best_piece = player_pieces[scores.index(max(scores))]
        best_move = best_piece.best_option
        if not best_piece.best_option['is_capture']:
            self._board[best_piece.row][best_piece.col] = Piece(None, best_piece.row, best_piece.col)
            self._board[best_move['position'][0]][best_move['position'][1]] = Piece(self.current_player, best_move['position'][0], best_move['position'][1])
        else:
            self._board[best_piece.row][best_piece.col] = Piece(None, best_piece.row, best_piece.col)
            self._board[best_move['position'][0]][best_move['position'][1]] = Piece(self.current_player, best_move['position'][0], best_move['position'][1])
            # Calculate eat direction
            eat_direction = (best_move['position'][0] - best_piece.row, best_move['position'][1] - best_piece.col)
            self._board[best_piece.row + eat_direction[0]][best_piece.col + eat_direction[1]] = Piece(None, best_piece.row + eat_direction[0], best_piece.col + eat_direction[1])
            




        self.current_player = 'white' if self.current_player.lower() == 'black' else 'black'

        return self.board, self.current_player

    def get_player_pieces(self, player) -> List[Piece]:
        pieces = []
        for row in range(8):
            for col in range(8):
                if self._board[row][col].color == player:
                    pieces.append(self._board[row][col])
        return pieces

    def set_board(self, board):
        for row in range(8):
            for col in range(8):
                if board[row][col] == Piece.white_color:
                    self._board[row][col] = Piece('white', row, col)
                elif board[row][col] == Piece.black_color:
                    self._board[row][col] = Piece('black', row, col)
                else:
                    self._board[row][col] = Piece(None, row, col)


