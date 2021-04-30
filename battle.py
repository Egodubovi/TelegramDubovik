import random

s_x = s_y = 10
ships = s_x
enemy_ships1 = [[0 for i in range(s_x)] for i in range(s_y)]
enemy_ships2 = [[0 for i in range(s_x)] for i in range(s_y)]
ships_list = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]


def generate_enemy_ships():
    global ships_list
    enemy_ships = []
    sum_1_all_ships = sum(ships_list)
    sum_1_enemy = 0
    while sum_1_enemy != sum_1_all_ships:
        enemy_ships = [[0 for i in range(s_x)] for i in
                       range(s_y)]
        for i in range(0, ships):
            len = ships_list[i]
            horizont_vertikal = random.randrange(1, 3)
            primerno_x = random.randrange(0, s_x)
            if primerno_x + len > s_x:
                primerno_x = primerno_x - len
            primerno_y = random.randrange(0, s_y)
            if primerno_y + len > s_y:
                primerno_y = primerno_y - len
            if horizont_vertikal == 1:
                if primerno_x + len <= s_x:
                    for j in range(0, len):
                        try:
                            check_near_ships = 0
                            check_near_ships = enemy_ships[primerno_y][primerno_x - 1] + \
                                               enemy_ships[primerno_y][primerno_x + j] + \
                                               enemy_ships[primerno_y][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y + 1][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y - 1][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y + 1][primerno_x + j] + \
                                               enemy_ships[primerno_y - 1][primerno_x + j]
                            if check_near_ships == 0:
                                enemy_ships[primerno_y][primerno_x + j] = i + 1
                        except Exception:
                            pass
            if horizont_vertikal == 2:
                if primerno_y + len <= s_y:
                    for j in range(0, len):
                        try:
                            check_near_ships = 0
                            check_near_ships = enemy_ships[primerno_y - 1][primerno_x] + \
                                               enemy_ships[primerno_y + j][primerno_x] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x + 1] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x - 1] + \
                                               enemy_ships[primerno_y + j][primerno_x + 1] + \
                                               enemy_ships[primerno_y + j][primerno_x - 1]
                            if check_near_ships == 0:
                                enemy_ships[primerno_y + j][primerno_x] = i + 1
                        except Exception:
                            pass
        sum_1_enemy = 0
        for i in range(0, s_x):
            for j in range(0, s_y):
                if enemy_ships[j][i] > 0:
                    sum_1_enemy = sum_1_enemy + 1
        enemy_ships = [[' ▓ ' if i != 0 else ' ░ ' for i in j] for j in enemy_ships]
    return enemy_ships


enemy_ships1 = generate_enemy_ships()
enemy_ships2 = generate_enemy_ships()
