import os


class Board:
    def __init__(self, *args):
        self.figs = list(args)
        self.figs_cor = self.cor_update()
        self.field = self.def_of_field()
        self.alph = '    A B C D E F G H   '
        self.numbers = '876543210HGFEDCBA'
        self.turn_count = 0
        self.turn_now = 'Black'
        self.hod = {}
        self.gamemode = 0

    def def_of_field(self):
        self.field = [['\u25A3' for _ in range(8)] for _ in range(8)]
        for i, l in enumerate(self.figs):
            if self.figs[i].coord == '':
                continue
            self.field[int(l.coord[0])][int(l.coord[1])] = l.name
        return self.field

    def cor_update(self):
        self.figs_cor = []
        for i in range(len(self.figs)):
            self.figs_cor.append(self.figs[i].coord)
        return self.figs_cor

    def definer(self, coord):
        for i in range(len(self.figs_cor)):
            if self.figs_cor[i] == coord:
                if self.turn_now != self.figs[i].color:
                    return f'Сейчас ход {self.turn_now}'
                if self.figs[i].choice() == 'нет хода':
                    return 'нет возможных ходов'
                else:
                    return self.figs[i].choice()
        return 'нет возможных ходов'

    def move(self, coord):
        if len(coord) != 2 or coord[0] not in (self.numbers + self.alph.lower()) or coord[1] not in self.numbers:
            print('Неверный формат координаты')
            self.move(
                input(f'Введите координату фигуры, сейчас ход {self.turn_now}: '))
        else:
            if coord[0].upper() in self.alph:
                for i in range(9, len(self.numbers)):
                    if coord[0].upper() == self.numbers[i]:
                        coord = self.numbers[i - 8] + coord[1]
            coord = coord[0] + str(int(coord[1]) - 1)
            movelist = self.definer(coord)
            if movelist != 'нет возможных ходов' and movelist != f'Сейчас ход {self.turn_now}':
                movelist1 = []
                movelist1.extend(movelist)
                for i in range(len(movelist1)):
                    if movelist1[i][0] not in self.alph:
                        for j in range(1, 9):
                            if movelist1[i][0] == self.numbers[j]:
                                movelist1[i] = self.numbers[j + 8] + \
                                    str(int(movelist1[i][1]) + 1)
                for i in range(len(self.figs)):
                    if self.figs[i].coord == coord:
                        q__q = i
                ttt = self.figs[q__q].name
                self.figs[q__q].name = '\033[44m' + \
                    self.figs[q__q].name + '\033[0m'
                self.coloring(coordl=movelist)
                self.figs[q__q].name = ttt
                self.coord_move(coord, movelist)
            else:
                print(movelist)
                self.move(
                    input(f'Введите координату фигуры, сейчас ход {self.turn_now}: '))

    def coord_move(self, coord, movelist):
        coordmove = input('Введите координату хода из возможных: ')
        if coordmove != '' and len(coordmove) == 2 and coordmove[0].upper() in self.alph and coordmove[
                1] in self.numbers[:8]:

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
                gx = []
                gy = []
                if self.gamemode == '3':
                    q = int(coordmove[0]) - int(coord[0])
                    w = int(coordmove[1]) - int(coord[1])
                    if q > 0:
                        for i in range(1, q):
                            gx.append(i)
                    else:
                        for i in range(q+1, 0):
                            gx.append(i)
                    if w > 0:
                        for i in range(1, w):
                            gy.append(i)
                    else:
                        for i in range(w+1, 0):
                            gy.append(i)
                    for i in range(min(len(gx), len(gy))):
                        gx[i] = int(coord[0]) + gx[i]
                        gy[i] = int(coord[1]) + gy[i]
                for i in range(len(self.figs_cor)):
                    if self.figs_cor[i] == coord:
                        self.figs[i].coord = coordmove
                        a = i
                for i in range(len(self.figs_cor)):
                    if i != a:
                        if self.figs_cor[i] == coordmove:
                            self.figs[i].coord = ''
                            l = i
                        for j in range(min(len(gx), len(gy))):
                            if self.figs_cor[i] == str(gx[j]) + str(gy[j]):
                                self.figs[i].coord = ''
                                l = i
                if l != 0:
                    if self.figs[a].name == '\u25B3' or self.figs[a].name == '\u25B2':
                        self.figs[l].coord = coord
                    else:
                        self.figs.pop(l)
                self.hod[coord] = coordmove
            else:
                print('Неверная координата')
                self.coord_move(coord, movelist)
        else:
            print('Неверный формат координаты')
            self.coord_move(coord, movelist)

    def coloring(self, coordl, mode=0, take_others=''):
        os.system('cls')
        self.field = [['\u25A3' for _ in range(8)] for _ in range(8)]
        for i, l in enumerate(self.figs):
            if self.figs[i].coord == '':
                continue
            self.field[int(l.coord[0])][int(l.coord[1])] = l.name
        if mode == 0:
            for i in range(len(coordl)):
                self.field[int(coordl[i][0])][int(coordl[i][1])] = '\033[35m' + '\033[45m' + \
                    self.field[int(coordl[i][0])][int(
                        coordl[i][1])] + '\033[0m'
        else:
            for i in range(len(coordl)):
                if self.field[int(coordl[i][0])][int(coordl[i][1])] in take_others:
                    self.field[int(coordl[i][0])][int(coordl[i][1])] = '\033[35m' + '\033[45m' + \
                        self.field[int(coordl[i][0])][int(
                            coordl[i][1])] + '\033[0m'
        field_for_view = list(map(list, zip(*self.field)))
        for il in range(9, -1, -1):
            if il == 0 or il == 9:
                print()
                print(self.alph)
                print()
            else:
                print(self.numbers[-il + 8], ' ',
                      ' '.join(field_for_view[il - 1]), ' ', self.numbers[-il + 8])

    def start_game(self):
        if self.gamemode == '3':
            figs = [Checker('00'), Checker('20'), Checker('40'), Checker('60'), Checker('11'), Checker('31'),
                    Checker('51'), Checker('71'), Checker('02'), Checker(
                        '22'), Checker('42'), Checker('62'),
                    Checker('17', 'Black'), Checker('37', 'Black'), Checker(
                        '57', 'Black'), Checker('77', 'Black'),
                    Checker('06', 'Black'), Checker('26', 'Black'), Checker(
                        '46', 'Black'), Checker('66', 'Black'),
                    Checker('15', 'Black'), Checker('35', 'Black'),
                    Checker('55', 'Black'),
                    Checker('75', 'Black')]
            for i in figs:
                self.figs.append(i)
        else:
            y = 0
            if self.gamemode == '2':
                S = Silver('01')
                G = Gold('71')
                M1 = Mover('11')
                M2 = Mover('61')
                s = Silver('06', 'Black')
                g = Gold('76', 'Black')
                m1 = Mover('16', 'Black')
                m2 = Mover('66', 'Black')
                y = 1

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
            P1 = Pawn('0' + str(1 + y))
            P2 = Pawn('1' + str(1 + y))
            P3 = Pawn('21')
            P4 = Pawn('31')
            P5 = Pawn('41')
            P6 = Pawn('51')
            P7 = Pawn('6' + str(1 + y))
            P8 = Pawn('7' + str(1 + y))
            p1 = Pawn('0' + str(6 - y), 'Black')
            p2 = Pawn('1' + str(6 - y), 'Black')
            p3 = Pawn('26', 'Black')
            p4 = Pawn('36', 'Black')
            p5 = Pawn('46', 'Black')
            p6 = Pawn('56', 'Black')
            p7 = Pawn('6' + str(6 - y), 'Black')
            p8 = Pawn('7' + str(6 - y), 'Black')
            figs = [P1, P2, P3, P4, P5, P6, P7, P8, B1, B2, R1, R2, N1, N2, Q, K, p1, p2, p3, p4, p5, p6, p7, p8, b1,
                    b2, r1,
                    r2, n1, n2, q, k]
            try:
                figs.extend([S, G, M1, M2, s, g, m1, m2])
            except NameError:
                pass
            for i in figs:
                self.figs.append(i)

    def game(self):
        self.def_of_field()
        self.cor_update()
        q = 0
        w = 0
        b = 0
        le = list()
        for i in range(len(self.figs)):
            self.figs[i].update(self.field)
            if self.figs[i].name == '\u2654' or self.figs[i].name == '\u265A':
                q += 1
                le.append(self.figs[i].color)
            if self.figs[i].color == 'White':
                w += 1
            else:
                b += 1
        if (q != 2 and self.gamemode in '12') or (self.gamemode == '3' and (b == 0 or w == 0)):
            print(f'{le[0]} цвет победил')
            print(f'Игра заняла {self.turn_count} ходов')
        else:
            self.color_manager()
            hg = []
            for a in range(len(self.figs)):
                if self.turn_now != self.figs[a].color:
                    m = a
                    if self.figs[a].choice() != 'нет хода':
                        if self.gamemode == '3':
                            for tr in self.figs[a].choice():
                                gx = []
                                gy = []
                                q = int(tr[0]) - int(self.figs[a].coord[0])
                                w = int(tr[1]) - int(self.figs[a].coord[1])
                                if q > 0:
                                    for zxc in range(1, q):
                                        gx.append(zxc)
                                else:
                                    for zxc in range(q+1, 0):
                                        gx.append(zxc)
                                if w > 0:
                                    for zxc in range(1, w):
                                        gy.append(zxc)
                                else:
                                    for zxc in range(w+1, 0):
                                        gy.append(i)
                                for zxc in range(min(len(gx), len(gy))):
                                    gx[zxc] = int(self.figs[a].coord[0]) + gx[zxc]
                                    gy[zxc] = int(self.figs[a].coord[1]) + gy[zxc]
                                for zxc in range(len(self.figs_cor)):
                                    if self.figs_cor[zxc] == self.figs[a].coord:
                                        self.figs[zxc].coord = tr
                                        a = zxc
                                for zxc in range(len(self.figs_cor)):
                                    for j in range(min(len(gx), len(gy))):
                                        if self.figs_cor[zxc] == str(gx[j]) + str(gy[j]):
                                            hg.append(str(gx[j]) + str(gy[j]))
                        else:              
                            hg.extend(self.figs[a].choice()) 
            self.coloring(hg, 1, self.figs[m].take_others())
            self.move(
                input(f'Введите координату фигуры, сейчас ход {self.turn_now}: '))
            os.system('cls')
            self.game()

    def color_manager(self):
        self.turn_count += 1
        if self.turn_now == 'White':
            self.turn_now = 'Black'
        else:
            self.turn_now = 'White'


