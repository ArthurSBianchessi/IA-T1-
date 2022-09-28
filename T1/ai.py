import random
import pandas as pd
import sys

num_coins = 0

def main():
    num_agents = int(sys.argv[1])
    grid, n = read_file()
    agents = gen_agents(n, num_agents)
    num_coins = n/2



    # for agent in agents:
    #     move(agent, grid, n)
    # evaluate(agents, n)
    # agents = reproduce(agents, n)
    # prt(agents[0])
    # for agent in agents:
    #     move(agent, grid, n)
    # prt(agents[0])





    for i in range(100):
        prt(agents[0])
        for agent in agents:
            move(agent, grid, n)
        prt(agents[0])
        evaluate(agents, n)
        # for agent in agents:
        #     prt(agent)
        agents = reproduce(agents, n)
        prt(agents[0])
    # print_best(agents[0], grid)


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
        self.coins_positions = []
        self.points = 0

    def copy(self):
        return Agent(self.moves)


def read_file():
    file = open("labirinto1.txt")
    n = int(file.readline())
    grid = []
    for line in file:
        grid.append(line.split())
    return [grid, n]


def gen_agents(n, num_agents):
    length = n**2
    agent_list = []
    for i in range(num_agents):
        list = []
        for i in range(length):
            while True:
                temp = [random.randrange(-1, 2, 1), random.randrange(-1, 2, 1)]
                if temp != [0,0]:
                    break
            list.append(temp)
        agent = Agent(list)
        agent_list.append(agent)
    return agent_list


def move(agent, grid, n):
    agent.num_moves = 0
    agent.coins_positions = []
    agent.coins = 0
    agent.posx = 0
    agent.posy = 0
    n2 = n**2
    while True:
        agent.posx += agent.moves[agent.num_moves][0]
        agent.posy += agent.moves[agent.num_moves][1]
        if 0 < agent.posx < n and 0 < agent.posy < n:
            if grid[agent.posy][agent.posx] == "C" and not [agent.posy, agent.posx] in agent.coins_positions:
                agent.coins += 1
                agent.coins_positions.append([agent.posy, agent.posx])
            elif grid[agent.posy][agent.posx] == "1":
                agent.posx -= agent.moves[agent.num_moves][0]
                agent.posy -= agent.moves[agent.num_moves][1]
                agent.moves.pop(agent.num_moves)
                agent.moves.append([random.randrange(-1, 2),
                                    random.randrange(-1, 2)])
                continue
        else:
            agent.posx -= agent.moves[agent.num_moves][0]
            agent.posy -= agent.moves[agent.num_moves][1]
            agent.moves.pop(agent.num_moves)
            agent.moves.append([random.randrange(-1, 2),
                                random.randrange(-1, 2)])
            continue

        if agent.num_moves >= n2 - 1 or agent.coins == n/2:
            break
        agent.num_moves += 1


def evaluate(agents, n):
    for agent in agents:
        agent.points = agent.coins * n + agent.posx + agent.posy
    agents.sort(key=lambda x: x.points, reverse=True)
    return agents


def reproduce(agents, n):
    new_agents = []
    new_agents.append(agents[0])

    length = int(len(agents[0].moves)/2)
    for i in range(1, len(agents), 2):
        a1 = champ(agents)
        a2 = champ(agents)
        new_agents.append(Agent(a1.moves[:length] + a2.moves[length:]))
        new_agents.append(Agent(a2.moves[:length] + a1.moves[length:]))

        # for j in range(int(len(agents)/2)):
        #     new_agents[i].moves[j]= agents[a1].moves[j]
        #     new_agents[i+1].moves[j]= agents[a2].moves[j]

        # for j in range(int(len(agents)/2),len(agents)):
        #     new_agents[i].moves[j]= agents[a2].moves[j]
        #     new_agents[i+1].moves[j]= agents[a1].moves[j]
    return agents


def champ(agents):
    a1 = agents[random.randrange(len(agents))].copy()
    a2 = agents[random.randrange(len(agents))].copy()
    if a1.points < a2.points:
        return a1
    else:
        return a2


if __name__ == "__main__":
    main()
