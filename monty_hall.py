
import random

def regular_guessing(total = 10000) -> int:
    wins = 0
    doors = [1, 2, 3]
    for _ in range(total):
        winning_door = random.choice(doors)
        guessed_door = random.choice(doors)
        wins += winning_door == guessed_door
    return wins

def monty_hall_guessing(total = 10000) -> int:
    def remove_non_winning_door(doors_to_pick, winning_door_num, guessed_door_num):
        doors = doors_to_pick[:]
        other_door = random.choice(list(set(doors) - set([winning_door_num, guessed_door_num])))
        doors.remove(other_door)
        return doors
    wins = 0
    doors = [1, 2, 3]
    for _ in range(total):
        winning_door = random.choice(doors)
        guessed_door = random.choice(doors)
        new_doors = remove_non_winning_door(doors, winning_door, guessed_door)
        switched_door = random.choice(new_doors)
        wins += winning_door == switched_door
    return wins

if __name__ == "__main__":
    total = 200000
    print(f'regular guessing: {round(regular_guessing(total) / total * 100,1)}%')
    print(f'switching door: {round(monty_hall_guessing(total) / total * 100,1)}%')
