class Board:
    def __init__(self, *args):
        self.figs = list(args)
        self.figs_cor = self.cor_update()
        self.field = self.def_of_field()
        self.alph = '    A B C D E F G H   '
        self.numbers = '876543210HGFEDCBA'

    def def_of_field(self):
        self.field = [['*' for _ in range(8)] for _ in range(8)]
        for il in self.figs:
            self.field[int(il.coord[0])][int(il.coord[1])] = il.name
        return self.field

    def view_of_field(self):
        self.def_of_field()
        field_for_view = list(map(list, zip(*self.field)))
        for il in range(9, -1, -1):
            if il == 0 or il == 9:
                print()
                print(self.alph)
                print()
            else:
                print(self.numbers[-il + 8], ' ', ' '.join(field_for_view[il - 1]), ' ', self.numbers[-il + 8])

    def cor_update(self):
        self.figs_cor = []
        for i in range(len(self.figs)):
            self.figs_cor.append(self.figs[i].coord)
        return self.figs_cor

    def definer(self, coord):
        for i in range(len(self.figs_cor)):
            if self.figs_cor[i] == coord:
                if self.figs[i].choice() == 'нет хода':
                    return 'нет возможных ходов'
                else:
                    return self.figs[i].choice()
        return 'нет возможных ходов'

    def move(self, coord):
        if coord[0].upper() in self.alph:
            for i in range(9, len(self.numbers)):
                if coord[0].upper() == self.numbers[i]:
                    coord = self.numbers[i - 8] + coord[1]
        coord = coord[0] + str(int(coord[1]) - 1)
        movelist = self.definer(coord)
        # if movelist == 'нет хода':
        #     choice()
        if movelist != 'нет возможных ходов':
            movelist1 = []
            movelist1.extend(movelist)
            for i in range(len(movelist1)):
                if movelist1[i][0] not in self.alph:
                    for j in range(1, 9):
                        if movelist1[i][0] == self.numbers[j]:
                            movelist1[i] = self.numbers[j + 8] + str(int(movelist1[i][1]) + 1)
            print(*movelist1)
            print(self.field[int(coord[0])][int(coord[1])])
            coordmove = input('Введите координату хода из возможных: ')
            if coordmove != '':
                if coordmove[0].upper() in self.alph:
                    for i in range(9, len(self.numbers)):
                        if coordmove[0].upper() == self.numbers[i]:
                            coordmove = self.numbers[i - 8] + coordmove[1]
            coordmove = coordmove[0] + str(int(coordmove[1]) - 1)
            flag = False
            for j in movelist:
                if j == coordmove:
                    flag = True
            if flag and coordmove != '':
                l = 0
                for i in range(len(self.figs_cor)):
                    if self.figs_cor[i] == coordmove:
                        self.figs[i].coord = ''
                        l = i
                    if self.figs_cor[i] == coord:
                        self.figs[i].coord = coordmove
                if l != 0:
                    self.figs.pop(l)
            else:
                print('Неверная координата')
                self.move(coord[0] + str(int(coord[1]) + 1))
        else:
            print(movelist)
            self.move(input())

    def game(self):
        self.view_of_field()
        self.cor_update()
        for i in range(len(self.figs)):
            self.figs[i].update(self.field)
        self.move(input())
        self.game()


class Figure(Board):
    def __init__(self, coord, color='White'):
        super().__init__()
        self.coord = coord
        self.color = color
        self.name = 'F'
        self.f = 'PQKNBR'

    def title(self, a):
        if self.color == 'White':
            return a
        else:
            return a.lower()

    def update(self, field):
        self.field = field

    def take_others(self):
        if self.color == 'White':
            return self.f.lower()
        return self.f.upper()

    @staticmethod
    def no_place(additional_list):
        co = 0
        for ir in range(len(additional_list)):
            if additional_list[ir] != 'нет хода':
                co += 1
        if co != len(additional_list) and co != 0:
            ir = 0
            while True:
                if ir >= len(additional_list):
                    break
                if additional_list[ir] == 'нет хода':
                    additional_list.pop(ir)
                else:
                    ir += 1

        elif co == 0:
            return 'нет хода'
        return additional_list


