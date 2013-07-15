import networkx as nx
from operator import itemgetter
from operator import mul
import matplotlib.pyplot as plt
import math
import random

################################################################################################################################################################
################################################################################################################################################################
def EdgeStarExperiment(number_of_vertices,number_of_edges):
	
	if number_of_vertices<1:
		print 'Why do you need me to make an empty graph???'
		return -1
	if number_of_edges<number_of_vertices-1:
		print 'With so few edges, how am I supposed to produce a connected graph???'
		return -1
	if number_of_edges>(number_of_vertices*(number_of_vertices-1)/2):
		print 'Way too many edges in here...'
		return -1
	
	G=nx.star_graph(number_of_vertices-1)
	while G.size()<number_of_edges:
		first_vertex=random.randrange(number_of_vertices)
		second_vertex=random.randrange(number_of_vertices)
		if first_vertex != second_vertex:
			G.add_edge(first_vertex,second_vertex)
		
	#average_distance=nx.average_shortest_path_length(G)
	return G

################################################################################################################################################################
################################################################################################################################################################
for k in range(10):
	F=EdgeStarExperiment(1000,50000)
	print 'Distance:', nx.average_shortest_path_length(F)
	#print 'Size: ', F.size()
	#print 'Vertices:', F.order()
	#print 'Edges:', F.edges()
	print '-----------------------------------------------'

