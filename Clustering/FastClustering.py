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
		
	cluster_size_list=FastClusterFinder(number_of_vertices,number_of_edges)
	remaining_edges=0
	if cluster_size_list[0]==0:
		remaining_edges=number_of_edges
		idontcare=cluster_size_list.pop(0)
		for k in cluster_size_list:
			remaining_edges=remaining_edges-BinomialCoefficient(k,2)
	print 'Remaining_Edges:', remaining_edges							#Find if there is a type 1 almost complete graph (there can be at most one)
	cluster_size_list.reverse()											#Put the biggest cluster in the front, so that we know where to attach the remaining edges.				
	G=nx.star_graph(number_of_vertices-1)
	for k in range(1,remaining_edges):
		G.add_edge(number_of_vertices-1,k)
	vertex_index=1														#Start from a star, and build the peripheral clusters by renaming the complete subgraphs.
	print cluster_size_list
	for dummy_cluster in cluster_size_list:
		if dummy_cluster>2:
			T=nx.complete_graph(dummy_cluster-1)
			print T.edges()
			W=nx.convert_node_labels_to_integers(T,vertex_index)
			print W.edges()
			G.add_edges_from(W.edges())
			vertex_index=vertex_index+dummy_cluster-1
			print 'Cluster Size:', dummy_cluster
			print 'Vertex Index:', vertex_index
	
	return G
		

################################################################################################################################################################
################################################################################################################################################################


aaa=SuboptimalSmallWorldGraphBuilder(11,35)
print aaa.edges()