class Pawn(Figure):
    def __init__(self, coord, color='White'):
        super().__init__(coord, color)
        self.name = self.title('P')

    def choices_pawn(self):
        additional_list = []
        if self.color == 'White':
            c = '1'
            g = 1
        else:
            c = '6'
            g = -1
        try:
            if self.field[int(self.coord[0])][int(self.coord[1]) + g] == '*':
                additional_list.append(self.coord[0] + str(int(self.coord[1]) + g))
                try:
                    if self.coord[1] == c and self.field[int(self.coord[0])][int(self.coord[1]) + g * 2] == '*':
                        additional_list.append(self.coord[0] + str(int(self.coord[1]) + g * 2))
                except IndexError:
                    additional_list.append('нет хода')
        except IndexError:
            additional_list.append('нет хода')
        try:
            if '-' in (str(int(self.coord[0]) + g) + str(int(self.coord[1]) + g)):
                raise IndexError
            if self.field[int(self.coord[0]) + g][int(self.coord[1]) + g] in self.take_others():
                additional_list.append(str(int(self.coord[0]) + g) + str(int(self.coord[1]) + g))
        except IndexError:
            additional_list.append('нет хода')
        try:
            if '-' in (str(int(self.coord[0]) - g) + str(int(self.coord[1]) + g)):
                raise IndexError
            if self.field[int(self.coord[0]) - g][int(self.coord[1]) + g] in self.take_others():
                additional_list.append(str(int(self.coord[0]) - g) + str(int(self.coord[1]) + g))
        except IndexError:
            additional_list.append('нет хода')
        return self.no_place(additional_list)

    def choice(self):
        return self.choices_pawn()


class Rook(Figure):
    def __init__(self, coord, color='White'):
        super().__init__(coord, color)
        self.name = self.title('R')

    def choices_rook(self):
        additional_list = []
        gx = [1, 0, -1, -0]
        gy = [0, -1, 0, 1]
        for i in range(len(gx)):
            flag = 0
            for j in range(1, 8):
                try:
                    if '-' not in (
                            str(int(self.coord[0]) + j * gx[i]) + str(int(self.coord[1]) + j * gy[i])) and flag == 0:
                        if self.field[int(self.coord[0]) + j * gx[
                            i]][int(self.coord[1]) + j * gy[i]] == '*':
                            additional_list.append(
                                str(int(self.coord[0]) + j * gx[i]) + str(int(self.coord[1]) + j * gy[i]))
                        elif self.field[int(self.coord[0]) + j * gx[
                            i]][int(self.coord[1]) + j * gy[i]] in self.take_others():
                            additional_list.append(
                                str(int(self.coord[0]) + j * gx[i]) + str(int(self.coord[1]) + j * gy[i]))
                            flag = 1
                        else:
                            break

                    else:
                        break
                except IndexError:
                    additional_list.append('нет хода')
        return self.no_place(additional_list)

    def choice(self):
        return self.choices_rook()


class Bishop(Figure):
    def __init__(self, coord, color='White'):
        super().__init__(coord, color)
        self.name = self.title('B')

    def choices_bishop(self):

        additional_list = []
        gx = [1, 1, -1, -1]
        gy = [1, -1, -1, 1]
        for i in range(len(gx)):
            flag = 0
            for j in range(1, 8):
                try:
                    if '-' not in (
                            str(int(self.coord[0]) + j * gx[i]) + str(int(self.coord[1]) + j * gy[i])) and flag == 0:
                        if self.field[int(self.coord[0]) + j * gx[
                            i]][int(self.coord[1]) + j * gy[i]] == '*':
                            additional_list.append(
                                str(int(self.coord[0]) + j * gx[i]) + str(int(self.coord[1]) + j * gy[i]))
                        elif self.field[int(self.coord[0]) + j * gx[
                            i]][int(self.coord[1]) + j * gy[i]] in self.take_others():
                            additional_list.append(
                                str(int(self.coord[0]) + j * gx[i]) + str(int(self.coord[1]) + j * gy[i]))
                            flag = 1
                        else:
                            break

                    else:
                        break

                except IndexError:
                    additional_list.append('нет хода')
        return self.no_place(additional_list)

    def choice(self):
        return self.choices_bishop()


