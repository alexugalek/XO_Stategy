import random
import copy

"""Sample player module.
- make_turn function is mandatory.
- Module shouldn't contain code outside functions (you can add any number 
of functions you need.
"""


def make_turn(board, symb):
    """ Function that makes turn. It should choose field to put your mark.

    Chosen field should be empty (contain None in board)

    Args:
        board: [['X', 'O', None,...],
                [None, None, ...],
                ...
               ] - list of lists len(board)==20,
               len[board[0]]==20 - inner lists are
               rows of 20x20 matrix.
        symb: 'X' or 'O' - capitalized letter - you symbol.

    Returns:
        (column_index, row_index) -
        tuple that contains two integers. 0 <= index <=19.

    """

    symb_enemy = 'O' if symb == 'X' else 'X'

    w_board_attack = [[0 for _ in range(20)] for _ in range(20)]
    w_board_defence = [[0 for _ in range(20)] for _ in range(20)]

    def validate_pos(row_nmb, col_nmb):
        if all(0 <= value < 20 for value in (row_nmb, col_nmb)):
            return True
        return False

    def templates(s, tmp_list):
        weight_dict = {
            (s, s, s, s, s): 1000000,
            (None, s, s, s, s, None): 7000,
            (None, s, s, s, s): 4000,
            (None, s, s, s, None): 3000,
            (None, s, None, s, s, s): 2000,
            (None, s, s, None, s, s): 2000,
            (None, s, s, s, None, s): 2000,
            (None, s, s, s): 1500,
            (None, s, s, None, s): 800,
            (None, s, None, s, s): 800,
            (None, s, s, None): 200,
            (s, None): 15
        }
        tmp_max_weight1, tmp_max_weight2 = 1, 1
        for key, value in weight_dict.items():
            if key == tuple(tmp_list):
                tmp_max_weight1 = weight_dict.get(tuple(tmp_list))
            if key == tuple(reversed(tmp_list)):
                tmp_max_weight2 = weight_dict.get(tuple(reversed(tmp_list)))
        return max(tmp_max_weight1, tmp_max_weight2)

    offsets = ((0, 4), (-1, 3), (-2, 2), (-3, 1), (-1, 2), (-2, 1), (-4, 0),
               (-3, 0), (-1, 4), (-3, 2), (-4, 1), (-5, 0), (-2, 3))

    const = ((0, 1), (1, 0), (1, 1), (1, -1))

    new_board = copy.deepcopy(board)

    set_attack, set_defence = set(), set()

    def weight_counter(line, column, symb_tmp, l_of, r_of, kx, ky):

        if validate_pos(line + l_of * kx, column + l_of * ky) and \
                validate_pos(line + r_of * kx, column + r_of * ky):
            new_board[line][column] = symb_tmp

            lst_tmp = [new_board[line + j * kx][column + j * ky]
                       for j in range(l_of, r_of + 1)]

            if symb_tmp != symb_enemy:
                set_attack.add(templates(symb_tmp, lst_tmp))
            else:
                set_defence.add(templates(symb_tmp, lst_tmp))

    def weight_maker(line, column, my_symb, enemy_symb):

        nonlocal set_attack, set_defence
        for left, right in offsets:
            for kx, ky in const:
                weight_counter(line, column, my_symb, left, right, kx, ky)
                weight_counter(line, column, enemy_symb, left, right, kx, ky)

        w_board_attack[line][column] = sum(set_attack)
        w_board_defence[line][column] = sum(set_defence)
        set_attack, set_defence = set(), set()

        new_board[line][column] = None

    max_weight_attack, max_weight_defence = 0, 0
    for row_nmb, row in enumerate(board):
        for col_nmb, element in enumerate(row):
            if element is None:
                weight_maker(row_nmb, col_nmb, symb, symb_enemy)
                if w_board_attack[row_nmb][col_nmb] > max_weight_attack:
                    max_weight_attack = w_board_attack[row_nmb][col_nmb]
                if w_board_defence[row_nmb][col_nmb] > max_weight_defence:
                    max_weight_defence = w_board_defence[row_nmb][col_nmb]

    if board[10][10] is None and symb == 'X':
        return 10, 10

    if max_weight_defence > max_weight_attack:
        max_weight = max_weight_defence
    else:
        max_weight = max_weight_attack

    for row_nmb, row in enumerate(board):
        for col_nmb, element in enumerate(row):
            if (w_board_attack[row_nmb][col_nmb] == max_weight or
                w_board_defence[row_nmb][col_nmb] == max_weight) and \
                    element is None:
                return col_nmb, row_nmb
