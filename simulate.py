from random import randint, choice

camels = [1, 2, 3, 4, 5]

# Use for simulating a full game
# GAMEBOARD = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

# Use for simulating from partial state
GAMEBOARD = [
    [],  # 1
    [4, 1],  # 2
    [3, 5, 2],  # 3
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

print("Starting gameboard:")
print(GAMEBOARD)


CAMELS_LEFT_TO_ROLL = set()
WINNER = None


def reset_pyramind():
    global CAMELS_LEFT_TO_ROLL
    CAMELS_LEFT_TO_ROLL = set(camels)


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

    print("Moving camel", camel_to_move, "for", amount_to_move)

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

    print(GAMEBOARD)
    return None


def simulate_leg():
    reset_pyramind()
    while len(CAMELS_LEFT_TO_ROLL) > 0:
        simuluate_turn()
    print("End of round state:")
    print(GAMEBOARD)


def simulate_game():
    while WINNER is None:
        simulate_leg()
    print("Final game state:")
    print(GAMEBOARD)
    print("WINNER:", WINNER)


simulate_game()