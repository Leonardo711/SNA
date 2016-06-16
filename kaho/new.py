from __future__ import division
import Graph
import time
from copy import deepcopy
import csv

def removeEdge(graph):
    for edge in graph.edges():
        u = edge[0]
        v = edge[1]
        if len(set(graph.neighbors(u)) & set(graph.neighbors(v))) < 1:
            #print edge
            #print len(set(GRAPH.neighbors(u)) & set(GRAPH.neighbors(v)))
            graph.Remove_edges((u,v))

def adjMatrix(GRAPH):
    matrix = {}
    for edge in GRAPH.edges():
        matrix[edge] = 1
    return matrix

def count_connectivity(graph):
    C = {}
    count = 0
    visited = {}
    nodes = graph.nodes()
    while nodes:
        node = nodes.pop()
        C[count]=[node]
        visited[node] = 1
        Q = graph.neighbors(node)
        while Q:
            u = Q.pop()
            C[count].append(u)
            visited[u] = 1
            nodes.remove(u)
            for v in graph.neighbors(u):
                if visited.get(v,0)==0 and v not in Q:
                    Q.append(v)
        count += 1
    return count,C

def clusteringCoefficient(node):
    #global max
    #global max_node
    neighbor = GRAPH.neighbors(node)
    k = len(neighbor)
    if k <= 1:
        coefficient = 0
    else:
        count = 0
        for i in range(k):
            for j in range(i+1,k):
                if mat.get((neighbor[i],neighbor[j]),0) == 1 or mat.get((neighbor[j],neighbor[i]),0) == 1:
            #if (tri_nodes[i]) in GRAPH.neighbors(tri_nodes[j]):
                    count += 1
        coefficient = 2 * count / (k * (k - 1))
    # if coefficient >= max:
    #     if coefficient == max:
    #         if len(GRAPH.neighbors(node)) > d:
    #             max = coefficient
    #             max_node = node
    #             d = GRAPH.neighbors(node)
    #     elif coefficient > max:
    #         max = coefficient
    #         max_node = node
    #         d = GRAPH.neighbors(node)
    return coefficient

def trans(S):
    #S[node,cc,dv]
    count = len(S)
    i = 0
    while count>0:
        if S[i][1] == 1 and S[i][2] <=2:
            temp = S[i]
            del S[i]
            S.append(temp)
        else:
            i += 1
        count -= 1
    return S

def InitialPartition(S):
    P = {}
    node_community = {}
    num = 0
    visited = {node:0 for node in GRAPH.nodes()}
    for i in range(len(S)):
        node = S[i][0]
        if visited[node] == 0:
            visited[node] = 1
            P[num] = [node]
            node_community[node] = num
            for u in GRAPH.neighbors(node):
                if visited[u] == 0:
                    P[num].append(u)
                    node_community[u] = num
                    visited[u] = 1
            num += 1
    return P,node_community

def t(x,C):
    neighbor = GRAPH.neighbors(x)
    count = 0
    tri_nodes = list(set(neighbor).intersection(set(C)))
    n = len(tri_nodes)
    for i in range(n):
        for j in range(i+1,n):
            #if mat.get((tri_nodes[i],tri_nodes[j]),0) == 1 or mat.get((tri_nodes[j],tri_nodes[i]),0) == 1:
            if GRAPH.graph[tri_nodes[i]].get(tri_nodes[j],0) == 1:
            #if (tri_nodes[i]) in GRAPH.neighbors(tri_nodes[j]):
                count += 1
    return count

def vt(x,C):
    neighbor = GRAPH.neighbors(x)
    count = 0
    c_neighbor = list(set(neighbor).intersection(set(C)))
    for node in c_neighbor:
        for v in neighbor:
            if GRAPH.graph[node].get(v,0) == 1 and v != node:
                count +=1
                break
    return count

def wcc(x,C):
    t_xV = t(x,V)
    if t_xV != 0:
        CvC = list((set(V)-set(C)))
        # result = t(x,C) * vt(x,V)/(t_xV * (len(C)-1+vt(x,CvC)))
        t1 = t(x,C)
        vt1 = vt(x,V)
        lenC = t_xV * (len(C)-1+vt(x,CvC))
        result = t1 * vt1 / lenC
    else:
        result = 0
    return result

