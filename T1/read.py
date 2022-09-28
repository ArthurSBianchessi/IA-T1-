from random import random
from re import L
import pandas as pd

file = open("labirinto1.txt")
n = file.readline()
data=[]
for line in file:
    # print(line)

    # line.split(" ")
    # print(line[1])
    # line = [x for x in line if (x and x!="\n" and x!=" ")]
    data.append(line.split())

    # if line:
    #     data.append(line)

# print(data)
print(pd.DataFrame(data))
print(len(data))








def gen_list(length):
    list = []
    for i in range(length):
        list.append([random.choice([-1, 0, 1]), random.choice([-1, 0, 1])])
        