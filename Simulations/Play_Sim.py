# ===2 Player Sims===
def play_all_2(pop):
    for i in range(pop.N-1):
        for player in pop.population[i+1:]:
            play_2(pop, pop.population[i], player)


def pair_random_2(pop):
    pop.shuffle()
    increment = pop.N//2
    n = 1
    while n < (increment):
        play_2(pop, pop.population[n], pop.population[n+increment])
        n += 1


def play_2(pop, player1, player2):
    player1.reset()
    player2.reset()
    for i in range(pop.num_rounds):
        result = []
        result.append(player1.eval())
        result.append(player2.eval())
        for i, choice in enumerate(result):
            if choice is True:
                result[i] = pop.is_mistake()
            # the below is for if you want chance to accidentally not cheat
            # else:
            #     choice = not self.is_mistake()
        player1.receive_2(result[1])
        player2.receive_2(result[0])
        match result:
            case [False, False]:
                reward = pop.reward_matrix[0]
                player1.update_score(reward[0])
                player2.update_score(reward[1])
            case [True, False]:
                reward = pop.reward_matrix[1]
                player1.update_score(reward[0])
                player2.update_score(reward[1])
            case [False, True]:
                reward = pop.reward_matrix[2]
                player1.update_score(reward[0])
                player2.update_score(reward[1])
            case [True, True]:
                reward = pop.reward_matrix[3]
                player1.update_score(reward[0])
                player2.update_score(reward[1])
            case _:
                raise Exception("Invalid Result")
        # print(player1.id, player1.label, player1.score)
        # print(player2.id, player2.label, player2.score)


# ===3 Player Sims===
# Each player plays every combo of other player
def play_every_combo_3(pop):
    for i in range(pop.N-1):
        for j, player2 in enumerate(pop.population[i+1:]):
            for player3 in pop.population[j+1:]:
                play_3(pop, pop.population[i], player2, player3)


def play_3(pop, player1, player2, player3):
    players = [player1, player2, player3]
    for player in players:
        player.reset()
    for i in range(pop.num_rounds):
        result = []
        for player in players:
            result.append(player.eval())
        for i, choice in enumerate(result):
            if choice is True:
                result[i] = pop.is_mistake()
            # the below is for if you want chance to accidentally not cheat
            # else:
            #     choice = not self.is_mistake()
        player1.receive_3(result[1], result[2])
        player2.receive_3(result[0], result[2])
        player3.receive_3(result[0], result[1])
        # print(result)
        match result.count(False):
            case 0:
                for player in players:
                    player.update_score(pop.reward_matrix[0][0])
            case 1:
                for i, player in enumerate(players):
                    if result[i] is True:
                        player.update_score(pop.reward_matrix[1][0])
                    else:
                        player.update_score(pop.reward_matrix[1][1])
            case 2:
                for i, player in enumerate(players):
                    if result[i] is True:
                        player.update_score(pop.reward_matrix[2][0])
                    else:
                        player.update_score(pop.reward_matrix[2][1])
            case 3:
                for player in players:
                    player.update_score(pop.reward_matrix[3][0])
            case _:
                raise Exception("Invalid Result")