class Figure(Board):
    def __init__(self, coord, color='White'):
        super().__init__()
        self.coord = coord
        self.color = color
        self.name = 'F'
        self.w = '\u2654\u2655\u2656\u2657\u2658\u2659\u25C7\u2B21\u25B3\u26c0\u26c1'
        self.b = '\u265A\u265B\u265C\u265D\u265E\u265F\u25C8\u2B22\u25B2\u26c2\u26c3'

    def title(self, a):
        if self.color == 'White':
            return self.w[a]
        else:
            return self.b[a]

    def update(self, field):
        self.field = field

    def take_others(self):
        if self.color == 'White':
            return self.b
        return self.w

    @staticmethod
    def no_place(additional_list):
        co = 0
        for ir in range(len(additional_list)):
            if additional_list[ir] != 'нет хода':
                co += 1
        ir = 0
        while True:
            if ir >= len(additional_list):
                break
            if additional_list[ir] in ['н', 'е', 'т', ' ', 'х', 'о', 'д', 'а']:
                additional_list.pop(ir)
            else:
                ir += 1
                
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
        self.name = self.title(5)
        if self.color == "White":
            self.o1 = '7'
        else:
            self.o1 = '0'

    def choices_pawn(self):
        additional_list = []
        if self.color == 'White':
            c = '1'
            g = 1
        else:
            c = '6'
            g = -1
        try:
            if self.field[int(self.coord[0])][int(self.coord[1]) + g] == '\u25A3':
                additional_list.append(
                    self.coord[0] + str(int(self.coord[1]) + g))
                try:
                    if self.coord[1] == c and self.field[int(self.coord[0])][int(self.coord[1]) + g * 2] == '\u25A3':
                        additional_list.append(
                            self.coord[0] + str(int(self.coord[1]) + g * 2))
                except IndexError:
                    additional_list.append('нет хода')
        except IndexError:
            additional_list.append('нет хода')
        try:
            if '-' in (str(int(self.coord[0]) + g) + str(int(self.coord[1]) + g)):
                raise IndexError
            if self.field[int(self.coord[0]) + g][int(self.coord[1]) + g] in self.take_others():
                additional_list.append(
                    str(int(self.coord[0]) + g) + str(int(self.coord[1]) + g))
        except IndexError:
            additional_list.append('нет хода')
        try:
            if '-' in (str(int(self.coord[0]) - g) + str(int(self.coord[1]) + g)):
                raise IndexError
            if self.field[int(self.coord[0]) - g][int(self.coord[1]) + g] in self.take_others():
                additional_list.append(
                    str(int(self.coord[0]) - g) + str(int(self.coord[1]) + g))
        except IndexError:
            additional_list.append('нет хода')
        return self.no_place(additional_list)

    def choice(self):
        return self.choices_pawn()