def WCC(S):
    result = 0
    for pp in S:
        Spp = S[pp]
        for node in Spp:
            result += wcc(node,S[pp])
    result = result / count_node
    return result

def InitialPartition(S):
    P = {}
    node_community = {}
    num = 0
    visited = {node:0 for node in GRAPH.nodes()}
    for i in range(len(S)):
        node = S[i][0]
        if visited[node] == 0:
            visited[node] = 1
            P[num] = [node]
            node_community[node] = num
            for u in GRAPH.neighbors(node):
                if visited[u] == 0:
                    P[num].append(u)
                    node_community[u] = num
                    visited[u] = 1
            num += 1
    return P,node_community

def bestMovement(v,P):
    beta = 1
    #beta = 1.2
    global node_community
    m = ["NO_ACTION"]
    sourceC = node_community[v]
    C_remove_v = deepcopy(P[sourceC])
    C_remove_v.remove(v)
    wcc_r = -WCC_insert(v,C_remove_v)
    wcc_t = 0.0
    bestC = None
    candidates = []
    neighbor = GRAPH.neighbors(v)
    for node in neighbor:
        candidates.append(node_community[node])
    candidates = set(candidates)
    for c in candidates:
        n = len(P[sourceC])
        if n >1:
            aux = -WCC_insert(v,C_remove_v) + WCC_insert(v,P[c])
        else:
            aux = WCC_insert(v,P[c])
        if aux > wcc_t:
            wcc_t = aux
            bestC = c
        if wcc_r > beta * wcc_t and wcc_r >0.0:
            m = ["REMOVE"]
    if wcc_t > 0.0:
        if len(P[sourceC])>1:
            m = ["TRANSFER",bestC]
        else:
            m = ["INSERT",bestC]
    return m

def WCC_insert(v,C):

      # Cv = deepcopy(C)
      # Cv.append(v)
      Cv = []
      for c in C:
          Cv.append(c)
      wccI = 0
      for node in C:
          wccI += (wcc(node,Cv) - wcc(node,C))
      wccI = (wccI + wcc(v,Cv)) / count_node
     # wccI = WCC(Pv)-WCC(P)
      return wccI

def Refinement(P):
    global node_community
    goahead = 4
    triesRemaining = goahead
    check = False
    bestWCC=WCC(P)
    count = 1
    while triesRemaining>0:
        movement = {"NO_ACTION":0,"INSERT":0,"TRANSFER":0,"REMOVE":0}
        start = time.time()
        triesRemaining -= 1
        M = {}
        for node in V:
           M[node] = bestMovement(node,P)
        aa = 0
        for m in M:
        #     print(m,M[m])
            if M[m][0]=="NO_ACTION":
                aa += 1
            movement[M[m][0]] += 1

        # print ("there are %d NO_ACTION nodes" %aa)
        nM = len(M)
        if aa == nM:
            check = True
        if check:
            print ("the interation ends at %d" %(count))
            break

        for action in movement:
            print("%d %s nodes" %(movement[action],action))
        P = applyMovement(M,P)
        print("========================================================================================")
        print ("there are  %d communities" %len([i for i in P if len(P[i])>0]))
        print ("there are  %d singular communities" %len([i for i in P if len(P[i])==1]))
        print ("there are  %d large communities" %len([i for i in P if len(P[i])>6]))
        print("=========================================================")
        newWCC=WCC(P)
        end = time.time()
        print ("the WCC of interation %d is: %f" %(count,newWCC))
        print ("interation %d costs: %d s" %(count,end-start))
        print("=========================================================================================")
        if (newWCC-bestWCC)/newWCC >= 0.1:
            triesRemaining = goahead
            bestWCC = newWCC
            print("==============new tries=============")
        count += 1

    return P

def applyMovement(M,P):
    global pointer
    global node_community
    for node in M:
        if M[node][0] == "REMOVE":
             pointer += 1
             P[pointer] = [node]
             P[node_community[node]].remove(node)
             node_community[node] = pointer
        if M[node][0] == "INSERT":
            P[M[node][1]].append(node)
            P[node_community[node]].remove(node)
            node_community[node] = M[node][1]
        elif M[node][0] == "TRANSFER":
            P[M[node][1]].append(node)
            P[node_community[node]].remove(node)
            node_community[node] = M[node][1]
    return P

