import networkx as nx
from itertools import *
from operator import itemgetter
from operator import mul
import matplotlib.pyplot as plt
from math import *
import random

################################################################################################################################################################
################################################################################################################################################################
def BinomialCoefficient(n,r):
    if r > n-r:
        r = n-r
    return int( reduce( mul, range((n-r+1), n+1), 1)/reduce( mul, range(1,r+1), 1) )

################################################################################################################################################################
################################################################################################################################################################
def FastClusterFinder(number_of_vertices,number_of_edges):
	
	#print 'Number_of_vertices:', number_of_vertices, '   Number of Edges:', number_of_edges
	
	if (number_of_vertices<2) or (number_of_edges<number_of_vertices-1) or (number_of_edges>BinomialCoefficient(number_of_vertices,2)):
		return -1
	if ( (number_of_edges>=2+BinomialCoefficient(number_of_vertices-1,2)) and (number_of_edges<BinomialCoefficient(number_of_vertices,2)) ):
		return [0,(number_of_vertices-1)]
	if number_of_edges==number_of_vertices-1:
		return [2]*number_of_edges
	if number_of_edges==BinomialCoefficient(number_of_vertices,2):
		return [number_of_vertices]
		
	cluster_size=int(ceil((1+sqrt(1+8*number_of_edges))/2))
	plausibility_flag=-1
	while ((plausibility_flag==-1) and (cluster_size>=2)):
		#print '------>Current Cluster: ', cluster_size
		previous_list=FastClusterFinder(number_of_vertices-cluster_size+1,number_of_edges-BinomialCoefficient(cluster_size,2))
		if (type(previous_list)==list) :
			#print 'Previous List:', previous_list
			new_list=previous_list[:]
			new_list.append(cluster_size)
			return new_list
		cluster_size=cluster_size-1
	
	return 0

################################################################################################################################################################
################################################################################################################################################################
def Alternative_FastClusterFinder(number_of_vertices,number_of_edges):
	
	#print 'Number_of_vertices:', number_of_vertices, '   Number of Edges:', number_of_edges
	
	if (number_of_vertices<3) or (number_of_edges<3*(number_of_vertices-1)/2) or (number_of_edges>BinomialCoefficient(number_of_vertices,2)):
		return -1
	if ( (number_of_edges>=2+BinomialCoefficient(number_of_vertices-1,2)) and (number_of_edges<BinomialCoefficient(number_of_vertices,2)) ):
		return [0,(number_of_vertices-1)]
	if number_of_edges==(3*(number_of_vertices-1)/2):
		return [3]*((number_of_vertices-1)/2)
	if number_of_edges==BinomialCoefficient(number_of_vertices,2):
		return [number_of_vertices]
		
	cluster_size=int(ceil((1+sqrt(1+8*number_of_edges))/2))
	plausibility_flag=-1
	while ((plausibility_flag==-1) and (cluster_size>=2)):
		#print '------>Current Cluster: ', cluster_size
		previous_list=Alternative_FastClusterFinder(number_of_vertices-cluster_size+1,number_of_edges-BinomialCoefficient(cluster_size,2))
		if (type(previous_list)==list) :
			#print 'Previous List:', previous_list
			new_list=previous_list[:]
			new_list.append(cluster_size)
			return new_list
		cluster_size=cluster_size-1
	
	return 0

################################################################################################################################################################
################################################################################################################################################################
def Type1AlmostCompleteGraph(n,m):
	if ( (BinomialCoefficient(n-1,2)+2 <= m) and (m <= BinomialCoefficient(n,2)-1)  ):
		G=nx.complete_graph(n-1)
		remaining_edges=m-BinomialCoefficient(n-1,2)
		for vertex_index in range(remaining_edges):
			G.add_edge(n-1,vertex_index)
		return G

