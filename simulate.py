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
    ["blue", "white", "green"],  # 3
    [],  # 4
    [],  # 5
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



# Use for simulating a full game
GAMEBOARD = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

# Populate from human-friendly names
if GAMEBOARD_FROM_COLOURS:
    for slot, contents in enumerate(GAMEBOARD_FROM_COLOURS):
        for camel_colour in contents:
            GAMEBOARD[slot] += [CAMEL_COLOUR_TO_ID[camel_colour]]

print("Starting gameboard:")
print(GAMEBOARD)


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
            global WINNER
            WINNER = camel_to_move  # Winner of the game
            return

        # Move them onto whatever stack is at the new position
        GAMEBOARD[camel_stack_new_position] += camel_stack_to_move

        # Remove the stack from the position we moved them from
        GAMEBOARD[slot_index] = GAMEBOARD[slot_index][:layer_index]

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
    # print("End of round state:")
    # print(GAMEBOARD)


def simulate_game():
    while WINNER is None:
        simulate_leg()
        reset_pyramind()
    print("Final game state:")
    print(GAMEBOARD)
    print("WINNER:", WINNER)


def probabilities_for_leg():
    global GAMEBOARD, WINNER, CAMELS_LEFT_TO_ROLL
    starting_state = copy.deepcopy(GAMEBOARD)
    starting_camels_to_roll = copy.deepcopy(CAMELS_LEFT_TO_ROLL)

    times_first = {CAMEL_ID_TO_COLOUR[camel_id]: 0 for camel_id in CAMELS}
    times_second = {CAMEL_ID_TO_COLOUR[camel_id]: 0 for camel_id in CAMELS}

    n_simulations = 10000

    for i in range(n_simulations):
        # print("GAMEBOARD start", GAMEBOARD)
        simulate_leg()
        positions = get_current_positions()
        # print(positions)

        times_first[CAMEL_ID_TO_COLOUR[positions[0]]] += 1
        times_second[CAMEL_ID_TO_COLOUR[positions[1]]] += 1

        GAMEBOARD = copy.deepcopy(starting_state)
        CAMELS_LEFT_TO_ROLL = copy.deepcopy(starting_camels_to_roll)

    for camel in sorted(times_first, key=times_first.get, reverse=True):
        print("Camel", camel, "wins", round(times_first[camel] / n_simulations * 100.0), "%")

    for camel in sorted(times_second, key=times_second.get, reverse=True):
        print("Camel", camel, "comes second", round(times_second[camel] / n_simulations * 100.0), "%")


probabilities_for_leg()