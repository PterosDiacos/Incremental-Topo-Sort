# DEFINE
FILE_PARAMETER = "c400-nr356.txt"
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

fout = open("out.edge.se.jump-" + FILE_PARAMETER, "w")

conjunction = []
count = 0 #debug
for line in matrix:
    line = str(line).split()
    wset = {i for i in range(vcount) if line[i] == "w"}
    lset = {i for i in range(vcount) if line[i] == "l"}
    for x in lset:
        conjunction.append([wset, x])
        if len(conjunction) == 1:
            topsort = sort(space, conjunction)
            count += 1 #debug
            fout.write(str(count)+ " - linear: " + str(topsort) + "\n\n") #debug
        else:
            precedents = [windex for windex in wset if topsort.index(windex) < topsort.index(x)]
            if len(precedents) == 0:
                xindex = topsort.index(x)
                rbound = xindex + 1
                while topsort[rbound] not in wset: rbound += 1
                
                prefrag = topsort[:xindex]
                updateFlag = 0
                while not updateFlag and rbound < len(topsort):
                    fragment = topsort[xindex:rbound + 1]
                    localConj = [[wset & set(fragment), x] for [wset, x] in conjunction
                                                           if x in fragment and len(wset & set(prefrag)) == 0]
                    fragmentsort = sort(set(fragment), localConj)
                    if len(fragmentsort) > 0:
                        topsort = prefrag + fragmentsort + topsort[rbound + 1:]
                        count += 1 #debug
                        fout.write(str(count)+ " - linear: " + str(topsort) + "\n\n") # debug
                        updateFlag = 1
                    else:
                        rbound += 1
                        while rbound < len(topsort) - 1  and  topsort[rbound] not in wset: rbound += 1

print("--- %s seconds ---" % (time.time() - start_time), file = fout)
fout.close()

#### ERROR CHECK
# for [wset, x] in conjunction:
#     forward = set(topsort[:topsort.index(x)])
#     if len(forward & wset) == 0:
#         print("Error @ ", [wset, x])
#         break
