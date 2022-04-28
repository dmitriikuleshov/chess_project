from copy import deepcopy

WHITE = 1
BLACK = 2


def opponent(color):
    if color == WHITE:
        return BLACK
    else:
        return WHITE


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)
        self.field[0] = [
            Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
            King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
        ]
        self.field[1] = [
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
        ]
        self.field[6] = [
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
        ]
        self.field[7] = [
            Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
            King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
        ]

    def get_piece(self, row, col):
        return self.field[row][col]

    def move_piece(self, row, col, row1, col1):
        piece = self.field[row][col]
        piece1 = self.field[row1][col1]
        if isinstance(piece1, King):
            if piece1.get_color() != self.color:
                return False
        if isinstance(piece, King) and isinstance(piece1, Rook):
            if piece.get_color() == piece1.get_color():
                if col1 == 0:
                    if self.castling0():
                        self.color = opponent(self.color)
                        return True
                elif col1 == 7:
                    if self.castling7():
                        self.color = opponent(self.color)
                        return True
        if row == row1 and col == col1:
            return False
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if piece1 is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif piece1.get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        if isinstance(piece, King):
            field_copy = deepcopy(self.field)
            self.field[row][col] = None
            self.field[row1][col1] = piece
            self.color = opponent(self.color)
            if piece.is_under_attack(self, row1, col1):
                self.field = field_copy
                self.color = opponent(self.color)
                return False
            return True
        else:
            king, r, c = self.find_king()
            field_copy = deepcopy(self.field)
            self.field[row][col] = None
            self.field[row1][col1] = piece
            self.color = opponent(self.color)
            if king.is_under_attack(self, r, c):
                self.field = field_copy
                self.color = opponent(self.color)
                return False
            return True

    def find_king(self):
        for r in range(8):
            for c in range(8):
                if not (self.field[r][c] is None):
                    if isinstance(self.field[r][c], King) and self.field[r][c].get_color() == self.color:
                        return self.field[r][c], r, c

    def castling0(self):
        row = 0 if self.color == WHITE else 7
        if isinstance(self.field[row][4], King) and isinstance(self.field[row][0], Rook):
            if not self.field[row][4].castling_passed and not self.field[row][0].castling_passed:
                if self.field[row][1] is None and self.field[row][2] is None and self.field[row][3] is None:
                    if not (self.field[row][4].is_under_attack(self, row, 2)):
                        self.field[row][4] = None
                        self.field[row][0] = None
                        self.field[row][2] = King(self.color)
                        self.field[row][3] = Rook(self.color)
                        self.field[row][2].castling_passed = True
                        self.field[row][3].castling_passed = True
                        return True
        return False

    def castling7(self):
        row = 0 if self.color == WHITE else 7
        if isinstance(self.field[row][4], King) and isinstance(self.field[row][7], Rook):
            if not self.field[row][4].castling_passed and not self.field[row][7].castling_passed:
                if self.field[row][5] is None and self.field[row][6] is None:
                    if not (self.field[row][4].is_under_attack(self, row, 6)):
                        self.field[row][4] = None
                        self.field[row][7] = None
                        self.field[row][5] = Rook(self.color)
                        self.field[row][6] = King(self.color)
                        self.field[row][5].castling_passed = True
                        self.field[row][6].castling_passed = True
                        return True
        return False


class Rook:

    def __init__(self, color):
        self.color = color
        self.castling_passed = False

    def get_color(self):
        return self.color

    def can_move(self, board, row, col, row1, col1):
        if row != row1 and col != col1:
            return False

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1, step):
            # Если на пути по горизонтали есть фигура
            if not (board.get_piece(r, col) is None):
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            # Если на пути по вертикали есть фигура
            if not (board.get_piece(row, c) is None):
                return False

        self.castling_passed = True
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Pawn:

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def can_move(self, board, row, col, row1, col1):
        if col != col1:
            return False

        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        if row + direction == row1:
            return True

        if (row == start_row
                and row + 2 * direction == row1
                and board.field[row + direction][col] is None):
            return True

        return False

    def can_attack(self, board, row, col, row1, col1):
        direction = 1 if (self.color == WHITE) else -1
        return (row + direction == row1
                and (col + 1 == col1 or col - 1 == col1))


class Knight:

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def can_move(self, board, row, col, row1, col1):
        if (abs(row1 - row) == 2 and abs(col1 - col) == 1) or \
                (abs(row1 - row) == 1 and abs(col1 - col) == 2):
            if not (board.get_piece(row1, col1) is None):
                if board.get_piece(row1, col1).get_color() == self.color:
                    return False
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class King:

    def __init__(self, color):
        self.color = color
        self.castling_passed = False

    def get_color(self):
        return self.color

    def can_move(self, board, row, col, row1, col1):
        if row == row1 and col == col1:
            return False
        if row1 != row and col1 != col:
            if (abs(row - row1) != 1) or (abs(col1 - col) != 1):
                return False
        elif row == row1 and col != col1:
            if max(col1, col) - min(col1, col) != 1:
                return False
        elif col == col1 and row != row1:
            if max(row1, row) - min(row1, row) != 1:
                return False

        if not (board.get_piece(row1, col1) is None):
            if board.get_piece(row1, col1).get_color() == self.color:
                return False
            self.castling_passed = True
        return True

    def is_under_attack(self, board, row1, col1):
        for r in range(8):
            for c in range(8):
                if not (board.get_piece(r, c) is None):
                    if board.get_piece(r, c).get_color() != self.color:
                        if board.get_piece(r, c).can_attack(board, r, c, row1, col1):
                            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Queen:

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def can_move(self, board, row, col, row1, col1):
        if row == row1 and col == col1:
            return False

        step_r = 1 if (row1 >= row) else -1
        step_c = 1 if (col1 >= col) else -1

        if abs(row - row1) == abs(col - col1):
            r = row
            c = col

            while max(row1, r) > min(row1, r):  # and abs(c) < col1
                r += step_r
                c += step_c
                if not (board.get_piece(r, c) is None):
                    if board.get_piece(r, c).get_color() == self.color:
                        return False
                    elif max(row1, r) > min(row1, r):
                        return False
            return True
        elif row1 == row and col1 != col:
            for c in range(col + step_c, col1 + step_c, step_c):
                if not (board.get_piece(row, c) is None):
                    if board.get_piece(row, c).get_color() == self.color:
                        return False
                    elif col < c < col1 or col > c > col1:
                        return False
            return True
        elif row1 != row and col1 == col:
            for r in range(row + step_r, row1 + step_r, step_r):
                if not (board.get_piece(r, col) is None):
                    if board.get_piece(r, col).get_color() == self.color:
                        return False
                    elif row < r < row1 or row > r > row1:
                        return False

            return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Bishop:

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def can_move(self, board, row, col, row1, col1):
        if (row == row1 and col == col1) or (abs(row - row1) != abs(col - col1)):
            return False

        step_r = 1 if (row1 >= row) else -1
        step_c = 1 if (col1 >= col) else -1

        r = row
        c = col

        while max(row1, r) > min(row1, r):  # and abs(c) < col1
            r += step_r
            c += step_c
            if not (board.get_piece(r, c) is None):
                if board.get_piece(r, c).get_color() == self.color:
                    return False
                elif max(row1, r) > min(row1, r):
                    return False
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)
