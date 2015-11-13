#Print latex table row
def printBelief(i, b):
    print "{} & {} & {} & {} & {} \\\\".format(i, b["A"], b["B"], b["C"], b["D"])
#Initial distribution
def initProb(x):
    if x == "A":
        return 1.0
    return 0.0
#Pr(E_i = e | X_i = x)
def E_cond_X(e, x):
    if e == x:
        return 0.5
    if (e == "A" and x == "D") or (e == "D" and x == "A") or \
       (e == "B" and x == "C") or (e == "C" and x == "B"):
           return 0.0
    return 0.25
    
#Pr(X_i = x | X_i-1 = x_1)
def X_cond_X_1(x, x_1):
    if x_1 == "A":
        if x == "A":
            return 0.5
        if x == "B":
            return 0.5
        if x == "C":
            return 0.0
        if x == "D":
            return 0.0
    if x_1 == "B":
        if x == "A":
            return 0.0
        if x == "B":
            return 0.5
        if x == "C":
            return 0.5
        if x == "D":
            return 0.0
    if x_1 == "C":
        if x == "A":
            return 0.5
        if x == "B":
            return 0.0
        if x == "C":
            return 0.0
        if x == "D":
            return 0.5
    if x_1 == "D":
        if x == "A":
            return 0.25
        if x == "B":
            return 0.25
        if x == "C":
            return 0.25
        if x == "D":
            return 0.25

#Normalize beliefs
def normalize(b):
    total = sum(b.values())
    for k in b:
        b[k] /= total

if __name__ == '__main__':
    states = ["A", "B", "C", "D"]
    E = ["A", "B", "B", "C", "D"]
    b = {}
    for x in states:
        b[x] = initProb(x)*E_cond_X(E[0], x)
    normalize(b)
    printBelief(1, b)
    for i in range(1, len(E)):
        temp = {}
        for x in states:
            temp[x] = 0.0
            for x_1 in states:
                temp[x] += E_cond_X(E[i], x)*X_cond_X_1(x, x_1)*b[x_1]
        normalize(temp)
        b = temp
        printBelief(i+1, b)