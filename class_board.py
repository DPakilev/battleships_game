from colorama import Fore, Style


class Board:
    PART_SHIP = '■'
    HITTING_SHIP = 'X'
    SHOT_MISSED = 'T'

    def __init__(self, battlefield):
        self.battlefield = battlefield
        self.ships = []

    def verify_cell(self, coordinate):
        """
        Метод проверяет занятость ячейки. И в случае если она занята, то программа возращает 'Cell is busy'.
        Если свободна, то возращает 'Cell if free'. А если программа ловит ошибку IndexError, то значит,
        что пользоваель ввел неверную координату и возращается 'Invalid coordinate'
        """
        try:
            # Есть ли на этом месте корабль по горизонтали
            for i in range(coordinate[0][1], coordinate[1][1] + 1):
                if self.battlefield[coordinate[0][0]][i] == Board.PART_SHIP:
                    return 'Cell is busy'

            # Есть ли на этом месте корабль по вертикали
            for i in range(coordinate[0][0], coordinate[1][0] + 1):
                if self.battlefield[i][coordinate[0][1]] == Board.PART_SHIP:
                    return 'Cell is busy'

            # Над координатами коробля
            for i in range(coordinate[0][1], coordinate[1][1] + 1):
                if coordinate[0][0] - 1 < 0:
                    break

                elif self.battlefield[coordinate[0][0] - 1][i] == Board.PART_SHIP:
                    return 'Cell is busy'

                else:
                    continue

            # Под координатами коробля
            for i in range(coordinate[0][1], coordinate[1][1] + 1):
                try:
                    if self.battlefield[coordinate[1][0] + 1][i] == Board.PART_SHIP:
                        return 'Cell is busy'
                    else:
                        continue
                except IndexError:
                    break

            # Левее координат коробля
            for i in range(coordinate[0][0], coordinate[1][0] + 1):
                if coordinate[0][1] - 1 < 0:
                    break

                elif self.battlefield[i][coordinate[0][1] - 1] == Board.PART_SHIP:
                    return 'Cell is busy'
                else:
                    continue

            # Правее координат коробля
            for i in range(coordinate[0][0], coordinate[1][0] + 1):
                try:
                    if self.battlefield[i][coordinate[1][1] + 1] == Board.PART_SHIP:
                        return 'Cell is busy'
                    else:
                        continue
                except IndexError:
                    break

        except IndexError:
            return 'Invalid coordinate'
        return 'Cell if free'

    # Установка корабля
    def set_ship(self, ship_coordinate):
        """
        Метод сохраниения корабля в списке-поля и в списке-кораблей.
        Создается новый список, в который будут добавлятсья координаты коробля.
        Проверяется ореинтация коробля. Первый if - корабль расположен по горизонтали.
        Второй - корабль расположен по вериткали.
        """
        self.ships.append([])

        if ship_coordinate[0][0] == ship_coordinate[1][0]:
            part_ship_coordinate = ship_coordinate[0][0]

            for part_coordinate in range(ship_coordinate[0][1], ship_coordinate[1][1] + 1):
                self.battlefield[part_ship_coordinate][part_coordinate] = Board.PART_SHIP

                self.ships[-1].append([part_ship_coordinate, part_coordinate])

        else:
            part_ship_coordinate = ship_coordinate[0][1]

            for part_coordinate in range(ship_coordinate[0][0], ship_coordinate[1][0] + 1):
                self.battlefield[part_coordinate][part_ship_coordinate] = Board.PART_SHIP

                self.ships[-1].append([part_coordinate, part_ship_coordinate])

    def shooting_interface_ship(self, shot_coordinate, battlefield_shot):
        """
            Метод, который в первую очередь отмечает на поле кораблей выстрел игрока. И если игрок попадает
        по кораблю, то возращается результат метода проверки на разрушение корабля ("Alive", "Destroyed", "Victory").
        Если игрок промахнулся, то возращается "Missed".
            Метод принимает координату выстрела и поле выстрелов, для дальнейших вызовов других методов.
        """
        shot_battlefield = self.battlefield[shot_coordinate[0]][shot_coordinate[1]]

        if shot_battlefield == Board.PART_SHIP:

            self.battlefield[shot_coordinate[0]][shot_coordinate[1]] = Board.HITTING_SHIP

            battlefield_shot.shooting_interface_shot(shot_coordinate, Board.PART_SHIP)

            return self.check_ship_destroyed(shot_coordinate, battlefield_shot.get_interface())

        elif shot_battlefield != Board.PART_SHIP and shot_battlefield != Board.HITTING_SHIP:

            self.battlefield[shot_coordinate[0]][shot_coordinate[1]] = Board.SHOT_MISSED

            battlefield_shot.shooting_interface_shot(shot_coordinate, Board.SHOT_MISSED)
            return "Missed"

    def shooting_interface_shot(self, shot_coordinate, status_shot):
        """
        Этот метод отмечает выстрел игрока на поле высрелов.
        Метод принимает координату выстрела и стутус выстрела (Попадание или промах).
        """
        if status_shot == Board.PART_SHIP:
            self.battlefield[shot_coordinate[0]][shot_coordinate[1]] = Board.HITTING_SHIP
        else:
            self.battlefield[shot_coordinate[0]][shot_coordinate[1]] = Board.SHOT_MISSED

    def check_ship_destroyed(self, part_ship_coordinate, interface_shot):
        """
            Метод, который проверяет разрушен корабль или у него ещё остались части. Первым делом,
        по координате выстрела находим полные координты корабля с помощью метода find_ship.

            В переменной check_part_ship генерируються все части коробля. И если остались живые
        части (■), то корабль ещё жив и возращается "Alive". Если таких частей нету, то запускается
        метод разрушения корабля, и возращается его результат.
        """
        ship_coordinate = self.find_ship(part_ship_coordinate)
        check_part_ship = [self.battlefield[part_ship[0]][part_ship[1]] for part_ship in ship_coordinate]

        if check_part_ship.count(Board.PART_SHIP) > 0:
            return "Alive"
        else:
            return self.ship_destroyed(ship_coordinate, interface_shot)

    def find_ship(self, part_ship_coordinate):
        """
        Метод находит полные координаты корабля по его части.
        """
        for ship_coordinate in self.ships:
            if part_ship_coordinate in ship_coordinate:
                return ship_coordinate

    def ship_destroyed(self, ship_coordinate, interface_shot):
        """
            Метод уничтожения корабля. Он отмечает промахи(Т) вокруг разрушенного корабля, и что бы
        не отметить промах на корабле, производиться проверка. После того как всё отмеченно, запускается
        метод удаления корабля и возращается его результат.
            Так же метод отмечает промахи на поле выстрелов.
        """
        for coordinate in ship_coordinate:
            # Под координатой
            try:
                if self.battlefield[coordinate[0]+1][coordinate[1]] != Board.HITTING_SHIP:
                    self.battlefield[coordinate[0]+1][coordinate[1]] = Board.SHOT_MISSED
                    interface_shot[coordinate[0]+1][coordinate[1]] = Board.SHOT_MISSED
            except IndexError:
                pass

            # Над координатой
            if self.battlefield[coordinate[0]-1][coordinate[1]] != Board.HITTING_SHIP and coordinate[0]-1 > -1:
                self.battlefield[coordinate[0]-1][coordinate[1]] = Board.SHOT_MISSED
                interface_shot[coordinate[0]-1][coordinate[1]] = Board.SHOT_MISSED

            # Правее координаты
            try:
                if self.battlefield[coordinate[0]][coordinate[1]+1] != Board.HITTING_SHIP:
                    self.battlefield[coordinate[0]][coordinate[1]+1] = Board.SHOT_MISSED
                    interface_shot[coordinate[0]][coordinate[1]+1] = Board.SHOT_MISSED
            except IndexError:
                pass

            # Левее координаты
            if self.battlefield[coordinate[0]][coordinate[1]-1] != Board.HITTING_SHIP and coordinate[1]-1 > -1:
                self.battlefield[coordinate[0]][coordinate[1]-1] = Board.SHOT_MISSED
                interface_shot[coordinate[0]][coordinate[1]-1] = Board.SHOT_MISSED
        return self.remove_ship(ship_coordinate)

    def remove_ship(self, ship_coordinate):
        """
        Метод удаляет корабль из списка кораблей, и запускает метод проверка победы и возращает его результат.
        """
        self.ships.remove(ship_coordinate)
        return self.victory_check()

    def victory_check(self):
        """
        Метод проверяет, если список кораблей пустой, то игрок победил и возращается "Victory",
        если в списке еще есть корабли, то он возращает "Destroyed".
        """
        if not self.ships:
            return "Victory"
        else:
            return "Destroyed"

    def verify_re_shot(self, shot_coordinate):
        """
        Метод, который проверяе, если игрок производит повторный выстрел, то возращается True,
        если не производил, то False.
        """
        try:
            shot_battlefield = self.battlefield[shot_coordinate[0]][shot_coordinate[1]]
            if any([shot_battlefield == Board.SHOT_MISSED,
                    shot_battlefield == Board.HITTING_SHIP]):
                return True
            else:
                return False
        except IndexError:
            return "Invalid coordinate"

    def get_app_interface_ships_and_shots(self, interface_second):
        """
            Метод, который вывод в консоль два рядом стоящих поля. Вторая задача - вывести цветное поле,
        что бы игроку было легче ореинтироваться в нём.
            Первый список окраски боковых цифр.
            Остальные списки созданы для выведения чисел в шапке поля (Первая строка).
        """
        list_ = ['1', '2', '3', '4', '5', '6']
        app_interface_first = [['1', '2', '3', '4', '5', '6']]
        app_interface_second = [['1', '2', '3', '4', '5', '6']]

        app_interface_first += interface_second
        app_interface_second += self.battlefield

        print(Fore.BLUE)
        for row in range(len(app_interface_first)):

            if row == 0:
                print(Fore.RED, "Вражеское поле                         ", Fore.GREEN, "Твоё поле")
                print(Style.RESET_ALL)
                print(Fore.GREEN, ' ', Fore.BLUE, end='|')
            else:
                print(Fore.GREEN, row, Fore.BLUE, end='|')

            for column in range(len(app_interface_first) - 1):

                if app_interface_first[row][column] in list_:
                    print(Fore.GREEN, app_interface_first[row][column], Fore.BLUE, end='|')

                elif app_interface_first[row][column] == Board.HITTING_SHIP:
                    print(Fore.RED, app_interface_first[row][column], Fore.BLUE, end='|')

                elif app_interface_first[row][column] == Board.SHOT_MISSED:
                    print(Fore.YELLOW, app_interface_first[row][column], Fore.BLUE, end='|')

                elif app_interface_first[row][column] == Board.PART_SHIP:
                    print(Fore.RED, app_interface_first[row][column], Fore.BLUE, end='|')

                else:
                    print(Fore.BLUE, app_interface_first[row][column], Fore.BLUE, end='|')

            print(end='          ')

            if row == 0:
                print(Fore.GREEN, ' ', Fore.BLUE, end='|')
            else:
                print(Fore.GREEN, row, Fore.BLUE, end='|')

            for column in range(len(app_interface_second) - 1):

                if app_interface_second[row][column] in list_:
                    print(Fore.GREEN, app_interface_second[row][column], Fore.BLUE, end='|')

                elif app_interface_second[row][column] == Board.HITTING_SHIP:
                    print(Fore.RED, app_interface_second[row][column], Fore.BLUE, end='|')

                elif app_interface_second[row][column] == Board.SHOT_MISSED:
                    print(Fore.YELLOW, app_interface_second[row][column], Fore.BLUE, end='|')

                elif app_interface_second[row][column] == Board.PART_SHIP:
                    print(Fore.RED, app_interface_second[row][column], Fore.BLUE, end='|')

                else:
                    print(Fore.BLUE, app_interface_second[row][column], Fore.BLUE, end='|')

            print('\n')
        print(Style.RESET_ALL)

    def get_app_interface_ships(self):
        """
        Метод, который выводит одно цветное поле. Суть та же что и в прошлом методе, только выводиться одно.
        """
        list_ = ['1', '2', '3', '4', '5', '6']
        app_interface = [['1', '2', '3', '4', '5', '6']]

        app_interface += self.battlefield
        print(Fore.BLUE)

        for row in range(len(app_interface)):
            if row == 0:
                print(Fore.GREEN, ' ', Fore.BLUE, end='|')
            else:
                print(Fore.GREEN, row, Fore.BLUE, end='|')

            for column in range(len(app_interface) - 1):

                if app_interface[row][column] in list_:
                    print(Fore.GREEN, app_interface[row][column], Fore.BLUE, end='|')

                elif app_interface[row][column] == Board.HITTING_SHIP:
                    print(Fore.RED, app_interface[row][column], Fore.BLUE, end='|')

                elif app_interface[row][column] == Board.SHOT_MISSED:
                    print(Fore.YELLOW, app_interface[row][column], Fore.BLUE, end='|')

                elif app_interface[row][column] == Board.PART_SHIP:
                    print(Fore.RED, app_interface[row][column], Fore.BLUE, end='|')

                else:
                    print(Fore.BLUE, app_interface[row][column], Fore.BLUE, end='|')
            print('\n')
        print(Style.RESET_ALL)

    def get_interface(self):
        return self.battlefield