class Rook(Figure):
    def __init__(self, coord, color='White'):
        super().__init__(coord, color)
        self.name = self.title(2)

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
                                i]][int(self.coord[1]) + j * gy[i]] == '\u25A3':
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
        self.name = self.title(3)

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
                                i]][int(self.coord[1]) + j * gy[i]] == '\u25A3':
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
        self.name = self.title(4)

    def choices_knight(self):
        additional_list = []
        gx = [1, 2, 2, 1, -1, -2, -2, -1]
        gy = [2, 1, -1, -2, -2, -1, 1, 2]
        for i in range(len(gx)):
            try:
                if '-' not in (str(int(self.coord[0]) + gx[i]) + str(int(self.coord[1]) + gy[i])) and \
                        self.field[int(self.coord[0]) + gx[i]][
                            int(self.coord[1]) + gy[i]] in self.take_others() + '\u25A3':
                    additional_list.append(
                        str(int(self.coord[0]) + gx[i]) + str(int(self.coord[1]) + gy[i]))
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
        self.name = self.title(1)

    def choices_queen(self):
        additional_list = []
        additional_list.extend(self.choices_bishop())
        additional_list.extend(self.choices_rook())
        ir = 0
        while True:
            if ir >= len(additional_list):
                break
            if additional_list[ir] in ['н', 'е', 'т', ' ', 'х', 'о', 'д', 'а']:
                additional_list.pop(ir)
            else:
                ir += 1
        return additional_list

    def choice(self):
        return self.choices_queen()


