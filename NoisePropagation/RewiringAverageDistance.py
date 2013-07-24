import networkx as nx
from operator import itemgetter
import math
import random


############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
def MaxDistanceGraphFinder(number_of_vertices,number_of_edges):
	
	if number_of_edges<number_of_vertices-1:
		print 'Too few edges. The graph will be disconnected. Exiting...'
		return -1
	if number_of_edges>(number_of_vertices-1)*number_of_vertices/2.0:
		print 'Too many edges. Such a graph cannot exist. Exiting...'
		return -1
		
	G=nx.path_graph(number_of_vertices)
	remaining_edges=number_of_edges-number_of_vertices+1
	
	for current_vertex in range(2,number_of_vertices):
		if remaining_edges<=0:break
		for previous_vertex in range(current_vertex-1):
			G.add_edge(previous_vertex,current_vertex)
			remaining_edges-=1
			if remaining_edges<=0:break
	
	return G

############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
def SingleEdgeRewiring(Input_Graph):
	
	max_count=1000
	N=Input_Graph.order()
	m=Input_Graph.size()
	G=Input_Graph.copy()
	
	#############################################################################
	#############################DOUBLE REWIRINGS################################
	#############################################################################
	
	EdgeList=G.edges()
	K=nx.complement(G)
	NonEdgeList=K.edges()
	
	ConnectedGraph=0
	trial_count=0
	while ConnectedGraph==0:
		H=G.copy()
		trial_count+=1
		OldEdge=random.choice(EdgeList)
		NewEdge=random.choice(NonEdgeList)		
		H.remove_edges_from([OldEdge])
		H.add_edges_from([NewEdge])
		
		if nx.is_connected(H):ConnectedGraph=1
		if trial_count>max_count:
			print 'A connected graph could not be found.'
			return -1
			break
			
	return H

############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################

G=MaxDistanceGraphFinder(200,8000)

number_of_steps=100
DistanceList=[0]*number_of_steps

for step in range(number_of_steps):
	DistanceList[step]=nx.average_shortest_path_length(G)
	G=SingleEdgeRewiring(G)
print DistanceList