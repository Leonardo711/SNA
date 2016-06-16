# This is the entroy metric 
# to evaluate the clustering algorithm 
import math
from Fvalue import precision
from functools import reduce

def log(value):
	result = math.log(value) if value else 0
	return result

def entropy_one_cluster(ground_truth, calCluster):
	'''
		entropy value for a calculated one 
		compare with the ground truth
		
		ground_truth:two_dimensional list 
		calCluster: a list
	'''
	x = log(len(ground_truth))
	entro = reduce(lambda x,y:x - precision(y, calCluster) \
		*log(precision(y, calCluster)), ground_truth, 0)
	return entro

def entropy(ground_truth, result):
	'''
		entropy value for the whole result
		compare with the ground truth
		
		ground_truth:two_dimensional list 
		calCluster: a list
	'''
	length_clusters = reduce(lambda x,y: x + len(y), result, 0)
	entropy_value = sum([len(cluster)/length_clusters \
		* entropy_one_cluster(ground_truth, cluster) for cluster in result])
	return entropy_value

a = [[1,2,3],[4,5,6],[7,8,9]]
b = [[2,3,4,10],[5,6,7,11],[1,8,9,12]]

m = entropy(a,b)
print(m)