class King(Figure):
    def __init__(self, coord, color='White'):
        super().__init__(coord, color)
        self.name = self.title(0)

    def choices_king(self):
        additional_list = []
        gx = [1, 1, 1, 0, 0, -1, -1, -1]
        gy = [1, -1, 0, 1, -1, 1, -1, 0]
        for i in range(len(gx)):
            try:
                if '-' not in (str(int(self.coord[0]) + gx[i]) + str(int(self.coord[1]) + gy[i])) and (
                        self.field[int(self.coord[0]) + gx[i]][int(self.coord[1]) + gy[i]] in (
                        self.take_others() + '\u25A3')):
                    additional_list.append(
                        str(int(self.coord[0]) + gx[i]) + str(int(self.coord[1]) + gy[i]))
            except IndexError:
                additional_list.append('нет хода')
        if self.no_place(additional_list) is not None:
            return self.no_place(additional_list)
        return self.no_place(additional_list)

    def choice(self):
        return self.choices_king()


class Gold(Figure):
    def __init__(self, coord, color="White"):
        super().__init__(coord, color)
        self.name = self.title(7)

    def choices_gold(self):
        additional_list = []
        if self.color == 'White':
            gx = [1, 1, 0, 0, -1, -1]
            gy = [1, 0, 1, -1, 1, 0]
        else:
            gx = [1, 1, 0, 0, -1, -1]
            gy = [-1, 0, 1, -1, -1, 0]

        for i in range(len(gx)):
            try:
                if '-' not in (str(int(self.coord[0]) + gx[i]) + str(int(self.coord[1]) + gy[i])) and (
                        self.field[int(self.coord[0]) + gx[i]][int(self.coord[1]) + gy[i]] in (
                        self.take_others() + '\u25A3')):
                    additional_list.append(
                        str(int(self.coord[0]) + gx[i]) + str(int(self.coord[1]) + gy[i]))
            except IndexError:
                additional_list.append('нет хода')
        if self.no_place(additional_list) is not None:
            return self.no_place(additional_list)
        return self.no_place(additional_list)

    def choice(self):
        return self.choices_gold()


