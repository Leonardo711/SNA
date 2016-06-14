import os
from functools import reduce

class LBSandRelation(object):
	def __init__(self, LbsPath, relationPath):
		'''
			globalDict match md5 id to a small number
		'''
		self.LbsPath = LbsPath
		self.relationPath = relationPath
		self.globalDict = {}
	
#	def processFile(path, para):
#		with open(path, 'r', encoding='mbcs') as rawFile:
#			header = rawFile.readline().strip()
#			tmpPath = os.path.dirname(path) + "/tmp" + para + ".csv"
#			with open(tmpPath,'w+',encoding = 'utf-8') as tmp:
#				while header:
#					print(header, file = tmp)
#					header = rawFile.readline().strip()
#		return tmpPath


	def processRelation(self):
		with open(self.relationPath,'r',encoding = 'utf-8') as rawFile:
			print(self.relationPath)
			header = rawFile.readline().strip()
			proPath = os.path.dirname(self.relationPath) + '/proRelation.csv'
			with open(proPath, 'w', encoding = 'utf-8') as output:
				print(header,file = output)
				content = rawFile.readline().strip().split(',')
				id = -1
				while len(content)>=2:
					if content[0] in self.globalDict:
						content[0] = self.globalDict[content[0]]
						if content[1] in self.globalDict:
							content[1] = self.globalDict[content[1]]
						else:
							id += 1
							self.globalDict[content[1]] = id
							content[1] = id
					else:
						id += 1
						self.globalDict[content[0]] = id
						content[0] = id
						if content[1] in self.globalDict:
							content[1] = self.globalDict[content[1]]
						else:
							id += 1
							self.globalDict[content[1]] = id
							content[1] = id
					outStr = reduce(lambda x,y:str(x)+','+str(y), content)
					print(outStr, file = output)
					content = rawFile.readline().strip().split(',')

	def processLBS(self, column):
		columnDict = {}
		with open(self.LbsPath,'r',encoding= 'utf-8') as rawFile:
			print(self.LbsPath)
			header = rawFile.readline().strip().split(',')
			string = header[column]
			proPath = os.path.dirname(self.LbsPath) + '/proData/' + '/proLBS_'+str(string).upper()+'.csv'
			with open(proPath, 'w', encoding = 'utf-8') as output:
				print(header, file = output)
				content = rawFile.readline().strip().split(',')
				columnId = -1
				while len(content)>column:
					if content[1] not in self.globalDict:
						content[1] = 'unknown'
					else:
						content[1] = self.globalDict[content[1]]
					if content[column] in columnDict:
						content[2] = columnDict[content[column]]
					else:
						columnId += 1
						columnDict[content[2]] = columnId
						content[2] = columnId
					outStr = reduce(lambda x,y:str(x)+','+str(y), content[0:3])
					print(outStr, file = output)
					content = rawFile.readline().strip().split(',')

	def UniqueDailyRoute(self, column):
		poiDict = {}
		dailyRoute = {} 
		slice_list = [0,1,2,7]
		with open(self.LbsPath,'r',encoding= 'utf-8') as rawFile:
			print(self.LbsPath)
			header = rawFile.readline().strip().split(',')
			proPath = os.path.dirname(self.LbsPath) + '/proLBS_daily.csv'
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

