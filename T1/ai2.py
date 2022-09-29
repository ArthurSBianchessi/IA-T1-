from copy import deepcopy
import random
import pandas as pd
import sys


def main():
    num_agents = int(sys.argv[1])
    grid, n = read_file()
    grid = add_borders(grid, n)
    num_coins = int(n/2)
    movabel_spaces = count_movable_spaces(grid) + num_coins + 1
    agent_length = 4*(movabel_spaces)
    agents = gen_agents(agent_length, num_agents)

    best = 0
    print("{0:>5}".format("Gen"), "{0:>10}".format(
        "Points"), "{0:>5}".format("Coins"))
    gen = 1
    best_gen = 0
    best_agent = agents[0]
    while True:
        print("\r{0:>5}".format(gen), "{0:>10}".format(
                best_agent.posx), "{0:>5}".format(best_agent.posy), end="")
        move(agents, grid, agent_length, num_coins)
        agents, best_agent = evaluate(agents, n, movabel_spaces)
        if gen - best_gen < min(100, 0.5*best_gen):
            agents = mutate(agents, 100)
        else:
            agents = mutate(agents, 20)
        agents = reproduce(agents)

        if best_agent.points > best:
            best = best_agent.points
            print("\r{0:>5}".format(gen), "{0:>10}".format(
                best), "{0:>5}".format(best_agent.coins))
            best_gen = gen
        if best_agent.coins == num_coins:
            if gen > best_gen*1.1:
                break
        gen += 1

    best_agent = agent_path(best_agent)
    print_best(grid, best_agent)
    simplified_print(grid, best_agent)

def agent_path(agent):
    agent.posx = 1
    agent.posy = 1
    for i in range(agent.num_moves):
        agent.posx += agent.moves[i][0]
        agent.posy += agent.moves[i][1]
        agent.positions.append([agent.posy, agent.posx])
    return agent



def print_best(grid, best_agent):
        print("\n")
        grid2 = deepcopy(grid)
        for p in best_agent.positions:
            if grid2[p[0]][p[1]] == "C":
                grid2[p[0]][p[1]] = 0
            if grid2[p[0]][p[1]] == "0":
                grid2[p[0]][p[1]] = 0
            if isinstance(grid2[p[0]][p[1]], int):
                grid2[p[0]][p[1]] += 1
        dt = pd.DataFrame(grid2)
        dt = dt.replace(to_replace="1", value="\u2588")
        print(dt, end="\n\n\n")

def simplified_print(grid, best_agent):
        for p in best_agent.positions:
            if grid[p[0]][p[1]] == "C" or grid[p[0]][p[1]] == "2":
                grid[p[0]][p[1]] = "2"
            else:
                grid[p[0]][p[1]] = "3"

        for line in grid:
            for char in line:
                if char == "2":
                    print("\033[96m\u2588\033[0m", end="")
                elif char == "3":
                    print("\033[94m\u2588\033[0m", end="")
                elif char == "1":
                    print("\u2588", end="")
                elif char == "0":
                    print(" ", end="")
                else:
                    print(char, end="")
            print()


class Agent():
    def __init__(self, list):
        self.moves = list
        self.posx = 1
        self.posy = 1
        self.num_moves = 0
        self.coins = 0
        self.positions = []
        self.coins_positions = [(1,1)]
        self.points = 0
        self.distance = 0
        self.distances = 0
        self.repeats = 0


def read_file():
    file = open("labirinto1.txt")
    n = int(file.readline())
    grid = []
    for line in file:
        grid.append(line.split())
    return [grid, n]


def add_borders(grid, n):
    extra_line = []
    for i in range(n):
        extra_line.append("1")
    grid.append(extra_line.copy())
    grid.insert(0, extra_line.copy())
    for line in grid:
        line.append("1")
        line.insert(0, "1")
    return grid


def gen_agents(length, num_agents):
    agent_list = []
    for i in range(num_agents):
        list = []
        for i in range(length):
            while True:
                temp = [random.randrange(-1, 2, 1), random.randrange(-1, 2, 1)]
                if temp != [0, 0]:
                    break
            list.append(temp)
        agent = Agent(list)
        agent_list.append(agent)
    return agent_list


def move(agents, grid, agent_length, num_coins):
    for agent in agents:
        while agent.num_moves < agent_length and agent.coins < num_coins:
            agent.posx += agent.moves[agent.num_moves][0]
            agent.posy += agent.moves[agent.num_moves][1]
            if grid[agent.posy][agent.posx] == "C" and not (agent.posy, agent.posx) in agent.coins_positions:
                agent.coins_positions.append((agent.posy, agent.posx))
                agent.coins += 1
                agent.distances += agent.distance
                agent.distance = 0
                agent.positions = []
            elif grid[agent.posy][agent.posx] == "1":
                agent.posx -= agent.moves[agent.num_moves][0]
                agent.posy -= agent.moves[agent.num_moves][1]
                break

            # agent.repeats += agent.positions.count([agent.posy, agent.posx])
            if (agent.posy, agent.posx) not in agent.positions:
                agent.positions.append((agent.posy, agent.posx))
                agent.distance += 1

            agent.num_moves += 1


def evaluate(agents, n, movabel_spaces):
    multiplier = 3*n*(movabel_spaces+2)
    for agent in agents:
        agent.points = agent.coins*multiplier - agent.distances + n*agent.distance +abs(agent.posy - agent.coins_positions[-1][0])+abs(agent.posx - agent.coins_positions[-1][1])
        # + n*len(agent.distances)#- agent.repeats

    agents.sort(key=lambda x: x.points, reverse=True)
    return agents, agents[0]


def reproduce(agents):
    new_agents = []
    new_agents.append(Agent(agents[0].moves))
    if not len(agents) % 2:
        new_agents.append(Agent(agents[1].moves))

    for i in range(1, len(agents), 2):
        a1 = agents[min(random.randrange(0, len(agents)),
                        random.randrange(0, len(agents)))]
        a2 = agents[min(random.randrange(0, len(agents)),
                        random.randrange(0, len(agents)))]

        first_error = max(a1.num_moves, a2.num_moves)
        length = random.randrange(0, first_error+1)
        new_agents.append(
            Agent(a1.moves[:length] + a2.moves[length:]))
        new_agents.append(
            Agent(a2.moves[:length] + a1.moves[length:]))
    return new_agents


def count_movable_spaces(grid):
    counter = 0
    for line in grid:
        for element in line:
            if element == "1":
                counter += 1
    return counter


def mutate(agents, mutation_param):
    max_mutation = int(len(agents)/mutation_param)
    if max_mutation < 2:
        max_mutation = 2
    mutations = random.randrange(1, max_mutation)
    for i in range(mutations):
        agent_pos = random.randrange(1, int(len(agents)))
        if agents[agent_pos].num_moves == 0:
            chromossome = 0
        else:
            chromossome = random.randrange(0, agents[agent_pos].num_moves+2)
        while True:
            temp = [random.randrange(-1, 2, 1), random.randrange(-1, 2, 1)]
            if temp != [0, 0]:
                break
        agents[agent_pos].moves[chromossome] = temp
    return agents



if __name__ == "__main__":
    main()
