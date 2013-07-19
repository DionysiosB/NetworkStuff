import networkx as nx
from operator import itemgetter
import math

############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
def CrosstalkFunction(GraphOrder,VertexDegree):
	N=GraphOrder
	d=VertexDegree
	output=(N-d-1)*math.sqrt(d)
	return output

############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
def TotalCrosstalk(degree_sequence):
	N=len(degree_sequence)
	total=0
	for k in degree_sequence:
		total+=(N-1-k)*math.sqrt(k)
	return total

############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################
def MinXtalkRewiringAlgorithm(Input_Graph):
	
	N=Input_Graph.order()
	G=Input_Graph.copy()
	
	#############################################################################
	#############################SINGLE REWIRINGS################################
	#############################################################################
	first_step_flag=1
	while first_step_flag==1:
		first_step_flag=0
		#print 'New FIRST STEP loop...'
		for current_vertex in G.nodes():
			if first_step_flag==1:break
			current_neighbors=G.neighbors(current_vertex)
			current_nonneighbors=list(set(G.nodes())-set(G.neighbors(current_vertex))-set([current_vertex]))
			
			current_neighbors_degrees=dict()
			current_nonneighbors_degrees=dict()
			
			for x in current_neighbors:
				current_neighbors_degrees[x]=G.degree(x)
			for y in current_nonneighbors:
				current_nonneighbors_degrees[y]=G.degree(y)
			
			if len(current_neighbors_degrees)==0:continue
			if len(current_nonneighbors_degrees)==0:continue
			
			sorted_neighbors_by_degree=sorted(current_neighbors_degrees.items(),key=itemgetter(1))
			sorted_nonneighbors_by_degree=sorted(current_nonneighbors_degrees.items(),key=itemgetter(1))

			if sorted_neighbors_by_degree[0][1]<=sorted_nonneighbors_by_degree[-1][1]:
				#REWIRING MUST TAKE PLACE
				G.remove_edge(current_vertex,sorted_neighbors_by_degree[0][0])
				G.add_edge(current_vertex,sorted_nonneighbors_by_degree[-1][0])
				
				if nx.is_connected(G):
					first_step_flag=1
				else:
					G.add_edge(current_vertex,sorted_neighbors_by_degree[0][0])
					G.remove_edge(current_vertex,sorted_nonneighbors_by_degree[-1][0])
					first_step_flag=0
					
	#############################################################################
	#############################DOUBLE REWIRINGS################################
	#############################################################################
	second_step_flag=1
	while second_step_flag==1:
		second_step_flag=0
		for current_edge in G.edges():
			#print 'NEW CURRENT EDGE LOOP'
			if second_step_flag==0:break;
			current_first_vertex=current_edge[0]
			current_second_vertex=current_edge[1]
			
			crosstalk_first_difference=-CrosstalkFunction(N,G.degree(current_first_vertex))-CrosstalkFunction(N,G.degree(current_second_vertex))
			crosstalk_first_difference+=CrosstalkFunction(N,-1+G.degree(current_first_vertex))+CrosstalkFunction(N,-1+G.degree(current_second_vertex))
			
			H=nx.complement(G)
			for nonexisting_edge in H.edges():
				if second_step_flag==0:break;
				nonexisting_first_vertex=nonexisting_edge[0]
				nonexisting_second_vertex=nonexisting_edge[1]
				
				if nonexisting_first_vertex==current_first_vertex:continue;
				if nonexisting_first_vertex==current_second_vertex:continue;
				if nonexisting_second_vertex==current_first_vertex:continue;
				if nonexisting_second_vertex==current_second_vertex:continue;
				
				crosstalk_second_difference=CrosstalkFunction(N,1+G.degree(nonexisting_first_vertex))+CrosstalkFunction(N,1+G.degree(nonexisting_second_vertex))
				crosstalk_second_difference-=CrosstalkFunction(N,G.degree(nonexisting_first_vertex))+CrosstalkFunction(N,G.degree(nonexisting_second_vertex))
				crosstalk_potential_difference=crosstalk_first_difference+crosstalk_second_difference
				
				if crosstalk_potential_difference<0:
					G.remove_edge(current_first_vertex,current_second_vertex)
					G.add_edge(nonexisting_first_vertex,nonexisting_second_vertex)
					
					if nx.is_connected(G):
						second_step_flag=1
						if crosstalk_potential_difference==0:second_step_flag=0;
					else:
						G.add_edge(current_first_vertex,current_second_vertex)
						G.remove_edge(nonexisting_first_vertex,nonexisting_second_vertex)
						second_step_flag=0
					
	#----------------------  ALGORITHM FINISHED!  --------------------------------
	output_graph=G
	return output_graph
	

############################################################################################################################################################
############################################################################################################################################################
############################################################################################################################################################

N=40;
xtalk_vector=list()
for m in range(N-1,1+N*(N-1)/2):
	connected_flag=0
	while connected_flag==0:
		J=nx.gnm_random_graph(N,m)
		if nx.is_connected(J)==1:
			connected_flag=1
			M=MinXtalkRewiringAlgorithm(J)
			min_xtalk=TotalCrosstalk(M.degree().values())
			print M.size(), '---->',sorted(M.degree().values()),'------>', min_xtalk
			xtalk_vector.append(min_xtalk)

print xtalk_vector