class Silver(Gold):
    def __init__(self, coord, color="White"):
        super().__init__(coord, color)
        self.name = self.title(6)
        self.flag = True
        if self.color == "White":
            self.o1 = '5'
        else:
            self.o1 = '3'

    def choices_silver(self):
        additional_list = []
        if self.color == 'White':
            gx = [1, 0, -1, -1, 1]
            gy = [1, 1, 1, -1, -1]
        else:
            gx = [1, 0, -1, -1, 1]
            gy = [1, -1, 1, -1, -1]

        for i in range(len(gx)):
            try:
                if '-' not in (str(int(self.coord[0]) + gx[i]) + str(int(self.coord[1]) + gy[i])) and (
                        self.field[int(self.coord[0]) + gx[i]][int(self.coord[1]) + gy[i]] in (
                        self.take_others() + '\u25A3')):
                    additional_list.append(
                        str(int(self.coord[0]) + gx[i]) + str(int(self.coord[1]) + gy[i]))
            except IndexError:
                additional_list.append('нет хода')
        if self.no_place(additional_list) is not None:
            return self.no_place(additional_list)
        return self.no_place(additional_list)

    def promotion(self):
        if self.coord[1] == self.o1 and self.flag:
            if input('Улучшить? (да/нет) ') == 'да':
                self.flag = False
                self.name = self.title(7)

    def choice(self):
        self.promotion()
        if not self.flag:
            return self.choices_gold()
        return self.choices_silver()


class Mover(Figure):
    def __init__(self, coord, color="White"):
        super().__init__(coord, color)
        self.name = self.title(8)
        self.d = True

    def choices_mover(self):
        additional_list = []
        gx = [1, 1, 1, 0, 0, -1, -1, -1]
        gy = [1, -1, 0, 1, -1, 1, -1, 0]
        for i in range(len(gx)):
            try:
                if '-' not in (str(int(self.coord[0]) + gx[i]) + str(int(self.coord[1]) + gy[i])) and (
                        self.field[int(self.coord[0]) + gx[i]][int(self.coord[1]) + gy[i]] in (
                        self.w + self.b)):
                    additional_list.append(
                        str(int(self.coord[0]) + gx[i]) + str(int(self.coord[1]) + gy[i]))
            except IndexError:
                additional_list.append('нет хода')
        if self.no_place(additional_list) is not None:
            return self.no_place(additional_list)
        return self.no_place(additional_list)

    def choice(self):
        return self.choices_mover()


