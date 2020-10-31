from colorama import Fore, Style
from copy import deepcopy
from battleships_game.class_board import Board
from battleships_game.class_ship import Ship
import time
from random import randint


checklist = ['1', '2', '3']
count_ships = {'count_one': 4,
               'count_two': 2,
               'count_three': 1}
coordinate_state = ('Invalid coordinate',
                    'Invalid coordinate, end coordinate < start coordinate',
                    'Cell is busy',
                    'Cell if free')

interface = [['O' for i in range(6)] for j in range(6)]  # Общий список для четырёх переменных

"""
Четыре объекта, принимают полную копию созданного списка. Если использовать метод списоков .copy(),
измения одного списка будут отображаться в остальных
"""
user_interface_ship = Board(deepcopy(interface))
user_interface_shot = Board(deepcopy(interface))
random_interface_ship = Board(deepcopy(interface))
random_interface_shot = Board(deepcopy(interface))

print(Fore.RED)
print("-------------------------------------------------------------------------------------------")
print("Важно")
print("1. Координаты нужно вводить через ПРОБЕЛ. Сначала начальная, потом конченая.")
print("   Пример ввода: Введите первые координаты через пробел: 2 1")
print("                 Введите вторые координаты через пробел: 2 2\n")
print("2. Первая координата не может быть больше конченой")
print("   Пример НЕПРАВИЛЬНОГО ввода: Введите первые координаты через пробел: 2 2")
print("                               Введите вторые координаты через пробел: 2 1")
print("   Пример правильного воода в первом пункте")
print("3. Если вы вводите координаты ОДНОПАЛУБНОГО корабля, то достаточно ввести координату один раз\n")
print("4. Если вы ввели первую координату неправильно или не ту что хотели, то при вводе воторой нажмите Enter")

while True:
    print("-------------------------------------------------------------------------------------------")
    print(Fore.GREEN)
    print("У вас в наличии:")
    print(f"           Корабль на 3 клетки - {count_ships['count_three']}шт,")
    print(f"           Корабль на 2 клетки - {count_ships['count_two']}шт,")
    print(f"           Корабль на 1 клетки - {count_ships['count_one']}шт\n")
    print("Если на 3 клетки, то введите цифру 3")
    print("Если на 2 клетки, то введите цифру 2")
    print("Если на 1 клетки, то введите цифру 1")
    print(Style.RESET_ALL)
    print("-------------------------------------------------------------------------------------------\n")

    ship = Ship()

    print(Fore.BLUE)
    user_input_size = input("Введите размер корабля: ").strip()

    size_ship = ship.set_size(user_input_size, checklist, count_ships)

    while not size_ship:

        print(Fore.RED, "Вы ввели неверный размер корабля", Style.RESET_ALL)
        print(Fore.BLUE)

        user_input_size = input("Введите размер корабля: ").strip()

        print(Style.RESET_ALL)

        size_ship = ship.set_size(user_input_size, checklist, count_ships)

    print()

    user_interface_ship.get_app_interface_ships()

    print(Fore.RED)

    if ship.get_size() == '3':
        print("Вы вводите коориднаты трёхпалубного корабля!!\n")

    elif ship.get_size() == '2':
        print("Вы вводите коориднаты двухпалубного корабля!!\n")

    else:
        print("Вы вводите коориднаты однопалубного корабля!!\n")

    print(Style.RESET_ALL)

    while True:
        try:
            start_ship = [int(i) - 1 for i in input("Введите первые координаты через пробел: ").split()]

            if ship.get_size() == '1':
                end_ship = start_ship.copy()

            else:
                end_ship = [int(i) - 1 for i in input("Введите вторые координаты через пробел: ").split()]

        except ValueError:

            print(Fore.RED)
            print("Нельзя вводить буквы")
            print(Style.RESET_ALL)

            continue

        verify_coordinate = ship.verify_coordinate(start_ship, end_ship, user_interface_ship)

        print(Fore.RED)

        if verify_coordinate == coordinate_state[0]:

            print("Вы ввели неверную координату")
            print(Style.RESET_ALL)

            continue

        elif verify_coordinate == coordinate_state[1]:

            print("Вы ввели неверную координату. Начальная координата не может быть больше конечной")
            print(Style.RESET_ALL)

            continue

        elif verify_coordinate == coordinate_state[2]:

            print("Ячейка занята")
            print(Style.RESET_ALL)

            continue

        elif verify_coordinate == coordinate_state[3]:

            break

    user_interface_ship.set_ship(ship.get_coordinate())

    user_interface_ship.get_app_interface_ships()

    print("Отлично, корабль на воде")

    del ship

    if all([count_ships['count_one'] == 0,
            count_ships['count_two'] == 0,
            count_ships['count_three'] == 0]):

        print(Fore.GREEN)
        print("Все корабли на поле", Style.RESET_ALL)

        break

checklist = ['1', '2', '3']
count_ships = {'count_one': 4,
               'count_two': 2,
               'count_three': 1}
