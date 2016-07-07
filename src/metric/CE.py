import math
import copy

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
        print(self.POI_sum)
        self.count = sum(self.POI_sum.values())
        self.entrSim = self.entroySimilarity()
		self.structSim = self.structSimilarity(alpha)

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
        print("_entroyEdge %f" %_entroyEdge)
        log_sim = self.node1.entroy + self.node2.entroy - _entroyEdge
        sim = math.exp(log_sim/self.count)
        return sim

    def structSimilarity(self):
            return alpha + (1-alpha) * self.entrSim
		
		

if __name__ == "__main__":
    POIa = {1:30, 2:4}
    POIb = {1:20, 2:1}
    no_a = 1
    no_b = 2
    node_a = node(no_a, POIa)
    node_b = node(no_b, POIb)
    edge_ab = edge(node_a,node_b)
    print(edge_ab.entrSim)


        