class Checker(Pawn):
    def __init__(self, coord, color='White'):
        super().__init__(coord, color)
        self.name = self.title(9)
        self.flag1 = False

    def choices_checker(self):
        additional_list = []
        if self.color == 'White':
            g = 1
        else:
            g = -1
        try:
            if '-' in (str(int(self.coord[0]) + g) + str(int(self.coord[1]) + g)):
                raise IndexError
            if self.field[int(self.coord[0]) + g][int(self.coord[1]) + g] == '\u25A3':
                additional_list.append(
                    str(int(self.coord[0]) + g) + str(int(self.coord[1]) + g))
            elif self.field[int(self.coord[0]) + g][int(self.coord[1]) + g] in self.take_others() and \
                    self.field[int(self.coord[0]) + 2 * g][int(self.coord[1]) + 2 * g] == '\u25A3':
                self.flag1 = True
                additional_list.append(
                    str(int(self.coord[0]) + 2 * g) + str(int(self.coord[1]) + 2 * g))

        except IndexError:
            additional_list.append('нет хода')
        try:
            if '-' in (str(int(self.coord[0]) - g) + str(int(self.coord[1]) + g)):
                raise IndexError
            if self.field[int(self.coord[0]) - g][int(self.coord[1]) + g] == '\u25A3':
                additional_list.append(
                    str(int(self.coord[0]) - g) + str(int(self.coord[1]) + g))
            elif self.field[int(self.coord[0]) - g][int(self.coord[1]) + g] in self.take_others() and \
                    self.field[int(self.coord[0]) - 2 * g][int(self.coord[1]) + 2 * g] == '\u25A3':
                self.flag1 = True
                additional_list.append(
                    str(int(self.coord[0]) - 2 * g) + str(int(self.coord[1]) + 2 * g))
        except IndexError:
            additional_list.append('нет хода')
        try:
            if self.field[int(self.coord[0]) - g][int(self.coord[1]) - g] in self.take_others() and \
                    self.field[int(self.coord[0]) - 2 * g][int(self.coord[1]) - 2 * g] == '\u25A3':
                self.flag1 = True
                additional_list.append(
                    str(int(self.coord[0]) - 2 * g) + str(int(self.coord[1]) - 2 * g))
        except IndexError:
            additional_list.append('нет хода')
        try:
            if self.field[int(self.coord[0]) + g][int(self.coord[1]) - g] in self.take_others() and \
                    self.field[int(self.coord[0]) + 2 * g][int(self.coord[1]) - 2 * g] == '\u25A3':
                self.flag1 = True
                additional_list.append(
                    str(int(self.coord[0]) + 2 * g) + str(int(self.coord[1]) - 2 * g))
        except IndexError:
            additional_list.append('нет хода')
        return self.no_place(additional_list)

    def choice(self):
        return self.choices_checker()


class Moves:
    def __init__(self):
        self.coords = []

    def update(self, dicti):
        for i in dicti:
            self.coords.append(
                {chr(int(i[0]) + 65) + str(int(i[1]) + 1): chr(int(dicti[i][0]) + 65) + str(int(dicti[i][1]) + 1)})

    def __str__(self):
        a = 'Сделанные ходы: \n'
        for i in range(len(self.coords)):
            a += f'Ход номер {i + 1}: {self.coords[i]} \n'
        return a


os.system('cls')
board = Board()
while True:
    board.gamemode = input(
        'Выберите тип игры: шахматы, шахматы с доп фигурами, шашки (1, 2, 3): ')
    if board.gamemode in '123':
        break
os.system('cls')
board.start_game()
board.game()
moves = Moves()
moves.update(board.hod)
print(moves)
input()
