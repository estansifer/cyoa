import sys

def disp(a):
    print("")
    n = len(a)
    for i in range(0, n):
        print ("    " + (a[n - i - 1] * '#'))
    print("")

def valid_move(a, b):
    bite = None
    n = len(a)
    for i in range(0, n):
        if a[i] < b[i]:
            return False
        if a[i] > b[i]:
            if (bite is None) or (bite == b[i]):
                bite = b[i]
            else:
                return False
    return not (bite is None)

def next(a, k):
    n = len(a)
    i = n - 1
    while a[i] == k:
        i -= 1
    a[i] += 1
    for j in range(i + 1, n):
        a[j] = a[i]

def compute_losers(n, k):
    losers = []
    a = n * [0]

    while a[0] < k:
        next(a, k)
        if choose_move(a, losers) is None:
            losers.append(a[:])

    return losers

def choose_move(a, losers):
    for loser in losers:
        if valid_move(a, loser):
            return loser
    return None

def display_losers(n, k):
    losers = compute_losers(n, k)
    for loser in losers:
        disp(loser)
        print ("")

def play(n, k):
    losers = compute_losers(n, k)

    a = n * [k]
    history = []

    while a[n - 1] > 0:
        a = choose_move(a, losers)[:]
        history.append(a[:])
        disp(a)

        row = 0
        col = 0
        while True:
            try:
                line = input("$ ")
            except:
                return
            if len(line) == 0:
                continue
            elif line[0] == 'h':
                print ("  Type the row and the column of the chocolate piece")
                print ("  you want to consume, e.g. \"3 2\" or \"7 10\".")
                print ("  Whoever eats the upper-left piece loses.")
                print ("  Other commands are 'quit', 'undo', and 'refresh'.")
            elif line[0] == 'r':
                disp(a)
            elif line[0] == 'u' or line[0] == 'b':
                if len(history) > 1:
                    history.pop()
                    a = history[-1][:]
                    disp(a)
            elif line[0] == 'q' or line[0] == 'e':
                return
            else:
                try:
                    row, col = line.split()
                    row = int(row)
                    col = int(col)

                    if row >= 1 and row <= n and col >= 1 and col <= k:
                        flag = False
                        for i in range(0, n - row + 1):
                            if a[i] >= col:
                                flag = True
                                a[i] = col - 1
                        if flag:
                            break
                        else:
                            print ("  That chocolate piece was already eaten.")
                    else:
                        print ("  There is no such piece.")
                except:
                    print ("  Did not understand command.")

    print ("I win!")

if len(sys.argv) == 3:
    play(int(sys.argv[1]), int(sys.argv[2]))
else:
    print("Usage:")
    print("  python chocolate.py <rows> <columns>")
    print("Use small numbers, e.g., 5 rows and 8 columns.")
