"""nqueens.py: Using a hill climbing algorithm with random restarts, this
program strives to find a chess board of n*n size with a queen in each column
where no queen is capable of attacking another. The program attempts to make the
best move possible on every turn, moving one queen at a time."""

__author__ = "Aidan Kaiser"
__copyright__ = "Copyright 2020, Aidan Kaiser"
__credits__ = ['https://stackoverflow.com/questions/533905/get-the-cartesian-product-of-a-series-of-lists - for the '
               'succ function, I used stack overflow to figure out how to get the cartesian product of two sets']

import itertools
import random

def succ(state, boulderX, boulderY):
    num_rows = len(state)
    comb_list = []
    for i in range(0, num_rows):
        comb_list.append(i)
    state_options = []
    for i in range(0, num_rows):
        options = []
        for x in range(0, num_rows):
            if i == boulderX and x == boulderY:
                continue
            options.append(x)
        state_options.append(options)
    final_options = []
    final_options_edited = []
    for element in itertools.product(*state_options):
        final_options.append(list(element))
    for a_list in final_options:
        moved_count = 0
        for i in range(0, num_rows):
            if state[i] != a_list[i]:
                moved_count = moved_count + 1
        if moved_count == 1:
            final_options_edited.append(a_list)
    return final_options_edited

def check_row_attacked(state, boulderX, boulderY, attacked):
    num_rows = len(state)
    for i in range(0, num_rows):
        sight_with_boulder = num_rows - i
        if boulderX != i and boulderY == state[i]:
            if boulderX - i > 0:
                sight_with_boulder = boulderX - i - 1
            elif boulderX - i == 0:
                continue
        for x in range(0, sight_with_boulder):
            if state[i] == state[i + x] and x != 0:
                attacked[i] = 1
                attacked[i + x] = 1

def calc_down_diag_sight(x_pos, y_pos, num_rows):
    sight = 0
    while x_pos < num_rows - 1 and y_pos < num_rows - 1:
        x_pos = x_pos + 1
        y_pos = y_pos + 1
        sight = sight + 1
    return sight

def calc_up_diag_sight(x_pos, y_pos, num_rows):
    sight = 0
    while x_pos < num_rows - 1 and y_pos > 0:
        x_pos = x_pos + 1
        y_pos = y_pos - 1
        sight = sight + 1
    return sight

def check_diagonal_attacked(state, boulderX, boulderY, attacked):
    num_rows = len(state)
    for i in range(0, num_rows):
        sight_with_boulder = calc_down_diag_sight(i, state[i], num_rows)
        if (boulderX - i == boulderY - state[i]) and boulderX - i > 0:
            sight_with_boulder = boulderX - i
        elif (boulderX - i == boulderY - state[i]) and boulderX - i == 0:
            continue
        for x in range(0, sight_with_boulder + 1):
            if state[i] + x == state[i + x] and x != 0 and i + x <= num_rows - 1:
                attacked[i] = 1
                attacked[i + x] = 1
    for i in range(0, num_rows):
        sight_with_boulder = calc_up_diag_sight(i, state[i], num_rows)
        if boulderX - i == ((boulderY - state[i]) * -1) and boulderX - i > 0:
            sight_with_boulder = boulderX - i
        elif (boulderX - i == ((boulderY - state[i]) * -1)) and boulderX - i == 0:
            continue
        for x in range(0, sight_with_boulder + 1):
            if state[i] - x == state[i + x] and x != 0 and i + x <= num_rows - 1:
                attacked[i] = 1
                attacked[i + x] = 1

def f(state, boulderX, boulderY):
    num_rows = len(state)
    attacked = []
    for i in range(0, num_rows):
        attacked.append(0)
    check_row_attacked(state, boulderX, boulderY, attacked)
    check_diagonal_attacked(state, boulderX, boulderY, attacked)
    attacked_count = 0
    for i in attacked:
        if i == 1:
            attacked_count = attacked_count + 1
    return attacked_count

def choose_next(curr, boulderX, boulderY):
    succ_array = succ(curr, boulderX, boulderY)
    succ_array.append(curr)
    succ_f_values = []
    for i in succ_array:
        succ_f_values.append(f(i, boulderX, boulderY))
    lowest_f = -1
    count_of_lowest = 0
    for i in succ_f_values:
        if i < lowest_f or lowest_f == -1:
            lowest_f = i
            count_of_lowest = 1
        elif i == lowest_f:
            count_of_lowest = count_of_lowest + 1
    if lowest_f == -1:
        return None
    if count_of_lowest > 1:
        lowest_indices = [i for i, x in enumerate(succ_f_values) if x == lowest_f]
        lowest = []
        for i in range(0, len(succ_array)):
            if i in lowest_indices:
                lowest.append(succ_array[i])
        lowest = sorted(lowest)
        if lowest[0] == curr:
            return None
        else:
            return lowest[0]
    lowest_state = succ_array[succ_f_values.index(lowest_f)]
    if lowest_state == curr:
        return None
    else:
        return lowest_state

def nqueens(initial_state, boulderX, boulderY):
    current = initial_state
    while True:
        print(str(current) + " - f=" + str(f(current, boulderX, boulderY)))
        if f(current, boulderX, boulderY) == 0:
            return current
        next = choose_next(current, boulderX, boulderY)
        if next is None:
            return current
        current = next

def nqueens_restart(n, k, boulderX, boulderY):
    solutions = []
    for i in range(0, k):
        state = []
        for x in range(0, n):
            rand = random.randint(0, n - 1)
            state.append(rand)
        while state[boulderX] == boulderY:
            state = []
            for x in range(0, n):
                rand = random.randint(0, n - 1)
                state.append(rand)
        solve = nqueens(state, boulderX, boulderY)
        if f(solve, boulderX, boulderY) == 0:
            print("Solution:\n" + str(solve) + " - f=0")
            return
        solutions.append({"SOLUTION": solve, "F": f(solve, boulderX, boulderY)})
    lowest_f = -1
    for i in solutions:
        if i["F"] < lowest_f or lowest_f == -1:
            lowest_f = i["F"]
    print("Best Solution(s):")
    for i in sorted(solutions):
        if i["F"] == lowest_f:
            print(str(i["SOLUTION"]) + " - f=" + str(i["F"]))



