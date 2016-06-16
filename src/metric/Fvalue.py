# This is the F_value metric 
# to evaluate the clustering algorithm 
import functools

def precision(labelCluster, calCluster):
	'''
		the precision rate between 
		a labeled one and a calculated one
	'''
	len_inter = len(set(labelCluster) & set(calCluster))
	return len_inter/len(calCluster)

	
def recall(labelCluster, calCluster):
	'''
		the recall rate between
		a labeled one and a calculated one
	'''
	len_inter = len(set(labelCluster) & set(calCluster))
	return len_inter/len(labelCluster)

def F_value(labelCluster, calCluster):
	'''
		the F value between 
		a labeled one and a calculated one
	'''
	pre = precision(labelCluster, calCluster)
	re = recall(labelCluster, calCluster)
	f_value = 0
	if pre+re != 0:
		f_value = 2 * pre * re / (pre + re)
	return f_value

def F_one_cluster(ground_truth, calCluster):
	'''
		the F value for a calculated one
		compare with the ground truth
		
		ground_truth:two_dimensional list 
		calCluster: a list
	'''
	F_Pj = max([F_value(x, calCluster) for x in  ground_truth])
	return F_Pj 

def F_clusters(ground_truth, result):
	'''
		the F value for the whole result
		compare with the ground truth
		
		ground_truth:two_dimensional list 
		result: two_dimensional list 
	'''
	length_clusters = functools.reduce(lambda x,y: x + len(y), result, 0)
	f_clusters = sum([len(cluster)/length_clusters \
		* F_one_cluster(ground_truth, cluster) for cluster in result])
	return f_clusters




	#example case

#	a = [[1,2,3],[4,5,6],[7,8,9]]
#	b = [[2,3,4],[5,6,7],[1,8,9]]
#
#	m = F_clusters(b,a)
#	print(m)