class Knight(Figure):
    def __init__(self, coord, color='White'):
        super().__init__(coord, color)
        self.name = self.title('N')

    def choices_knight(self):
        additional_list = []
        gx = [1, 2, 2, 1, -1, -2, -2, -1]
        gy = [2, 1, -1, -2, -2, -1, 1, 2]
        for i in range(len(gx)):
            try:
                if '-' not in (str(int(self.coord[0]) + gx[i]) + str(int(self.coord[1]) + gy[i])) and \
                        self.field[int(self.coord[0]) + gx[i]][
                            int(self.coord[1]) + gy[i]] in self.take_others() + '*':
                    additional_list.append(str(int(self.coord[0]) + gx[i]) + str(int(self.coord[1]) + gy[i]))
            except IndexError:
                additional_list.append('нет хода')
        if self.no_place(additional_list) is not None:
            return self.no_place(additional_list)
        return self.no_place(additional_list)

    def choice(self):
        return self.choices_knight()


class Queen(Bishop, Rook):
    def __init__(self, coord, color='White'):
        super().__init__(coord, color)
        self.name = self.title('Q')

    def choices_queen(self):
        additional_list = []
        additional_list.extend(self.choices_bishop())
        additional_list.extend(self.choices_rook())
        return additional_list

    def choice(self):
        return self.choices_queen()


class King(Figure):
    def __init__(self, coord, color='White'):
        super().__init__(coord, color)
        self.name = self.title('K')

    def choices_king(self):
        additional_list = []
        gx = [1, 1, 1, 0, 0, -1, -1, -1]
        gy = [1, -1, 0, 1, -1, 1, -1, 0]
        for i in range(len(gx)):
            try:
                if '-' not in (str(int(self.coord[0]) + gx[i]) + str(int(self.coord[1]) + gy[i])) and (
                        self.field[int(self.coord[0]) + gx[i]][int(self.coord[1]) + gy[i]] in (
                        self.take_others() + '*')):
                    additional_list.append(str(int(self.coord[0]) + gx[i]) + str(int(self.coord[1]) + gy[i]))
            except IndexError:
                additional_list.append('нет хода')
        if self.no_place(additional_list) is not None:
            return self.no_place(additional_list)
        return self.no_place(additional_list)

    def choice(self):
        return self.choices_king()


P1 = Pawn('01')
P2 = Pawn('11')
P3 = Pawn('21')
P4 = Pawn('31')
P5 = Pawn('41')
P6 = Pawn('51')
P7 = Pawn('61')
P8 = Pawn('71')
p1 = Pawn('06', 'Black')
p2 = Pawn('16', 'Black')
p3 = Pawn('26', 'Black')
p4 = Pawn('36', 'Black')
p5 = Pawn('46', 'Black')
p6 = Pawn('56', 'Black')
p7 = Pawn('66', 'Black')
p8 = Pawn('76', 'Black')
B1 = Bishop('20')
B2 = Bishop('50')
R1 = Rook('00')
R2 = Rook('70')
N1 = Knight('10')
N2 = Knight('60')
Q = Queen('30')
K = King('40')
b1 = Bishop('27', 'Black')
b2 = Bishop('57', 'Black')
r1 = Rook('07', 'Black')
r2 = Rook('77', 'Black')
n1 = Knight('17', 'Black')
n2 = Knight('67', 'Black')
q = Queen('37', 'Black')
k = King('47', 'Black')
figs = [P1, P2, P3, P4, P5, P6, P7, P8, B1, B2, R1, R2, N1, N2, Q, K, p1, p2, p3, p4, p5, p6, p7, p8, b1, b2, r1, r2,
        n1, n2, q, k]
board = Board()
for i in figs:
    board.figs.append(i)
board.game()
# print(board.field)
# print(board.figs)
