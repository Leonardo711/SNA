import os
from __future__ import division
from functools import reduce
from math import sqrt
import datetime
import pickle
import math



def splitLbs(LbsPath, splitOutPath):
        with open(LbsPath, 'r', encoding="utf-8") as LBS:
                header = LBS.readline()
                content = LBS.readline().strip().split(",")
                while len(content)>=3:
                        date = content[0]
                        usr = content[1]
                        poi = content[2]
                        outPath = splitOutPath + content[0] +".csv"
                        with open(outPath, 'a',encoding="utf-8") as outFile:
                                outStr = reduce(lambda x,y:str(x)+","+str(y), content)
                                print(outStr,file=outFile)
                        content = LBS.readline().strip().split(",")

def buildLbsDict(path, LbsDictPath):
        '''
         construct the dict for daily LBS information of everyone
         {date:{usr:{poi:count}}}
        '''
        print("Building Lbs Dict...")
        with open(path,'r',encoding= 'utf-8') as rawFile:
                line = 0
                header = rawFile.readline().strip().split(',')
                content = rawFile.readline().strip().split(',')
                while len(content)>=3:
                        line+= 1
                        print("processing line:%d" %line)
                        date = content[0]
                        usr = content[1]
                        poi = content[2]
                        usr_poi = LbsDict.setdefault(date,{})
                        pois = usr_poi.setdefault(usr,{})
                        count = pois.setdefault(poi,0)
                        LbsDict[date][usr][poi] += 1
                        content = rawFile.readline().strip().split(',')
        print("Done build LbsDict")
        print("Start pickling")
#       with open(LbsDictPath, 'wb') as lbsdict:
#               pickle.dump(LbsDict, lbsdict)
#               print("Done with pickling")
                

def cal_simSet_cos(usr1, usr2):
        '''
        calculate similarity of a relation for 31 days (method: cos)
        return a list contain 31 numbers
        '''
        sim_set = []
        for date in LbsDict.keys():
                usrs_pois = LbsDict[date]
                sim = 0
                if (usr1 in usrs_pois) and (usr2 in usrs_pois):
                        co_poi = list(set(usrs_pois[usr1]) & set(usrs_pois[usr2]))
                        sqrt_usr1 = sqrt(sum([count**2 for count in usrs_pois[usr1].values()]))
                        sqrt_usr2 = sqrt(sum([count**2 for count in usrs_pois[usr2].values()]))
                        coeff = sum([usrs_pois[usr1][poi] * usrs_pois[usr2][poi] for poi in co_poi])
                        sim = coeff/(sqrt_usr1 * sqrt_usr2)
                sim_set.append(sim)
        return sim_set

def DayWeight(dateSet):
        weight=[]
        for day in dateSet:
                date_time = datetime.datetime.strptime(day,'%Y%m%d')
                if date_time.weekday() < 5:
                        weight.append(0.08)
                else:
                        weight.append(0.3)
                sumation = sum(weight)
        weight_set = [ele/sumation for ele in weight]
        print("Done with day weight calculation")
        return weight_set

def cal_sim(sim_set, weight_set):
        if len(sim_set)!= len(weight_set):
                print("Your sim_set and weight_set is wrong")
                print("sim_set length :%d, weight_set length:%d " %(len(sim_set), len(weight_set)))
        simu = math.e ** sum([sim_set[i] * weight_set[i] for i in range(len(sim_set))])
        return simu

def weightedConstr(RelationPath, outPath):
        print("length of LbsDict.keys(): %d" %(len(list(LbsDict.keys()))))
        weight_set = DayWeight(list(LbsDict.keys()))
        print("Constructing weighted network...")
        with open(RelationPath, "r", encoding= "utf-8") as Rela:
                with open(outPath, "w", encoding= "utf-8") as out:
                        header = Rela.readline()
                        content = Rela.readline().strip().split(",")
                        while len(content)>=3:
                                usr1 = content[0]
                                usr2 = content[1]
                                sim_set = cal_simSet_cos(usr1, usr2)
                                simu = cal_sim(sim_set, weight_set)
                                content[2] = simu
                                outStr = reduce(lambda x,y : str(x)+","+str(y), content[0:3])
                                print(outStr, file=out)
                                content = Rela.readline().strip().split(",")
        print("Done with constructing")

def sum_dict(dict_A, dict_B):
    for key_A in dict_A:
        if key_A in dict_B:
            dict_B[key_A] += dict_A[key_A] 
        else:
            dict_B[key_A] = dict_A[key_A]
    return dict_B

def entroy(dict_):
    sum_value = reduce(lambda x,y: x+y ,[value for _,value in dict_.items()])
    entroy = 0
    for _,value in dict_.items():
        value /= sum_value
        entroy -= value * math.log(value)
    return entroy
        
        

            
class entroySimilarity(object):
    def __init__(self, usra, usrb):
        self.usra = usra
        self.usrb = usrb

    def dailySimilarity(self, date):
        pattern_a = LbsDict[date].get(self.usra,0)
        pattern_b = LbsDict[date].get(self.usrb,0)
        return self.similarity(pattern_a,pattern_b)
    
    def similarity(self, dict_a, dict_b):
        '''
        dict_a/b   {poi:count}
        '''
        entroy_A = entroy(dict_a)
        entroy_B = entroy(dict_b)
        entroy_AB = entroy(sum_dict(dict_a, dict_b))
        return 2 * entroy_AB - entroy_A - entroy_B
   def similarity(self):
        sim_set = []
        for date in LbsDict:
            sim_set.append(self.dailySimilarity(self.usra, self.usrb, date))
        return sim_set

           


        
def main():
        LbsPath = "../Data/result/proLBS_daily.csv"
        RelationPath = "../Data/result/proRelation.csv"
        outPath = "../Data/result/dailyWeighted/sim_cos_E.csv"
        LbsDictPath = "../Data/result/dailyWeighted/LbsDict.txt"
#       splitOutPath = "../Data/result/daily/"
#       splitLbs(LbsPath,splitOutPath)
        buildLbsDict(LbsPath, LbsDictPath)
        weightedConstr(RelationPath, outPath)


if __name__ == "__main__":
        LbsDict = {}
        main()