while True:
    ship = Ship()

    random_input_size = str(randint(1, 3))

    size_ship = ship.set_size(random_input_size, checklist, count_ships)

    while not size_ship:

        random_input_size = str(randint(1, 3))

        size_ship = ship.set_size(random_input_size, checklist, count_ships)

    while True:

        start_ship = [randint(0, 5) for i in range(2)]

        if ship.get_size() == '1':
            end_ship = start_ship.copy()

        else:
            end_ship = [randint(0, 5) for i in range(2)]

        verify_coordinate = ship.verify_coordinate(start_ship, end_ship, random_interface_ship)

        if verify_coordinate == coordinate_state[3]:
            break
        else:
            continue

    random_interface_ship.set_ship(ship.get_coordinate())
    del ship

    if all([count_ships['count_one'] == 0,
            count_ships['count_two'] == 0,
            count_ships['count_three'] == 0]):
        break

print("-------------------------------------------------------------------------------------------")
print("Игра началась")

victory_check = False

while True:

    user_interface_ship.get_app_interface_ships_and_shots(user_interface_shot.get_interface())

    while True:
        try:
            print(Fore.GREEN, end=' ')
            user_shot = [int(i)-1 for i in input("Координаты выстрела: ").split()]
            print(Style.RESET_ALL)

            user_verify_re_shot = user_interface_shot.verify_re_shot(user_shot)

            if len(user_shot) > 2:
                print("Вы ввели неверные координаты")
                continue

            elif user_verify_re_shot == "Invalid coordinate":
                print("Вы ввели неверные координаты")
                continue

            elif user_verify_re_shot:
                print("Вы уже стреляли в эту ячейку. Введите другие координаты")
                continue

            ship_shot = random_interface_ship.shooting_interface_ship(user_shot, user_interface_shot)

            if ship_shot == "Missed":
                print(Style.RESET_ALL, "Твой ход: ", end=' ')
                print(Fore.GREEN, "Промах\n")
                break

            elif ship_shot == "Destroyed":

                time.sleep(0.5)

                print(Style.RESET_ALL, "Твой ход: ", end=' ')
                print(Fore.GREEN, "Убит\n")
                print(Style.RESET_ALL, '-----------------------------------------------------------------------------')

                user_interface_ship.get_app_interface_ships_and_shots(user_interface_shot.get_interface())

                continue

            elif ship_shot == "Alive":

                time.sleep(0.5)

                print(Style.RESET_ALL, "Твой ход: ", end=' ')
                print(Fore.GREEN, "Ранен\n")
                print(Style.RESET_ALL, '-----------------------------------------------------------------------------')

                user_interface_ship.get_app_interface_ships_and_shots(user_interface_shot.get_interface())

                continue

            elif ship_shot == "Victory":

                print(Style.RESET_ALL, '-----------------------------------------------------------------------------')
                print(' -----------------------------------------------------------------------------')
                print(Style.RESET_ALL, "Твой ход: ", end=' ')
                print(Fore.GREEN, "Убит")

                user_interface_ship.get_app_interface_ships_and_shots(user_interface_shot.get_interface())

                print(Fore.GREEN)
                print('-------------------------------ПОБЕДА----------------------------------------')

                victory_check = True
                break

            else:
                print("Не знаю что случилось, но вы никуда не попали и походу ни куда не стреляли")
                print("И поэтому введите координаты заново")

        except IndexError and ValueError:
            print("Вы ввели неверную координату")

    if victory_check:
        break

    time.sleep(0.5)

    while True:
        try:
            random_shot = [randint(0, 5) for i in range(2)]

            if random_interface_shot.verify_re_shot(random_shot):
                continue

            ship_shot = user_interface_ship.shooting_interface_ship(random_shot, random_interface_shot)

            if ship_shot == "Missed":

                print(Style.RESET_ALL, "Ход противника: ", end=' ')
                print(Fore.GREEN, f"Промах {random_shot[0]+1} {random_shot[1]+1}")

                break

            elif ship_shot == "Destroyed":

                print(Style.RESET_ALL, "Ход противника: ", end=' ')
                print(Fore.GREEN, f"Убит {random_shot[0]+1} {random_shot[1]+1}")

                continue

            elif ship_shot == "Alive":

                print(Style.RESET_ALL, "Ход противника: ", end=' ')
                print(Fore.GREEN, f"Ранен {random_shot[0]+1} {random_shot[1]+1}")

                continue

            elif ship_shot == "Victory":

                print(Style.RESET_ALL, '-----------------------------------------------------------------------------')
                print(' -----------------------------------------------------------------------------')

                user_interface_ship.get_app_interface_ships_and_shots(user_interface_shot.get_interface())

                print(Fore.RED)
                print('------------------------------ПОРАЖЕНИЕ--------------------------------------')

                victory_check = True

                break

        except IndexError:
            pass

    if victory_check:
        break

    time.sleep(0.5)

    print(Style.RESET_ALL, '-----------------------------------------------------------------------------')
    print(Fore.GREEN)
