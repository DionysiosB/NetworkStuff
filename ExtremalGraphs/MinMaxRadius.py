import networkx as nx
from operator import itemgetter
import math
import random

from time import *
import pylab as P

############################################################################################################################################################
############################################################################################################################################################
def MaxRadiusGraphFinder(number_of_vertices,number_of_edges):
	
	#WARNING: CONTAINS ERROR FOR WHEN WE HAVE SUFFICIENTLY MANY EDGES AND R=2
	
	if number_of_edges<number_of_vertices-1:
		print('Too few edges. The graph will be disconnected. Exiting...')
		return -1
	if number_of_edges>(number_of_vertices-1)*number_of_vertices/2.0:
		print('Too many edges. Such a graph cannot exist. Exiting...')
		return -1
		
	if number_of_edges==number_of_vertices-1:
		G=nx.path_graph(number_of_vertices)
		return G
		
	G=nx.cycle_graph(number_of_vertices)
	remaining_edges=number_of_edges-number_of_vertices
	
	for current_vertex in range(2,number_of_vertices):
		if remaining_edges<=0:break
		for previous_vertex in range(current_vertex-2,-1,-1):
			G.add_edge(previous_vertex,current_vertex)
			remaining_edges-=1
			if remaining_edges<=0:break
	
	return G

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
			return Input_Graph
			break
			
	return H

############################################################################################################################################################
############################################################################################################################################################
def MinRadiusGraphFinder(number_of_vertices,number_of_edges):
		
	if number_of_edges<number_of_vertices-1:
		print 'Too few edges. The graph will be disconnected. Exiting...'
		return -1
	if number_of_edges>(number_of_vertices-1)*number_of_vertices/2.0:
		print 'Too many edges. Such a graph cannot exist. Exiting...'
		return -1
		
	if number_of_edges>(number_of_vertices-2)*(number_of_vertices-1)/2.0:
		OutputGraph=nx.gnm_random_graph(number_of_vertices,number_of_edges)
		return OutputGraph
	
	
	G=nx.star_graph(number_of_vertices-1)
	VertexList=G.nodes()
	remaining_edges=number_of_edges-number_of_vertices+1
	
	while remaining_edges>0:
		first_vertex=random.choice(VertexList)
		second_vertex=random.choice(VertexList)
		if first_vertex==second_vertex:continue
		if (first_vertex,second_vertex) in G.edges():continue
		if (second_vertex,first_vertex) in G.edges():continue
		
		G.add_edge(first_vertex,second_vertex)
		remaining_edges-=1
		
	OutputGraph=G.copy()
		
	return OutputGraph

############################################################################################################################################################
############################################################################################################################################################

N=8
m=12

Gmin=MinRadiusGraphFinder(N,m)
Gmax=MaxRadiusGraphFinder(N,m)
