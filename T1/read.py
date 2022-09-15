import pandas as pd

file = open("T1/labirinto1.txt")
n = file.readline()
data=[]
for line in file:
    line.split()
    line = [x for x in line if (x and x!="\n" and x!=" ")]
    if line:
        data.append(line)

print(pd.DataFrame(data))
