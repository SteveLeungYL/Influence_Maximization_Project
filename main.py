"""
Author: Yu Liang.
Main calling functions for Fake News Diffusion project.
"""
from Data_Structure import *
from Greedy_Algorithm import *
from Global_Variables import *
# input files and form the structure.
graph = Graph(csvFile=csv_file_directory)


for negative_seed_id in negative_seed_id_list:
    node = graph.nodeDict[negative_seed_id]
    node.active_state = Active_State.negative_active

positiveSeed, graph = greedy(graph, number_of_Positive_Seed)
print("Positive activate number and negative activate number are: " + str(
    graph.get_Positive_and_Negative_Nodes_number()))
print("Pick positive seed node ID are: " + str(positiveSeed))

