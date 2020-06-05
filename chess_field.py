"""
Функция field_calc принимает на вход строку типа "QD1 RA5 NF8 ... "
где перый символ - код фигуры (Q - Queen, R - Rook) два следующих - её позиция.
Возвращает двумерный список:

0 0 0 1 0 0 0 0
0 0 0 1 0 1 0 0
0 0 1 1 0 0 1 0
0 0 0 1 N 0 0 1
1 0 1 1 0 0 1 0
1 1 1 R 1 1 1 1
0 0 1 1 1 0 0 0
1 1 1 Q 1 1 1 1

где 1 - клетка поля под атакой, 0 - безопасная клетка, Q, R, N - код фигуры
"""


class Desk:
    pos_y = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7,
             'H': 8}

    def __init__(self):
        self.pieces = []
        self.field = [['0'] * 8 for _ in range(8)]
        self.pieces_position = {}

    def set_pieces(self, pieces: str):
        self.pieces = pieces.split(' ')
        piece = None
        for p in self.pieces:
            x = int(p[2]) - 1
            y = self.pos_y[p[1]] - 1
            if p[0] == 'Q':
                piece = Queen()
            elif p[0] == 'N':
                piece = Knight()
            elif p[0] == 'R':
                piece = Rook()
            elif p[0] == 'B':
                piece = Bishop()
            elif p[0] == 'p':
                piece = Pawn()
            elif p[0] == 'K':
                piece = King()
            self.field[x][y] = p[0]
            self.pieces_position[piece] = p[1:]

    def make_movement(self):
        for key, value in self.pieces_position.items():
            key.make_projection(self)


class Piece:

    def __init__(self):
        self.movement = []
        self.pos = Desk.pos_y

    def make_projection(self, desk: Desk):

        mov = desk.pieces_position.get(self)

        y_off = self.pos[mov[0]]
        x_off = int(mov[1])
        for ray in self.movement:
            for x, y in ray:
                pos_x = x + x_off - 1
                pos_y = y + y_off - 1
                if 0 <= pos_x <= 7 and 0 <= pos_y <= 7:
                    cell = desk.field[pos_x][pos_y]
                    if cell != '0' and cell != '1':
                        break
                    desk.field[pos_x][pos_y] = '1'


class Knight(Piece):

    def __init__(self):
        super().__init__()
        m_list = ((2, -1), (1, -2), (1, 2), (2, 1), (-1, -2), (-2, -1),
                  (-1, 2), (-2, 1))
        for i in m_list:
            self.movement.append([i])

    def __str__(self):
        return 'N'  # u'\u2658'


class Pawn(Piece):

    def __init__(self):
        super().__init__()
        self.movement = [[(1, 1)], [(1, -1)]]

    def __str__(self):
        return 'p'  # u'\u2659'


class King(Pawn):

    def __init__(self):
        super().__init__()
        m_list = ((0, 1), (1, 0), (-1, 0), (0, -1), (-1, 1), (-1, -1))
        for i in m_list:
            self.movement.append([i])

    def __str__(self):
        return 'K'  # u'\u2654'


class Rook(Piece):

    def __init__(self):
        super().__init__()
        self.movement.append([(0, i) for i in range(1, 8)])
        self.movement.append([(i, 0) for i in range(1, 8)])
        self.movement.append([(i * -1, 0) for i in range(1, 8)])
        self.movement.append([(0, i * -1) for i in range(1, 8)])

    def __str__(self):
        return 'R'  # u'\u2656'


class Bishop(Piece):
    def __init__(self):
        super().__init__()
        self.movement.append([(i, i) for i in range(1, 8)])
        self.movement.append([(i, i * -1) for i in range(1, 8)])
        self.movement.append([(i * -1, i) for i in range(1, 8)])
        self.movement.append([(i * -1, i * -1) for i in range(1, 8)])

    def __str__(self):
        return 'B'  # u'\u2657'


class Queen(Rook, Bishop):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'Q'  # u'\u2655'


def field_calc(inp: str) -> tuple:
    f = Desk()
    f.set_pieces(inp)
    f.make_movement()
    cell = 0
    for i in f.field[::-1]:
        cell += i.count('1')
    return f.field[::-1], cell


if __name__ == '__main__':
    p_set = 'pA2 pB2 pC2 pD2 pE2 pF2 pG2 pH2 KE1 QD1 BC1 NB1 RA1 RH1 NG1 BF1'
    field, attacked_cell = field_calc(p_set)
    for line in field:
        print(' '.join(line))
    print(f'Число клеток под ударом {attacked_cell}')