################################################################################################################################################################
################################################################################################################################################################
def Type2AlmostCompleteGraph(n,m):
	if ( (BinomialCoefficient(n-2,2)+4 <= m) and (m <= BinomialCoefficient(n-1,2) +1) ):
		first_candidate=nx.complete_graph(n-2)
		remaining_edges=m-BinomialCoefficient(n-2,2)
		first_candidate.add_edge(n-2,0)
		first_candidate.add_edge(n-2,1)
		for vertex_index in range(remaining_edges-2):
			first_candidate.add_edge(n-1,vertex_index)
		first_coefficient=nx.average_clustering(first_candidate)
		
		second_candidate=nx.complete_graph(n-2)
		second_candidate.add_edge(n-2,n-1)
		remaining_edges=(m-BinomialCoefficient(n-2,2)-1)
		number_of_common_neighbors=(remaining_edges/2)
		for vertex_index in range(number_of_common_neighbors):
			second_candidate.add_edge(vertex_index,n-2)
			second_candidate.add_edge(vertex_index,n-1)
		if (remaining_edges-2*number_of_common_neighbors)==1:
			second_candidate.add_edge(vertex_index+1,n-2)
		second_coefficient=nx.average_clustering(second_candidate)
		
		if first_coefficient>second_coefficient:
			G=first_candidate.copy()
		else:
			G=second_candidate.copy()
		return G

################################################################################################################################################################
################################################################################################################################################################
def SuboptimalSmallWorldGraphBuilder(number_of_vertices,number_of_edges):
	
	if number_of_edges<number_of_vertices-1:
		print 'Not enough edges for a connected graph. Exiting...'
		return -1
	if number_of_edges>BinomialCoefficient(number_of_vertices,2):
		print 'Too many edges given. Exiting...'
		return -1
	if number_of_vertices==1 and number_of_edges==0:
		G=nx.Graph()
		G.add_node(0)
		return G
	if ( (BinomialCoefficient(number_of_vertices-1,2)+2 <= number_of_edges) and (number_of_edges <= BinomialCoefficient(number_of_vertices,2)-1)  ):
		return Type1AlmostCompleteGraph(number_of_vertices,number_of_edges)
	if ( (BinomialCoefficient(number_of_vertices-2,2)+4 <= number_of_edges) and (number_of_edges <= BinomialCoefficient(number_of_vertices-1,2)+1)):
		return Type2AlmostCompleteGraph(number_of_vertices,number_of_edges)
		
	cluster_size_list=Alternative_FastClusterFinder(number_of_vertices,number_of_edges)
	remaining_edges=0
	if cluster_size_list[0]==0:
		remaining_edges=number_of_edges
		idontcare=cluster_size_list.pop(0)
		for k in cluster_size_list:
			remaining_edges=remaining_edges-BinomialCoefficient(k,2)
	cluster_size_list.reverse()											#Put the biggest cluster in the front, so that we know where to attach the remaining edges.				
	G=nx.star_graph(number_of_vertices-1)
	for k in range(1,remaining_edges):
		G.add_edge(number_of_vertices-1,k)
	vertex_index=1														#Start from a star, and build the peripheral clusters by renaming the complete subgraphs.
	for dummy_cluster in cluster_size_list:
		if dummy_cluster>2:
			T=nx.complete_graph(dummy_cluster-1)
			W=nx.convert_node_labels_to_integers(T,vertex_index)
			G.add_edges_from(W.edges())
			vertex_index=vertex_index+dummy_cluster-1	
	return G
		

################################################################################################################################################################
################################################################################################################################################################
def GraphRewiring(G,number_of_rewirings):
	number_of_vertices=G.order()
	number_of_edges=G.size()
	
	rewirings_left=number_of_rewirings
	while rewirings_left>0:
		current_edge_list=G.edges()
		current_random_edge=random.choice(current_edge_list)
		#print current_random_edge
		if 0 in current_random_edge:continue 				#We want the star architecture
		first_vertex=random.randrange(1,number_of_vertices)
		candidate_second_vertices=range(number_of_vertices)
		candidate_second_vertices.remove(first_vertex)
		for u in G.neighbors(first_vertex):candidate_second_vertices.remove(u);
		#print candidate_second_vertices
		if len(candidate_second_vertices)==0: continue
		second_vertex=random.choice(candidate_second_vertices)
		G.remove_edges_from([current_random_edge])
		G.add_edge(first_vertex,second_vertex)
		#print first_vertex,second_vertex
		if nx.is_connected(G): rewirings_left-=1;
	return G

################################################################################################################################################################
################################################################################################################################################################

graph_order=2000
graph_size=20000

G=SuboptimalSmallWorldGraphBuilder(graph_order,graph_size)

clustering_list=list()
distance_list=list()
for k in range(graph_size):
	GraphRewiring(G,1)
	myclustering=nx.average_clustering(G)
	clustering_list.append(myclustering)
	mydistance=nx.average_shortest_path_length(G)
	distance_list.append(mydistance)
		
print clustering_list
print distance_list
		