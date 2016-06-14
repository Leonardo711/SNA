import networkx as nx
from math import sqrt 
import sys
import copy
import time

# function to calculate the similarity between neighbor vertex
#def struct_similarity(u,v):
#	 d_u = GRAPH.degree(u) + 1
#	 d_v = GRAPH.degree(v) + 1
#	 total_neighbor = set(GRAPH.neighbors(u)+GRAPH.neighbors(v))
#	 common = d_u + d_v - len(total_neighbor)		 #
#	 result = common/(math.sqrt(d_u*d_v))
#	 return result

#weighted similarity
def weight_similarity(u,v):
	u_neighbors = GRAPH.neighbors(u) + [u]
	v_neighbors = GRAPH.neighbors(v) + [v]
	GRAPH[u][u] = {'weight':1.2}
	GRAPH[v][v] = {'weight':1.2}
	print(u)
	print(v)
	co_neighbors = list(set(u_neighbors) & set(v_neighbors))
	co_weight = 0
	for x in co_neighbors:
		co_weight += GRAPH[u][x]['weight'] * GRAPH[v][x]['weight']
	u_weight = 0
	v_weight = 0
	for x in u_neighbors:
		u_weight += GRAPH[u][x]['weight'] ** 2
	for x in v_neighbors:
		v_weight += GRAPH[v][x]['weight'] ** 2

	similarity = co_weight / sqrt(u_weight * v_weight)
	return similarity

# function for disjoint : union
def union(u,v):
	global GRAPH						# cluster label choose the smaller one
	un = find_subset(u)
	vn = find_subset(v)
	if(un <= vn):
		GRAPH.node[vn]['label'] = un
	else:
		GRAPH.node[un]['label'] = vn

# function for disjoint : find_subset
def find_subset(u):
	if (GRAPH.node[u]['label'] != u):
		u = GRAPH.node[u]['label']
		u = find_subset(u)
	return u

def max_ed(ed):
	key = -1
	value = -1
	for k in ed.keys():
		v = ed[k]
		if(v > value):
			value = v
			key = k
	return key

def CheckCore(u):
	if(GRAPH.node[u]["ed"] >=mu and GRAPH.node[u]["sd"] <mu ):
		GRAPH.node[u]["ed"] = GRAPH.degree(u)+1
		GRAPH.node[u]["sd"] = 1
		for v in GRAPH.neighbors(u):
			sigma = weight_similarity(u, v)
			if(sigma >= epsilon):
				GRAPH.node[u]["sd"] += 1
				GRAPH.edge[u][v] = 1					# u,v are checked and struct similar
				GRAPH.edge[v][u] = 1
			else:
				GRAPH.node[u]["ed"] -= 1
				ed[u] -= 1
				GRAPH.edge[u][v] = 0					# u,v are checked and not struct similar
				GRAPH.edge[v][u] = 0
			if (GRAPH.node[v]["explored"] == 0):
				if(sigma >= epsilon):
					GRAPH.node[v]["sd"] += 1
				else:
					GRAPH.node[v]["ed"] -= 1
					ed[v] -= 1
			if(GRAPH.node[u]["ed"] < mu or GRAPH.node[u]["sd"] >=mu ):
				break
	GRAPH.node[u]["explored"] = 1


def ClusterCore(u):
	for v in GRAPH.neighbors(u):
		if GRAPH.edge[u][v] != {}:									  # sigma(u,v) has been computed
			if(GRAPH.node[v]["sd"] >= mu) and (GRAPH.edge[u][v] == 1):
				union(u, v)
		else:
			if (find_subset(u) != find_subset(v)) and (GRAPH.node[v]["ed"] >= mu):
				sigma = weight_similarity(u, v)
				if(sigma >= epsilon):
					GRAPH.edge[v][u] = 1
					GRAPH.edge[u][v] = 1
				else:
					GRAPH.edge[v][u] = 0
					GRAPH.edge[u][v] = 0
				if GRAPH.node[v]["explored"] == 0:
					if(sigma >= epsilon):
						GRAPH.node[v]["sd"] += 1
					else:
						GRAPH.node[v]["ed"] -= 1
						ed[v] -= 1
				if(GRAPH.node[v]["sd"] >= mu and GRAPH.edge[u][v] == 1):
					union(u, v)

def derive_cluster_core(core_list):
	tmp_dict = {}
	for core in core_list:
		label = find_subset(core)
		try:
			tmp_dict[label].append(core)
		except:
			tmp_dict[label] = [core]
	cluster_core = list(tmp_dict.values())
	return cluster_core

def ClusterNoncore(cluster_core):
	cluster_set = []
	for cluster in cluster_core:
		cluster_all = copy.deepcopy(cluster)
		for core in cluster:							# cluster can not changed
			for neighbor in GRAPH.neighbors(core):
				if (GRAPH.node[neighbor]["sd"] < mu) and (neighbor not in cluster_all):
					if(GRAPH.edge[neighbor][core] == 1):
						cluster_all.append(neighbor)
					else:
						sigma = weight_similarity(core,neighbor)
						if(sigma >= epsilon):
							cluster_all.append(neighbor)
		cluster_all = sorted(cluster_all)
		cluster_set.append(cluster_all)
	return cluster_set