def print_com(P):
    community = {}
    for i in P:
        n = len(P[i])
        for j in range(n):
            community[P[i][j]] = i
    return community

def writecsv(P,PATH):
      csvfile = open(PATH,'wb')
      writer = csv.writer(csvfile,dialect='excel')
      for i in P:
          s = []
          n = len(P[i])
          if n >=1:
              for j in range(n):
                  s.append(label[P[i][j]])
              writer.writerow(s)

def combine(P,community):
    check1 = True
    while check1:
        count = 0
        for node in community:
            check2 = False
            neighbor = GRAPH.neighbors(node)
            neighbor_community = {}
            for v in neighbor:
                neighbor_community[community[v]] = neighbor_community.get(community[v],0) + 1
            max_c = community[node]
            for c in neighbor_community:
                if len(P[max_c]) < neighbor_community[c]:
                    max_c = c
                    check2 = True
            if check2:
                P[community[node]].remove(node)
                P[max_c].append(node)
                community[node] = max_c
                count += 1
        if count > 0:
            print("there are %d nodes transfer" %count)
        else:
            check1 = False
    return P,community

def writeCommunity(community,PATH):
    csvfile = open(PATH,'wb')
    writer = csv.writer(csvfile,dialect='excel')
    for node in community:
        writer.writerow([node,community[node]])

def overlapping(P,community,a):
    count = 0
    for node in community:
        check = False
        neighbor = GRAPH.neighbors(node)
        n = len(neighbor)
        if n >=3 :
            neighbor_community = {}
            for v in neighbor:
                neighbor_community[community[v]] = neighbor_community.get(community[v],0) + 1
            for c in neighbor_community:
                if c != community[node] and neighbor_community[c]/n >a and neighbor_community[c]>3:
                        P[c].append(node)
                        check = True
                        print node

        if check:
            count += 1

    print("there are %d overlapping nodes" %count)
    for key in P:
        P[key] = list(set(P[key]))
    return P

def construct(community):
    P = {}
    for node in community:
        P[community[node]] = P.get(community[node],[])
        P[community[node]].append(node)
    return P

def main():
    global P
    P = Refinement(P)
    # P,community = combine(partition,node_community)
    #P = overlapping(P,community,0.5)
    path = 'e:/data/result/kaho_test.csv'
    writecsv(P,path)
    # for i in range(1):
    #     WCC_insert(1,[1,2,3,4,66])
    # #     #WCC(P)
    # #     #wcc(1,[1,2,3,4,66])
    # # # test = [1,2,3,4,5,6,7,8,9,8,9,10]
    # # # for i in range (10000000):
    # # #     #te = deepcopy(test)   17
    # # #     s = []
    # # #     for j in test:
    # # #         s.append(j)



if __name__ == '__main__':
    path1 = 'e:/data/kaho.csv'
    path2 = 'e:/data/nodes_kaho.csv'
    GRAPH = Graph.readedgelist(path1)
    print('===read graph completed!===')
    label = {}
    file=open(path2,'rb')
    reader = csv.reader(file)
    for row in reader:
       label[int(row[0])] = row[1]
    GRAPH.Remove_node(0)
    removeEdge(GRAPH)
    mat = adjMatrix(GRAPH)
    print('===remove edges completed!===')
    connectivity,CCC= count_connectivity(GRAPH)
    for i in range(len(CCC)):
        if len(CCC[i])==1:
            GRAPH.Remove_node(CCC[i][0])
            del CCC[i]
    V = GRAPH.nodes()
    count_node = len(V)
    print count_node
    print('===calculation begin!===')
    tstart = time.time()
    S = []
    for node in GRAPH.nodes():
        S.append((node,clusteringCoefficient(node),len(GRAPH.neighbors(node))))
    S.sort(key = lambda s:(s[1],s[2]),reverse = True)
    S=trans(S)
    P,node_community = InitialPartition(S)
    pointer = max(P.keys())
    nncount=0
    main()
    tend = time.time()
    t = tend - tstart
    print('===calculation completed!=== %d seconds!' %t)