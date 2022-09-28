import pandas as pd
file = open("labirinto1.txt")
n = int(file.readline())
data=[]
for line in file:
    data.append(line.split())

# print([1,2]+[2,1])
# print(data[1])
# print()
# print(pd.DataFrame(data))
df=pd.DataFrame(data)
df = df.replace(to_replace="1", value="\u2588")
df = df.replace(to_replace="0", value=" ")
# print(df[0])
# print(data[0])
# for line in data:
#     for char in line:
#         if char == "1":
#             print("\u2588", end="")
#         elif char == "0":
#             print(" ", end="")
#         else:
#             print(char, end="")
#     print()

# print(df)

df = df.replace(to_replace="\u2588", value="\u25A0")
df = df.replace(to_replace="0", value=" ")
print(df)
# print("\u25A0")

extra_line=[]
for i in range(n):
    extra_line.append("\u2588")

data.append(extra_line.copy())
data.insert(0, extra_line.copy())
for line in data:
    line.append("\u2588")
    line.insert(0, "\u2588")


for line in data:
    for char in line:
        if char == "1":
            print("\u2588", end="")
        elif char == "0":
            print(" ", end="")
        else:
            print(char, end="")
    print()


print("\033[94m\u2588\033[0m")