def evaluate(cluster_set):
	average_degree = []
	for cluster in cluster_set:
		node_num = len(cluster)
		edge_num = 0
		for u,v in GRAPH.edges_iter():
			if(u in cluster and v in cluster):
				edge_num += 1
		average_degree.append((node_num, round(edge_num/node_num, 1)))
	return average_degree


def pscan():
	global GRAPH

	# Initialize sd, ed, explored and cluster label disjoint,
	# ed must have a variable  to store in addition.
	# and core vertex list
	global ed
	ed = GRAPH.degree(GRAPH.nodes())
	core_list = []
	for node in GRAPH.nodes_iter():
		GRAPH.node[node] = {"sd": 1, "ed": (GRAPH.degree(node)+1), "label": node, "explored": 0}
	for u, v in GRAPH.edges_iter():
		GRAPH.edge[u][v] = {}
		GRAPH.edge[v][u] = {}
	while(len(ed) != 0):
		node = max_ed(ed)
		if(node == 2795):
			abc = 1
		CheckCore(node)
		if(GRAPH.node[node]["sd"] >= mu):
			core_list.append(node)
			ClusterCore(node)
		ed.pop(node)
	cluster_core = derive_cluster_core(core_list)

	cluster_set = ClusterNoncore(cluster_core)
	return cluster_set

def hubAndOutlier(cluster_set):
	tmp_dict = {}
	index = 1
	hub = 0
	outlier = 0
	for cluster in cluster_set:
		for node in cluster:
			try:
				tmp_dict[node].append(index)
			except:
				tmp_dict[node] = [index]
		index += 1
	for node in GRAPH.nodes_iter():
		if(node not in tmp_dict.keys()):
			neighbor_cluster = []
			for neighbor in GRAPH.neighbors(node):
				if(neighbor in tmp_dict.keys()):
					neighbor_cluster = neighbor_cluster + tmp_dict[neighbor]
					neighbor_cluster = list(set(neighbor_cluster))
					if(len(neighbor_cluster)>=2):
						hub += 1
						break
			if(len(neighbor_cluster)<2):
				outlier+=1
	return (hub,outlier)


if __name__ == "__main__":
	# read file and set parameters

	path = '../Data/result/dailyWeighted/sim_cos_e.csv'
	GRAPH = nx.read_weighted_edgelist(path, delimiter=',', nodetype=int)
	print(GRAPH.node[0])
	if (len(sys.argv)!=3):
		sys.argv = [' ', 0.5, 4]
	epsilon = sys.argv[1]
	mu = sys.argv[2]

	result_set = []
	while (mu < 10):
		epsilon = 0.2
		while(round(epsilon, 1)<1):
			# output file path
			filename = "../Data/result/dailyWeighted/" + str(round(epsilon, 1))+'_'+str(mu)+"_result.txt"
			# main program
			# GRAPH = nx.read_edgelist(path, delimiter=',', nodetype=int)
			tStart = time.time()
			cluster_set = pscan()
			#print("number of cluster: %s" %(len(cluster_set)))
			tEnd = time.time()
			#print("Done psan in %s seconds" %str(round(tEnd-tStart, 1)))
			#print("Evaluating with epsilon = %s, mu = %s" %(str(round(epsilon,1)), str(mu)))
			tStart = time.time()
			result = evaluate(cluster_set)
			tEnd = time.time()
			#print("Evaluate done in %s seconds" %(str(round(tEnd-tStart, 1))))
			#print("Calculating hub and outlier")
			hub,outlier = hubAndOutlier(cluster_set)
			print("\nhub:%s  outlier:%s" %(hub, outlier))
			print("\n")
			result_set.append(result)
			with open(filename, 'w', encoding='utf8') as f:
				index = 0
				for cluster in cluster_set:
					f.write(str(cluster)+'\n')
				f.write(str(result) + "epsilon: " + str(round(epsilon, 1)) + " mu: " + str(mu))
				f.write("\nhub:%s  outlier:%s" %(hub,outlier))
				# print("Done with epsilon = %s, mu = %s" %(str(round(epsilon, 1)), str(mu)))
			epsilon += 0.1
		mu += 1
	with open("../Data/result/dailyWeighted/result_cos_e.csv", 'w', encoding='utf8') as g:
		for result in result_set:
			g.write(str(result)+'\n')



	# cluster_set = pscan()

	# test code 1
	# path = '../data/test/test.txt'
	# GRAPH = nx.read_edgelist(path, delimiter=',', nodetype=int)
	# tStart = time.time()
	# cluster_set = pscan()
	# print(cluster_set)

