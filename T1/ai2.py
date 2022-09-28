from copy import deepcopy
import random
import pandas as pd
import sys


def main():
    num_agents = int(sys.argv[1])
    if num_agents%2==0:
        num_agents+=1
    grid, n = read_file()
    num_coins = int(n/2)
    agent_length = 4*(count_movable_spaces(grid) + num_coins + 1)
    agents = gen_agents(agent_length, num_agents)
    

    # for agent in agents:
    #     move(agent, grid, n)
    # evaluate(agents, n)
    # agents = reproduce(agents, n)
    # prt(agents[0])
    # for agent in agents:
    #     move(agent, grid, n)
    # prt(agents[0])
    best = 0
    print(n)
    print(count_movable_spaces(grid)+ num_coins + 1)
    print()
    for i in range(100):
        move(agents, grid, n, agent_length, num_coins)
        agents = evaluate(agents, n)

        # for agent in agents:
        #     print(agent.points)
        # print()

        # print(agents[0].points)
        # print(agents[1].points)
        # print(agents[2].points)
        # print()

        agents = mutate(agents, agent_length)
        agents = reproduce(agents)


        if best_agent.points > best:
            best = best_agent.points
            print(best, " ", best_agent.coins, i)

        # prt(agents[0])
    print("\n")
    print(best_agent.posx, best_agent.posy)
    print(best_agent.points)
    # print(pd.DataFrame(grid))
    print("\n")
    grid2 = deepcopy(grid)
    for p in best_agent.all_positions:
        if grid2[p[0]][p[1]] == "C":
            grid2[p[0]][p[1]] = 0
        if grid2[p[0]][p[1]] == "0":
            grid2[p[0]][p[1]] = 0
        grid2[p[0]][p[1]] += 1
    dt = pd.DataFrame(grid2)
    dt = dt.replace(to_replace="1", value="\u2588")
    print(dt)

    print("\n")
    for p in best_agent.all_positions:
        if grid[p[0]][p[1]] == "C" or grid[p[0]][p[1]] == "2":
            grid[p[0]][p[1]] = "2"
        else:
            grid[p[0]][p[1]] = "3"
    extra_line=[]
    data = grid
    for i in range(n):
        extra_line.append("\u2588")
    data.append(extra_line.copy())
    data.insert(0, extra_line.copy())
    for line in data:
        line.append("\u2588")
        line.insert(0, "\u2588")
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


def print_best(agent, grid):
    agent.posy = 0
    agent.posx = 0
    for move in agent.moves:
        agent.posx += move[0]
        agent.posy += move[1]
        # print(agent.posy, agent.posx)
        print(move)
        grid[agent.posy][agent.posx] = "\x1b[0;34;40m\u2588\x1b[0m"
    df = pd.DataFrame(grid)
    df = df.replace(to_replace="\u2588", value="\u25A0")
    df = df.replace(to_replace="0", value=" ")
    print(df)


def prt(a):
    print(a.posx, a.posy, a.coins, a.num_moves, a.points)


class Agent():
    def __init__(self, list):
        self.moves = list
        self.posx = 0
        self.posy = 0
        self.num_moves = 0
        self.coins = 0
        self.positions = []
        self.all_positions = []
        self.coin_positions = []
        self.points = 0
        self.distance = 0
        self.distances = []
        self.repeats = 0


def read_file():
    file = open("labirinto1.txt")
    n = int(file.readline())
    grid = []
    for line in file:
        grid.append(line.split())
    return [grid, n]


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


def move(agents, grid, n, agent_length, num_coins):
    for agent in agents:
        while True:
            agent.posx += agent.moves[agent.num_moves][0]
            agent.posy += agent.moves[agent.num_moves][1]
            if 0 <= agent.posx < n and 0 <= agent.posy < n:
                if grid[agent.posy][agent.posx] == "C" and not [agent.posy, agent.posx] in agent.coin_positions:
                    agent.coins += 1
                    agent.distances.append(agent.distance)
                    agent.distance = 0
                    agent.positions = []
                    agent.points = 0
                    agent.coin_positions.append([agent.posy, agent.posx])
                elif grid[agent.posy][agent.posx] == "1":
                    agent.posx -= agent.moves[agent.num_moves][0]
                    agent.posy -= agent.moves[agent.num_moves][1]
                    break
            else:
                agent.posx -= agent.moves[agent.num_moves][0]
                agent.posy -= agent.moves[agent.num_moves][1]
                break

            agent.repeats += agent.positions.count([agent.posy, agent.posx])
            agent.positions.append([agent.posy, agent.posx])
            agent.all_positions.append([agent.posy, agent.posx])

            if agent.num_moves >= agent_length - 1 or agent.coins == num_coins:
                break
            # if [agent.posy, agent.posx] in agent.positions:
            #     continue
            # else:
            #     agent.positions.append([agent.posy, agent.posx])
            agent.num_moves += 1
            agent.distance += 1


def evaluate(agents, n):
    for agent in agents:
        agent.points = agent.coins*n*n + agent.distance - sum(agent.distances) - agent.repeats
    agents.sort(key=lambda x: x.points, reverse=True)
    return agents


def reproduce(agents):
    new_agents = []
    new_agents.append(Agent(agents[0].moves))
    global best_agent
    best_agent = agents[0]

    for i in range(1, len(agents), 2):
        # a1 = agents[max(random.randrange(0, len(agents)),
        #          random.randrange(0, len(agents)))]
        # a2 = agents[max(random.randrange(0, len(agents)),
        #          random.randrange(0, len(agents)))]
        a1 = champ(agents)
        a2 = champ(agents)

        first_error = max(a1.num_moves, a2.num_moves)
        length = random.randrange(0, first_error+1)
        new_agents.append(
            Agent(a1.moves[:length] + a2.moves[length:]))
        new_agents.append(
            Agent(a2.moves[:length] + a1.moves[length:]))
    return new_agents

def champ(agents):
    a1 = agents[random.randrange(len(agents))]
    a2 = agents[random.randrange(len(agents))]
    if a1.points > a2.points:
        return a1
    else:
        return a2

def count_movable_spaces(grid):
    counter = 0
    for line in grid:
        for element in line:
            if element == "1":
                counter+=1
    return counter


def mutate(agents, agent_length):
    max_mutation = int(len(agents)/20)
    if max_mutation < 2:
        max_mutation = 2
    mutations = random.randrange(1, max_mutation)
    for i in range(mutations):
        agent_pos = random.randrange(1, int(len(agents)))
        if agents[agent_pos].num_moves == 0:
            chromossome = 0
        else:
            chromossome =   random.randrange(0, agents[agent_pos].num_moves+1)
        while True:
                temp = [random.randrange(-1, 2, 1), random.randrange(-1, 2, 1)]
                if temp != [0, 0]:
                    break
        agents[agent_pos].moves[chromossome] = temp
    return agents




if __name__ == "__main__":
    main()
