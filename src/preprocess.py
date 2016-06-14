# -*- coding=utf-8 -*-
import os
from functools import reduce

def processLBS(path):
	poiDict = {}
	with open(path,'r',encoding= 'utf-8') as rawFile:
		print(path)
		header = rawFile.readline().strip()
		proPath = os.path.dirname(path) + '/proLBS_POIwithoutDate.csv'
		with open(proPath, 'w', encoding = 'utf-8') as output:
			print(header, file = output)
			content = rawFile.readline().strip().split(',')
			poiId = -1
			while len(content)>=3:
				if content[1] not in globalDict:
					content[1] = 'unknown'
				else:
					content[1] = globalDict[content[1]]
				if content[2] in poiDict:
					content[2] = poiDict[content[2]]
				else:
					poiId += 1
					poiDict[content[2]] = poiId
					content[2] = poiId
				outStr = reduce(lambda x,y:str(x)+','+str(y), content[1:3])
				print(outStr, file = output)
				content = rawFile.readline().strip().split(',')

def UniqueDailyRoute(path):
	poiDict = {}
	dailyRoute = {} 
	slice_list = [0,1,2,10]
	with open(path,'r',encoding= 'utf-8') as rawFile:
		print(path)
		header = rawFile.readline().strip().split(',')
		proPath = os.path.dirname(path) + '/proLBSwithRegion_daily.csv'
		with open(proPath, 'w', encoding = 'utf-8') as output:
			header = [header[i] for i in slice_list]
			outheader = reduce(lambda x,y :str(x) +','+str(y), header)
			print(outheader, file = output)
			content = rawFile.readline().strip().split(',')
			poiId = -1
			while len(content)>=3:
				if content[1] not in globalDict:
					content[1] = 'unknown'
				else:
					content[1] = globalDict[content[1]]
				if content[2] in poiDict:
					content[2] = poiDict[content[2]]
				else:
					poiId += 1
					poiDict[content[2]] = poiId
					content[2] = poiId
				if content[0] in dailyRoute:
					person_poi = dailyRoute[content[0]]
					if content[1] in person_poi:
						poi = person_poi[content[1]]
						if content[2] in poi:
							content = rawFile.readline().strip().split(',')
							continue
					else:
						dailyRoute[content[0]][content[1]]=[] 
				else:
					dailyRoute[content[0]] = {content[1]:[]} 
				dailyRoute[content[0]][content[1]].append(content[2])
				outStr = reduce(lambda x,y:str(x)+','+str(y), [content[i] for i in slice_list])
				print(outStr, file = output)
				content = rawFile.readline().strip().split(',')

def processKahoLBS(path):
	poiDict = {}
	with open(path,'r',encoding= 'utf-8') as rawFile:
		print(path)
		header = rawFile.readline().strip()
		proPath = os.path.dirname(path) + '/proLBS_kaho.csv'
		with open(proPath, 'w', encoding = 'utf-8') as output:
			print(header, file = output)
			content = rawFile.readline().strip().split(',')
			poiId = -1
			while len(content)>=3:
				if globalDict[content[1]]==0:
					content[1] = globalDict[content[1]]
					if content[2] in poiDict:
						content[2] = poiDict[content[2]]
					else:
						poiId += 1
						poiDict[content[2]] = poiId
						content[2] = poiId
					outStr = reduce(lambda x,y:str(x)+','+str(y), content)
					print(outStr, file = output)
				content = rawFile.readline().strip().split(',')

def processLeoLBS(path):
	poiDict = {}
	with open(path,'r',encoding= 'utf-8') as rawFile:
		print(path)
		header = rawFile.readline().strip()
		proPath = os.path.dirname(path) + '/proLBS_Leo.csv'
		with open(proPath, 'w', encoding = 'utf-8') as output:
			print(header, file = output)
			content = rawFile.readline().strip().split(',')
			poiId = -1
			while len(content)>=3:
				if globalDict[content[1]]==7:
					content[1] = globalDict[content[1]]
					if content[2] in poiDict:
						content[2] = poiDict[content[2]]
					else:
						poiId += 1
						poiDict[content[2]] = poiId
						content[2] = poiId
					outStr = reduce(lambda x,y:str(x)+','+str(y), content)
					print(outStr, file = output)
				content = rawFile.readline().strip().split(',')

def processFile(path, para):
	with open(path, 'r', encoding='mbcs') as rawFile:
		header = rawFile.readline().strip()
		tmpPath = os.path.dirname(path) + "/tmp" + para + ".csv"
		with open(tmpPath,'w+',encoding = 'utf-8') as tmp:
			while header:
				print(header, file = tmp)
				header = rawFile.readline().strip()
	return tmpPath

def processRelation(path):
	with open(path,'r',encoding = 'utf-8') as rawFile:
		print(path)
		header = rawFile.readline().strip()
		proPath = os.path.dirname(path) + '/proRelation.csv'
		with open(proPath, 'w', encoding = 'utf-8') as output:
			print(header,file = output)
			content = rawFile.readline().strip().split(',')
			id = -1
			while len(content)>=2:
				if content[0] in globalDict:
					content[0] = globalDict[content[0]]
					if content[1] in globalDict:
						content[1] = globalDict[content[1]]
					else:
						id += 1
						globalDict[content[1]] = id
						content[1] = id
				else:
					id += 1
					globalDict[content[0]] = id
					content[0] = id
					if content[1] in globalDict:
						content[1] = globalDict[content[1]]
					else:
						id += 1
						globalDict[content[1]] = id
						content[1] = id
				outStr = reduce(lambda x,y:str(x)+','+str(y), content)
				print(outStr, file = output)
				content = rawFile.readline().strip().split(',')

def main():
	LbsPath = "E:/Python/SNA/LBS/Data/tmpLbs.csv"
	relationPath = "E:/Python/SNA/LBS/Data/relation_sample.csv"
	tmpRelation = processFile(relationPath, 'Relation')
	processRelation(tmpRelation)
	#tmpLbs = processFile(LbsPath,'Lbs')
#	processLeoLBS(LbsPath)
#	processKahoLBS(LbsPath)
	UniqueDailyRoute(LbsPath)

if __name__ == "__main__":
	globalDict = {}
	main()
