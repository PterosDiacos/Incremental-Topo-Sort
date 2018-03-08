# DEFINE
FILE_PARAMETER = "c80-nr134.txt"
KILLTIME = 600
import time, sys
if len(sys.argv) > 1: FILE_PARAMETER = sys.argv[1]
start_time = time.time()

# read an M*N matrix, N constraints
fin = open(FILE_PARAMETER, "r")
matrix = fin.readlines()
fin.close()

vcount = len(str(matrix[0])) // 2   # linebreak included
space = {i for i in range(vcount)}


def sort(space, conjunction):
    nonzeroin = {x for [wset, x] in conjunction}
    zeroin = space - nonzeroin
    topsort = []
    #Kahn's algorithm
    while len(zeroin) > 0:
        topsort.append(zeroin.pop())
        conjunction = [[wset, x] for [wset, x] in conjunction
                                 if topsort[-1] not in wset]
        nonzeroin = {x for [wset, x] in conjunction}
        space = space - {topsort[-1]}
        zeroin = space - nonzeroin

    if len(nonzeroin) == 0: return topsort
    else: return []

fout = open("out.edge.un-" + FILE_PARAMETER, "w")

conjunction = []
count = 0 #debug
linecount = 0 #debug
for line in matrix:
    linecount += 1
    line = str(line).split()
    wset = {i for i in range(vcount) if line[i] == "w"}
    lset = {i for i in range(vcount) if line[i] == "l"}
    for x in lset:
        conjunction.append([wset, x])
        if len(conjunction) == 1:
            topsort = sort(space, conjunction)
            count += 1 #debug
            fout.write(str(count) + " - linear: " + str(topsort) + "\n\n") #debug
        else:
            precedents = [windex for windex in wset if topsort.index(windex) < topsort.index(x)]
            if len(precedents) == 0:
                topsort = sort(space, conjunction)
                count += 1 #debug
                fout.write(str(count) + " - linear: " + str(topsort) + "\n\n") #debug
    # When running over time        
    if time.time() - start_time > KILLTIME:
        estimatedTime = (time.time() - start_time) * len(matrix) / linecount
        print("--- %s seconds estimated ---" % estimatedTime, file = fout)
        fout.close()
        exit()

print("--- %s seconds ---" % (time.time() - start_time), file = fout)
fout.close()
