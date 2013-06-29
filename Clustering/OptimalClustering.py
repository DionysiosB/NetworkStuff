import networkx as nx
from operator import itemgetter
from operator import mul
import matplotlib.pyplot as plt
import math

################################################################################################################################################################
################################################################################################################################################################
def BinomialCoefficient(n,r):
    if r > n-r:
        r = n-r
    return int( reduce( mul, range((n-r+1), n+1), 1)/reduce( mul, range(1,r+1), 1) )

################################################################################################################################################################
################################################################################################################################################################
def DisconnectedGraph(n,m):
	if m<(n-1):
		G=nx.Graph()
		G.add_nodes_from(range(n))
		number_of_triangles=m/3
		vertex_index=0
		for triangle_index in range(number_of_triangles):
			G.add_edge(vertex_index,vertex_index+1)
			G.add_edge(vertex_index+1,vertex_index+2)
			G.add_edge(vertex_index+2,vertex_index)
			vertex_index=3*(triangle_index+1)
		
		remaining_edges=m-3*number_of_triangles
		for current_edge in range(remaining_edges):
			G.add_edge(vertex_index,vertex_index+1)
			vertex_index=vertex_index+2
		return G

################################################################################################################################################################
################################################################################################################################################################
def AlmostTree(n,m):
	t=m-n+1
	vertices_in_triangles=3*t
	edges_in_triangles=3*t
	
	if vertices_in_triangles<=n:
		G=nx.star_graph(n-2*t-1)
		vertex_index=n-2*t
		for triangle_index in range(t):
			G.add_edge((triangle_index+1)%(n-2*t),vertex_index)
			G.add_edge((triangle_index+1)%(n-2*t),vertex_index+1)
			G.add_edge(vertex_index,vertex_index+1)
			vertex_index=vertex_index+2
		return G
		
	if vertices_in_triangles>n:
		g=3*t-n+1   #Number of merged triangles
		f=t-g		#Number of free triangles
		G=nx.star_graph(f+2*g)
		star_index=0
		for merged_index in range(g):
			star_index=star_index+2
			G.add_edge(star_index,star_index-1)
		
		vertex_index=f+2*g+1
		for triangle_index in range(f):
			star_index=star_index+1
			G.add_edge(star_index,vertex_index)
			G.add_edge(star_index,vertex_index+1)
			G.add_edge(vertex_index,vertex_index+1)
			vertex_index=vertex_index+2
		return G

################################################################################################################################################################
################################################################################################################################################################
def Type1AlmostCompleteGraph(n,m):
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
def Type2AlmostCompleteGraph(n,m):
	if ( (BinomialCoefficient(n-1,2)+2 <= m) and (m <= BinomialCoefficient(n,2)-1)  ):
		G=nx.complete_graph(n-1)
		remaining_edges=m-BinomialCoefficient(n-1,2)
		for vertex_index in range(remaining_edges):
			G.add_edge(n-1,vertex_index)
		return G

################################################################################################################################################################
################################################################################################################################################################
def OptimalGraphFinder(number_of_vertices,number_of_edges,previous_graph_dict):
	
	################################################################################################################################################################
	if number_of_edges<(number_of_vertices-1):
		F=DisconnectedGraph(number_of_vertices,number_of_edges)
		return F
	################################################################################################################################################################
	if ((number_of_edges>=number_of_vertices-1) and number_of_edges<=(3*(number_of_vertices-1)/2)  ):
		F=AlmostTree(number_of_vertices,number_of_edges)
		return F
	################################################################################################################################################################
	if ( (number_of_edges>(3*(number_of_vertices-1)/2))   and (number_of_edges <= BinomialCoefficient(number_of_vertices-2,2)+3) ):
		
		best_clustering=0
		for d in range(2,number_of_vertices):
			PreviousGraph=previous_graph_dict[(number_of_vertices-1,number_of_edges-d)]
			if nx.is_connected(PreviousGraph)==0:
				break
			existing_cliques=list(nx.find_cliques(PreviousGraph))
			for current_clique in existing_cliques:
				if d>len(current_clique):continue
				vertex_degrees=PreviousGraph.degree(current_clique)
				sorted_vertices_bydegree=sorted(vertex_degrees.items(),key=itemgetter(1),reverse=True)
				sorted_vertices=[currentpair[0] for currentpair in sorted_vertices_bydegree]
				
				G=PreviousGraph.copy()
				counter=0
				for connected_vertex in sorted_vertices:
					counter=counter+1
					G.add_edge(number_of_vertices-1,connected_vertex)
					if counter>=d:break
				
				current_clustering=nx.average_clustering(G)
				if current_clustering>best_clustering:
					best_clustering=current_clustering
					F=G.copy()
				
		return F
	################################################################################################################################################################
	if ( (BinomialCoefficient(number_of_vertices-2,2)+4 <= number_of_edges) and (number_of_edges <= BinomialCoefficient(number_of_vertices-1,2) +1) ):
		F=Type1AlmostCompleteGraph(number_of_vertices,number_of_edges)	
		return F
	################################################################################################################################################################	
	if ( (BinomialCoefficient(number_of_vertices-1,2)+2 <= number_of_edges) and (number_of_edges <= BinomialCoefficient(number_of_vertices,2)-1)  ):
		F=Type2AlmostCompleteGraph(number_of_vertices,number_of_edges)
		return F
	################################################################################################################################################################	
	if number_of_edges==BinomialCoefficient(number_of_vertices,2):
		F=nx.complete_graph(number_of_vertices)
		return F
		
	return F

################################################################################################################################################################
################################################################################################################################################################
def OptimalGraphBuilder(number_of_vertices,number_of_edges):
	
	all_graphs_dict=dict()
	for current_order in range(3,number_of_vertices):
		for current_size in range( min(1+BinomialCoefficient(current_order,2),number_of_edges) ):
			NewGraph=OptimalGraphFinder(current_order,current_size,all_graphs_dict)
			all_graphs_dict[(current_order,current_size)]=NewGraph
		print 'Order ', current_order
	
	output_graph=OptimalGraphFinder(number_of_vertices,number_of_edges,all_graphs_dict)		
	return output_graph

################################################################################################################################################################
################################################################################################################################################################


testGraph=OptimalGraphBuilder(30,200)
nx.draw(testGraph)
plt.draw()
