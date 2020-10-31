class Ship:
    def __init__(self, size=None, coordinate=None):
        self.size = size
        self.coordinate = coordinate

    def set_size(self, size, checklist_ships, count_ship):
        """
        Метод проверка размера корабля. Елси размер не подходит ни к одному условию, то возращается False.
        Если размер подходит, то атрибуту обйекта присваивается новый размер, и уменьшается счетчик кораблей.
        Если счетчик = 0, то корабль удаляется из списка и его размер больше нельзя ввести.
        """
        if size == '3' and count_ship['count_three'] > 0:

            self.size = '3'
            count_ship['count_three'] -= 1

            if count_ship['count_three'] == 0:
                checklist_ships.remove('3')

            return True

        elif size == '2' and count_ship['count_two'] > 0:

            self.size = '2'
            count_ship['count_two'] -= 1

            if count_ship['count_two'] == 0:
                checklist_ships.remove('2')

            return True

        elif size == '1' and count_ship['count_one'] > 0:

            self.size = '1'
            count_ship['count_one'] -= 1

            if count_ship['count_one'] == 0:
                checklist_ships.remove('1')

            return True

        else:
            return False

    def verify_coordinate(self, start_coordinate, end_coordinate, interface_ship):
        """
            Метод, который проверяет координаты введенные ползователем. Если все проверки пройдены, то запускается
        метод проверки ячейки на поле и возращается его результат.
            Проверки: Координаты должны быть 2, Конечная координата должна быть больше начальной, Если
        метод get_coordinate() возращает None, то координаты не установелны.
        """
        if len(start_coordinate) != 2 and len(end_coordinate) != 2:
            return 'Invalid coordinate'

        try:
            if any([start_coordinate[0] > end_coordinate[0],
                    start_coordinate[1] > end_coordinate[1]]):

                return 'Invalid coordinate, end coordinate < start coordinate'

        except IndexError:
            return 'Invalid coordinate'

        location = [start_coordinate, end_coordinate]

        self.set_coordinate(location)

        if self.get_coordinate() is None:
            return 'Invalid coordinate'

        else:
            return interface_ship.verify_cell(self.get_coordinate())

    def set_coordinate(self, coordinate):
        """
            Метод, который присваивет атрибуту объекта новые значения. Он проверяет соответствие
        между размером корабля и введеным координатами. Если всё сходиться, то новое значение атрибута.
        Если не сходиться, атрибут попрежнему остаеться None.
        """
        if self.size == "3":

            if any([coordinate[0][0] == coordinate[1][0] and abs(coordinate[0][1] - coordinate[1][1]) == 2,
                    coordinate[0][1] == coordinate[1][1] and abs(coordinate[0][0] - coordinate[1][0]) == 2]):
                self.coordinate = coordinate

        elif self.size == "2":

            if any([coordinate[0][0] == coordinate[1][0] and abs(coordinate[0][1] - coordinate[1][1]) == 1,
                    coordinate[0][1] == coordinate[1][1] and abs(coordinate[0][0] - coordinate[1][0]) == 1]):
                self.coordinate = coordinate
        else:
            if coordinate[0][0] == coordinate[1][0] and coordinate[0][1] == coordinate[1][1]:
                self.coordinate = coordinate

    def get_coordinate(self):
        return self.coordinate

    def get_size(self):
        return self.size
