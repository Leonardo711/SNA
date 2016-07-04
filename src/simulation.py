from __future__ import division
import math
from functools import reduce
import random
def entroy(dict_):
    sum_value = sum([dict_[key] for key in dict_])
    entroy = 0
    for key,value in dict_.items():
        value /= sum_value
        entroy -= value * math.log(value)
    return entroy

def sum_dict(dict_A, dict_B):
    for key_A in dict_A:
        if key_A in dict_B:
            dict_B[key_A] += dict_A[key_A] 
        else:
            dict_B[key_A] = dict_A[key_A]
    return dict_B


class entroySimilarity(object):
    def __init__(self, dict_A, dict_B):
        self.dict_A = dict_A
        self.dict_B = dict_B

   
    def similarity(self):
        '''
        dict_A/B   {poi:count}
        '''
        entroy_A = entroy(self.dict_A)
        entroy_B = entroy(self.dict_B)
        entroy_AB = entroy(sum_dict(self.dict_A, self.dict_B))
        return 2 * entroy_AB - entroy_A - entroy_B

def simulation():
    len_A =30 #random.randint(9,100)
    len_B =30 #random.randint(9,100)
    dict_A = {}
    dict_B = {}
    while len(dict_A)<len_A:
        a = random.randint(1,30)
        va = random.randint(1,31)
        if a not in dict_A:
           dict_A[a] = va
    
    while len(dict_B)<len_B:
        b = random.randint(1,30)
        vb = random.randint(1,31)
        if b not in dict_B:
           dict_B[b] = vb
    return dict_A, dict_B
     
def main():
    for i in range(1000000):
        print("simulation times:%d" %i)
        dict_A, dict_B = simulation()
        edge = entroySimilarity(dict_A, dict_B)
        value = edge.similarity()
        print("value: %f" %value)
        if value < 0:
            break

if __name__ == "__main__":
    main()



