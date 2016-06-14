#encoding = gbk
import pandas as pd
from functools import reduce

def createLbsDict(path):
	with open(path, 'r', encoding="utf-8") as lbs:
		header = lbs.readline().strip().split(",")
		content = lbs.readline().strip().split(",")
		print(content)
		while len(content)>=3:
			date = content[0]
			usr = content[1]
			poi = content[2]
			if usr in LbsDict:
				pois = LbsDict[usr]
				if poi in pois:
					LbsDict[usr][poi] += 1
				else:
					LbsDict[usr][poi]=1
			else:
				LbsDict[usr] = {poi:1}
			content = lbs.readline().strip().split(",")
	print(LbsDict['0'])
	print("Create LbsDict Done!")

# simularity metrics : sim_co
def sim_co(RelationPath, outPath):
	with open(RelationPath, "r", encoding= "utf-8") as Rela:
		with open(outPath, "w", encoding= "utf-8") as out:
			header = Rela.readline()
			content = Rela.readline().strip().split(",")
			while len(content)>=3:
				user1 = content[0]
				user2 = content[1]
				sum_max = 0
				if (user1 in LbsDict) and (user2 in LbsDict):
					co_poi = list(set(LbsDict[user1].keys() | set(LbsDict[user2].keys())))
					sum_min = sum([min(LbsDict[user1].get(poi,0),LbsDict[user2].get(poi,0)) for poi in co_poi])
					content[2] = round(sum_min/len(co_poi), 2)
				else:
					content[2] = 0
				outStr = reduce(lambda x,y : str(x)+","+str(y), content[0:3])
				print(outStr, file=out)
				content = Rela.readline().strip().split(",")

		

def main():
	LbsPath = "../Data/result/proLBS_daily.csv"
	RelationPath = "../Data/result/proRelation.csv"
	# outPath = "../Data/result/newWeighted.csv"
	sim_co_Path = "../Data/result/sim_co.csv"
	createLbsDict(LbsPath)
	sim_co(RelationPath,sim_co_Path)

if __name__ == "__main__":
	LbsDict = {}
	main()
