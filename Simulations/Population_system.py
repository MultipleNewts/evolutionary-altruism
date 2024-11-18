import random
import graph as gr
import numpy as np


class Population:
    def __init__(self, size, nr, nrp, mc, rm):
        self.N = size
        self.population = []
        self.pop_flux = {}
        self.gen = 0
        self.types = []
        self.num_rounds = nr
        self.mistake_chance = mc
        self.reward_matrix = rm
        self.num_replace = nrp

    def assemble(self):
        id = 1
        ratio = 0
        for type in self.types:
            ratio += type[2]
            n = 0
            while n < ((self.N*type[2])//1):
                self.population.append(type[1](id, type[0]))
                n += 1
                id += 1
        if np.round(ratio, 10) != 1:
            raise AttributeError("Ratios do not sum to 1")

    def add_type(self, label, strategy, ratio=1):
        self.types.append([label, strategy, ratio])
        self.pop_flux[label] = []

    def shuffle(self):
        random.shuffle(self.population)

    def print_pop(self):
        for member in self.population:
            print(member.id)

    def is_mistake(self):
        if random.randint(1, 1000) > self.mistake_chance*1000:
            return True
        return False

    def set_play(self, method):
        self.play_type = method

    def assess(self):
        dists = {}
        for member in self.population:
            if member.label not in dists.keys():
                dists[member.label] = [member.score]
            elif member.label in dists.keys():
                dists[member.label].append(member.score)
        # print(dists)

        for key in self.pop_flux.keys():
            if key not in dists:
                dists[key] = []

        for label, dist in dists.items():
            self.pop_flux[label].append(len(dist))

    def evolve(self):
        scored_population = sorted(self.population, key=lambda x: x.score, reverse=True)
        scores = []
        for item in scored_population:
            scores.append(item.score)
        num_top = scores.count(np.max(scores))
        num_bottom = scores.count(np.min(scores))
        # print(num_top, num_bottom)
        top = scored_population[:self.num_replace]
        bottom = scored_population[-self.num_replace:]
        if num_top > self.num_replace:
            top = []
            top_selection = scored_population[:num_top-1]
            for i in range(self.num_replace):
                choice = random.choice(top_selection)
                top.append(choice)
                top_selection.remove(choice)

        if num_bottom > self.num_replace:
            bottom = []
            bottom_selection = scored_population[-num_bottom-1:]
            for i in range(self.num_replace):
                choice = random.choice(bottom_selection)
                bottom.append(choice)
                bottom_selection.remove(choice)

        for i in range(self.num_replace):
            self.population.remove(bottom[i])
            self.population.append(top[i])

        for member in self.population:
            # print(scored_population)  # is this introducing error? How are they sorted?
            # print(member.label, member.score)
            member.score_reset()

    def run_tournament(self, max_gen, show=True):
        for i in range(max_gen):
            # play.play_all_2(self)
            self.play_type(self)
            self.assess()
            self.evolve()
            self.gen += 1
        if show is True:
            self.output_data()

    def output_data(self):
        print("===Population Make-Up===")
        for type in self.types:
            print(f"{type[0]} initially makes up {type[2]*100}% of the population")
        # print(self.pop_flux)
        # gr.plot_population(list(range(self.gen)), self.pop_flux)
        gr.plot_double(list(range(self.gen)), self.pop_flux)
