import networkx as nx
import sys
from itertools import izip
import numpy as np
import scipy.linalg as linalg

from time import *
import pylab as P

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
def MaxImpedanceGraphFinder(number_of_vertices,number_of_edges):
	
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

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
def MinImpedanceGraphFinder(number_of_vertices,number_of_edges):
	
	if number_of_edges<number_of_vertices-1:
		print 'Too few edges. The graph will be disconnected. Exiting...'
		return -1
	if number_of_edges>(number_of_vertices-1)*number_of_vertices/2.0:
		print 'Too many edges. Such a graph cannot exist. Exiting...'
		return -1
	
	
	G=nx.star_graph(number_of_vertices-1)
	remaining_edges=number_of_edges-number_of_vertices+1
	
	for current_vertex in range(2,number_of_vertices):
		if remaining_edges<=0:break
		G.add_edge(1,current_vertex)
		remaining_edges-=1
		
	while remaining_edges>0:
		for first_vertex in range(2,number_of_vertices):
			if remaining_edges<=0:break
			for second_vertex in range(first_vertex+1,number_of_vertices):
				if remaining_edges<=0:break
				if second_vertex not in G.neighbors(first_vertex):
					G.add_edge(first_vertex,second_vertex)
					remaining_edges-=1
		
	return G

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################

G=MinImpedanceGraphFinder(8,19)