import random

atoms = 1000
decay_chance = 0.03
for t in range(50):
    decayed_this_turn = 0
    for i in range(atoms): 
        if random.random() < decay_chance:
            decayed_this_turn += 1
    atoms -= decayed_this_turn
    print(f"Time {t}: {atoms} left")