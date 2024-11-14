# %%
import strategies as strat
import graph as gr
import Play_Sim as play
from Population_system import Population

import time
import numpy as np

start_time = time.time()

# Simulation Vars
# ===Reward Matrix===
# ---Coin Machine---
# FOR 2 PLAYERS
# This reward matrix uses the coin machine: put 1 in, give 3 to opponent
# If you both put 1 in, you each profit 2;
# if you put in 1, but your opponent doesnt, you lose 1, and your opponent gains 3
# if neither of you put a coin in, nothing happens
reward_matrix = [
    [0, 0],  # Cheat-Cheat
    [-1, 3],  # Coop-Cheat
    [3, -1],  # Cheat-Coop
    [2, 2],  # Coop-Coop
]
# ---Fruit Tree---
# FOR 3 PLAYERS
# A fruit tree has 9 fruits
# A cooperator will try to take 3, leaving an equal amount for the other players
# A cheater (eagle) will take their 3, and will take 1 from each cooperator
# Each eagle loses a fruits worth of energy fighting each other eagle at its tree
p3_RM = [
    [3],  # all coop
    [2, 5],  # 2 coop, 1 cheat: coop_score, cheat_score
    [1, 4],  # 1 coop, 2 cheat: coop_score, cheat_score
    [1],  # all cheat: try 0
]

# <><><><><><><><><><><><><>
# ===Control Vars===
# Note: this only the chance a coop becomes a cheat - the inverse is not considered in this model
mistake_chance = 0.00
# Number of members in the population
pop_N = 100
# Number of times a given member plays a given opponent
num_rounds = 10
# The number of the bottom x members that are replaced with the top x members
num_replace = 5
# Max number of times the population is evolved
max_gen = 15
# <><><><><><><><><><><><><>


def for_three():
    pop = Population(pop_N, num_rounds, num_replace, mistake_chance, p3_RM)
    pop.set_play(play.play_every_combo_3)
    return pop


def for_two():
    pop = Population(pop_N, num_rounds, num_replace, mistake_chance, reward_matrix)
    pop.set_play(play.play_all_2)
    return pop


def test_time():
    times = []
    for r in np.arange(10, 21, 1):
        print(f"{r}{{")
        pop_times = []
        for n in np.arange(10, 20, 1):
            print(n)
            start = time.time()
            pop = Population(n, r, num_replace, mistake_chance, reward_matrix)
            pop.set_play(play.play_every_combo_3)
            pop.add_type("Always Cheat", strat.AlwaysCheat, 0.2)
            pop.add_type("Copy Cat", strat.CopyCat, 0.2)
            pop.add_type("Copy Kitten", strat.CopyKitten, 0.2)
            pop.add_type("Variant Cat", strat.CopyCatVariant, 0.2)
            pop.add_type("Variant Kitten", strat.CopyKittenVariant, 0.2)
            pop.assemble()
            pop.run_tournament(10, show=False)
            pop_times.append([n, ((time.time()-start)/10)])
            del pop
        print("}")
        times.append([r, pop_times])
    gr.plot_times(times)


def main():
    # pop = for_three()
    pop = for_two()
    pop.add_type("Always Coop", strat.AlwaysCoop, 0.2)
    pop.add_type("Always Cheat", strat.AlwaysCheat, 0.2)
    pop.add_type("Random", strat.Random, 0.2)
    pop.add_type("Copy Cat", strat.CopyCat, 0.2)
    pop.add_type("Grudger", strat.Grudger, 0.2)
    # pop.add_type("Copy Kitten", strat.CopyKitten, 0.2)
    # pop.add_type("Variant Cat", strat.CopyCatVariant, 0.2)
    # pop.add_type("Variant Kitten", strat.CopyKittenVariant, 0.2)
    pop.assemble()
    print("===Control Vars===")
    print(f"The Total Population is: {pop_N}")
    print(f"The Max. Generation is: {max_gen}")
    print(f"The Number of Rounds between players is: {num_rounds}")
    print(f"Each Evolution Replaces the bottom: {num_replace} members")
    print(f"The Mistake Chance is: {mistake_chance*100}%")
    pop.run_tournament(max_gen)
    print("===Execution Time===")
    print(f"Execution Time: {time.time()-start_time} seconds")


# main()
main()

# %%
