import math
import sys
from functools import reduce
import os
import copy
import json

class node(object):
    def __init__(self, number, POI):
        '''
            number: int
            POI : dict
        '''
        self.number = number
        self.POI = POI
        self.count = sum(POI.values())
        self.entroy = self.entroy()

    def entroy(self):
        _entroy = sum([a * (math.log(self.count) - math.log(a))
                for a in self.POI.values()])
        return _entroy
    
class edge(object):
    def __init__(self, node1, node2, alpha):
        '''
            node1, node2 : node
        '''
        self.node1 = node1
        self.node2 = node2
        self.POI_sum  = self.combinePOI()
        #print(self.POI_sum)
        self.count = sum(self.POI_sum.values())
        self.entrSim = self.entroySimilarity()
        self.alpha = alpha
        self.structSim = self.structSimilarity()

    def combinePOI(self):
        poiSet = copy.deepcopy(self.node1.POI)
        for key2 in self.node2.POI:
            if key2 in self.node1.POI:
                poiSet[key2] += self.node2.POI[key2]
            else:
                poiSet[key2] = self.node2.POI[key2]
        return poiSet

    def entroySimilarity(self):
        _entroyEdge = sum([a * (math.log(self.count) - math.log(a))
                for a in self.POI_sum.values()])
        #print("_entroyEdge %f" %_entroyEdge)
        log_sim = self.node1.entroy + self.node2.entroy - _entroyEdge
        sim = math.exp(log_sim/self.count)
        return sim

    def structSimilarity(self):
            return self.alpha + (1-self.alpha) * self.entrSim

           

def calculateWeight(PoiPath, networkPath, alpha):
    with open(PoiPath, 'r') as fin:
        user_poi_count = json.load(fin)
    line = 1
    with open(networkPath,'r',encoding= 'utf-8') as rawFile:
        proPath = os.path.dirname(PoiPath) + '/weighted_network_'+str(alpha)+'.txt'
        with open(proPath, 'w', encoding = 'utf-8') as output:
            content = rawFile.readline().strip().split('\t')
            while len(content)==2:
                print("line: %d" %line)
                line += 1
                no_a, no_b = content
                if no_a not in user_poi_count or no_b not in user_poi_count:
                    content.append(alpha)
                else:
                    POIa = user_poi_count[no_a]
                    POIb = user_poi_count[no_b]
                    node_a = node(no_a, POIa)
                    node_b = node(no_b, POIb)
                    edge_ab = edge(node_a,node_b, alpha)
                    content.append(edge_ab.structSim)
                outStr = reduce(lambda x,y:str(x)+'\t'+str(y), content)
                print(outStr, file = output)
                content = rawFile.readline().strip().split('\t')


def main(alpha):
    PoiPath = "/home/leo/Documents/Thesis/user_poi_count.json"
    networkPath = "/home/leo/Documents/Thesis/unweight_network.txt"
    calculateWeight(PoiPath, networkPath, alpha)


if __name__ == "__main__":
    alpha = float(sys.argv[1])
    main(alpha)
#    POIa = {1:30, 2:4}
#    POIb = {1:20, 2:1}
#    no_a = 1
#    no_b = 2
#    node_a = node(no_a, POIa)
#    node_b = node(no_b, POIb)
#    edge_ab = edge(node_a,node_b, 0.8)
#    print(edge_ab.entrSim)
#    print(edge_ab.structSim)


        
