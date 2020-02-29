from random import randint, choice
import copy

CAMELS = [1, 2, 3, 4, 5]
CAMEL_COLOUR_TO_ID = {
    "orange": 1,
    "green": 2,
    "blue": 3,
    "yellow": 4,
    "white": 5
}
CAMEL_ID_TO_COLOUR = dict(reversed(item) for item in CAMEL_COLOUR_TO_ID.items())

# Camel on right-hand-side is on top
GAMEBOARD_FROM_COLOURS = [
    [],  # 1
    ["yellow", "orange"],  # 2
    ["blue", "white"],  # 3
    [],  # 4
    ["green"],  # 5
    [],  # 6
    [],  # 7
    [],  # 8
    [],  # 9
    [],  # 10
    [],  # 11
    [],  # 12
    [],  # 13
    [],  # 14
    [],  # 15
    []  # 16
]

# Position: modifier
# E.g. 4: -1 would mean there is a -1 movement desert tile on slot 4 of the board
DESERT_TILES = {
    4: -1
}

# Convert to array indices instead of gameboard slots
DESERT_TILES = {tile - 1: modifier for (tile, modifier) in DESERT_TILES.items()}

# Use for simulating a full game
GAMEBOARD = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

# Populate from human-friendly names
if GAMEBOARD_FROM_COLOURS:
    for slot, contents in enumerate(GAMEBOARD_FROM_COLOURS):
        for camel_colour in contents:
            GAMEBOARD[slot] += [CAMEL_COLOUR_TO_ID[camel_colour]]

print("Starting gameboard:\n", GAMEBOARD_FROM_COLOURS or GAMEBOARD)


CAMELS_LEFT_TO_ROLL = set(CAMELS)
WINNER = None


def reset_pyramind():
    global CAMELS_LEFT_TO_ROLL
    CAMELS_LEFT_TO_ROLL = set(CAMELS)


def roll_dice():
    dice = choice(tuple(CAMELS_LEFT_TO_ROLL))
    value = randint(1, 3)

    CAMELS_LEFT_TO_ROLL.remove(dice)
    return dice, value


# TODO: Optimize lookup
def find_camel(camel_to_find):
    for i, slot in enumerate(GAMEBOARD):
        for j, camel in enumerate(slot):
            if camel == camel_to_find:
                return i, j
    return None, None


def simuluate_turn():
    global WINNER
    camel_to_move, amount_to_move = roll_dice()

    # print("Moving camel", camel_to_move, "for", amount_to_move)

    # Slot = GAMEBOARD position, layer = position in stack of camels
    slot_index, layer_index = find_camel(camel_to_move)

    if slot_index is None:
        # Camel not in gameboard, must be starting turns
        GAMEBOARD[amount_to_move - 1] += [camel_to_move]
    else:
        # Camel stack to move as a unit
        camel_stack_to_move = GAMEBOARD[slot_index][layer_index:]

        camel_stack_new_position = slot_index + amount_to_move

        if camel_stack_new_position >= 15:
            WINNER = camel_to_move  # Winner of the game
            return

        # Remove the stack from the position we moved them from
        GAMEBOARD[slot_index] = GAMEBOARD[slot_index][:layer_index]

        if camel_stack_new_position in DESERT_TILES.keys():
            # print("Desert tile in play")
            # There is a desert tile in the new location
            if DESERT_TILES[camel_stack_new_position] > 0:

                camel_stack_new_position += 1
                if camel_stack_new_position >= 15:
                    WINNER = camel_to_move  # Winner of the game
                    return

                # Move them onto whatever stack is at the new position
                GAMEBOARD[camel_stack_new_position] += camel_stack_to_move
            else:
                camel_stack_new_position -= 1
                # Move them to the bottom of any stack already there
                GAMEBOARD[camel_stack_new_position] = camel_stack_to_move + GAMEBOARD[camel_stack_new_position]
        else:
            # Move them onto whatever stack is at the new position
            GAMEBOARD[camel_stack_new_position] += camel_stack_to_move

    # print(GAMEBOARD)
    return None


