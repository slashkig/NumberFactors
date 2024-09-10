
from math import floor, sqrt

def print_factors(num):
    fNum = num
    factor = 2
    maxFactor = floor(sqrt(num));
    while factor <= maxFactor:
        if fNum % factor == 0:
            if fNum == factor: break
            print(factor, end=", ")
            fNum //= factor
        else:
            factor += 1
    print(fNum)


def test_combos(x, y, comboList):
    if x + y in comboList:
        formulas[x + y].append(f"{x}+{y}")
    else:
        comboList.append(x + y)
        formulas[x + y] = [f"{x}+{y}"]

    if x - y in comboList:
        formulas[x - y].append(f"{x}-{y}")
    else:
        comboList.append(x - y)
        formulas[x - y] = [f"{x}-{y}"]

    if x * y in comboList:
        formulas[x * y].append(f"{x}*{y}")
    else:
        comboList.append(x * y)
        formulas[x * y] = [f"{x}*{y}"]

    if x % y == 0:
        if x // y in comboList:
            formulas[x // y].append(f"{x}/{y}")
        else:
            comboList.append(x // y)
            formulas[x // y] = [f"{x}/{y}"]


def find_near_nums():
    min = target - numList[-3] - numList[-2]
    max = target * numList[0]
    nearList = []
    for num in comboList:
        if num < min: continue
        elif num >= max: break
        else: nearList.append(num)
    print_combos(nearList, True)


def print_combos(cList, show_factors=False):
    for num in cList:
        print(f"{num} = " + ", ".join(formulas[num]))
        if show_factors:
            print("   ", end="")
            print_factors(num)
    print()


def evaluate(math_str):
    ind = math_str.index(" ")
    result = int(math_str[:ind])
    while True:
        math_str = math_str[ind+1:]
        if math_str == "": break
        op = math_str[0]
        if math_str[2] == "(":
            ind = math_str.index(")")
            while math_str.count("(", 3, ind) != math_str.count(")", 3, ind):
                ind = math_str.index(")", ind + 1)
            num = evaluate(math_str[3:ind])
            ind += 1
        elif math_str.count(" ") == 1:
            num = int(math_str[2:])
            ind = len(math_str)
        else:
            ind = math_str.index(" ", 2)
            num = int(math_str[2:ind])

        if op == "+": result += num
        elif op == "-": result -= num
        elif op == "*": result *= num
        elif op == "/": result //= num

    return result

def aim_for(target):
    loopList = comboList.copy()
    print(f"{target}:")
    for i in range(len(comboList)):
        x = loopList.pop()
        for y in loopList:
            if x + y == target:
                print(f"{x}+{y}", end=", ")
            elif x - y == target:
                print(f"{x}-{y}", end=", ")
            elif x * y == target:
                print(f"{x}*{y}", end=", ")
            elif x // y == target and x % y == 0:
                print(f"{x}/{y}", end=", ")
    print("\b\b \n")


def try_calc(x, op, y):
    for comboX in formulas[x]:
        for comboY in formulas[y]:
            if op == "+": print(f"{comboX} + {comboY}")
            elif op == "-": print(f"{comboX} - {comboY}")
            elif op == "*": print(f"{comboX} * {comboY}")
            elif op == "/": print(f"{comboX} / {comboY}")
    print()


def setup():
    global numList, target
    numList = [int(input("Enter number: ")) for i in range(int(input("Count: ")))]
    target = int(input("Target: "))
    numList.append(target)
    numList.sort()

    print()
    for num in numList:
        print(num, end=" | ")
        print_factors(num)

    comboList.clear()
    formulas.clear()
    loopList = numList.copy()
    for i in range(len(numList)):
        x = loopList.pop()

        if x in comboList:
            formulas[x].append(f"{x}")
        else:
            comboList.append(x)
            formulas[x] = [f"{x}"]

        for y in loopList:
            test_combos(x, y, comboList)
    comboList.sort()
    print()
    
numList = list()
comboList = list()
formulas = dict()
command = str()
target = int()
setup()

while command != "exit":
    command = input("Enter command: ").lower()
    print()
    if command == "near": find_near_nums()
    elif command == "list": print_combos(comboList)
    elif command == "full": print_combos(comboList, True)
    elif command.startswith("factor"): num = int(command[7:]); print(num, end=" | "); print_factors(num)
    elif command.startswith("calc"): print(evaluate(command[5:]), end="\n\n")
    elif command.startswith("aim"): aim_for(int(command[4:]))
    elif command.startswith("try"):
        try: ind = command.index(" ", 4)
        except: continue
        try_calc(int(command[4:ind]), command[ind+1], int(command[ind+3:]))
    elif command == "help":
        print("near: Find numbers close to the target.")
        print("list: Show all stored combinations.")
        print("full: Show all combinations along with their factors.")
        print("factor <X>: Print factors of 'X'.")
        print("calc <expression>: Evaluate a simple mathematical expression.")
        print("aim <X>: Find combinations that result in 'X'.")
        print("try <X> <op> <Y>: Show all combinations of 'X' and 'Y' using operation 'op'.")
        print("reset: Resets the program.\n")
    elif command == "reset": setup()