def get_current_positions():
    order = []
    for slot in reversed(GAMEBOARD):
        for camel in reversed(slot):
            order += [camel]
    return order


def simulate_leg():
    while len(CAMELS_LEFT_TO_ROLL) > 0:
        simuluate_turn()


def simulate_game():
    while WINNER is None:
        simulate_leg()
        reset_pyramind()
    # print("Final game state:\n", GAMEBOARD)
    # print("WINNER:", WINNER)


def print_recommendations_for_leg():
    global GAMEBOARD, WINNER, CAMELS_LEFT_TO_ROLL
    starting_state = copy.deepcopy(GAMEBOARD)
    starting_camels_to_roll = copy.deepcopy(CAMELS_LEFT_TO_ROLL)

    times_first = {CAMEL_ID_TO_COLOUR[camel_id]: 0 for camel_id in CAMELS}
    times_second = {CAMEL_ID_TO_COLOUR[camel_id]: 0 for camel_id in CAMELS}

    n_simulations = 50000

    for i in range(n_simulations):
        simulate_leg()
        positions = get_current_positions()

        times_first[CAMEL_ID_TO_COLOUR[positions[0]]] += 1
        times_second[CAMEL_ID_TO_COLOUR[positions[1]]] += 1

        GAMEBOARD = copy.deepcopy(starting_state)
        CAMELS_LEFT_TO_ROLL = copy.deepcopy(starting_camels_to_roll)
        WINNER = None
        # print("Reset board back to:\n", GAMEBOARD)

    print("\nRecommendations for short-term bets:")
    for gold_value_of_bet in [5, 3, 2]:
        expected_values = {camel: gold_value_of_bet * (times_first[camel] / n_simulations) for camel in times_first.keys()}

        # Add on value of it coming second (reward: 1)
        expected_values = {camel: expected_values[camel] + (times_second[camel] / n_simulations) for camel in times_second.keys()}

        for camel in sorted(expected_values, key=expected_values.get, reverse=True):
            if expected_values[camel] > 1:
                print("Camel", camel, "expected value at bet", gold_value_of_bet, " is ", round(expected_values[camel], 1))
    print("If none of these are available, do a long term bet, place a road block, or roll a dice")


def print_recommendations_for_game():
    global GAMEBOARD, WINNER, CAMELS_LEFT_TO_ROLL
    starting_state = copy.deepcopy(GAMEBOARD)
    starting_camels_to_roll = copy.deepcopy(CAMELS_LEFT_TO_ROLL)

    times_first = {CAMEL_ID_TO_COLOUR[camel_id]: 0 for camel_id in CAMELS}
    times_last = {CAMEL_ID_TO_COLOUR[camel_id]: 0 for camel_id in CAMELS}

    n_simulations = 50000

    for i in range(n_simulations):
        simulate_game()
        positions = get_current_positions()

        times_first[CAMEL_ID_TO_COLOUR[WINNER]] += 1
        times_last[CAMEL_ID_TO_COLOUR[positions[-1]]] += 1

        GAMEBOARD = copy.deepcopy(starting_state)
        CAMELS_LEFT_TO_ROLL = copy.deepcopy(starting_camels_to_roll)
        WINNER = None

    print("\nRecommendations for long-term bets:")
    expected_values_for_first = {camel: 8 * (times_first[camel] / n_simulations) for camel in
                       times_first.keys()}

    # Add on value of it coming second (reward: 1)
    expected_values_for_last = {camel: 8 * (times_last[camel] / n_simulations) for camel in
                       times_last.keys()}

    for camel in sorted(expected_values_for_first, key=expected_values_for_first.get, reverse=True):
        if expected_values_for_first[camel] > 1:
            print("Camel", camel, "expected value to win is ", round(expected_values_for_first[camel], 1))

    print("")
    for camel in sorted(expected_values_for_last, key=expected_values_for_last.get, reverse=True):
        if expected_values_for_last[camel] > 1:
            print("Camel", camel, "expected value to come last is ", round(expected_values_for_last[camel], 1))

    print("If none of these are available, place a road block, or roll a dice")


print_recommendations_for_leg()
print_recommendations_for_game()