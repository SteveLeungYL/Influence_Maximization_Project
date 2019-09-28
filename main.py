"""
Author: Yu Liang.
Main calling functions for Fake News Diffusion project.
"""
from Data_Structure import *
from Greedy_Algorithm import *
from Global_Variables import *
from Evaluation import *
# input files and form the structure.
graph = Graph(random_initialized=True)
graph_for_realworld = graph.copy_graph()
graph_for_uniform = graph.copy_graph()
graph_for_evaluate_realworld = graph.copy_graph()
graph_for_evaluate_uniform = graph.copy_graph()

graph.set_nodes_attributes()
graph_for_realworld.set_nodes_attributes(fDistribution=0.722222222, r1Distribution=	0.076388889, r2Distribution=
0.201388889 )
graph_for_uniform.set_nodes_attributes(fDistribution=0.33333333333333, r1Distribution=0.33333333333333, r2Distribution=
0.33333333333333 )
graph_for_evaluate_realworld.set_nodes_attributes(fDistribution=0.9538461538461539,
                                                  r1Distribution=0.042735042735042736, r2Distribution=0.003418803418803419)
graph_for_evaluate_uniform.set_nodes_attributes(fDistribution=0.9538461538461539, r1Distribution=0.042735042735042736,
                                          r2Distribution=0.003418803418803419)

setup_seed_node(negative_seed_id_list, graph_for_realworld, Active_State.negative_active)
setup_seed_node(negative_seed_id_list, graph_for_uniform, Active_State.negative_active)
setup_seed_node(negative_seed_id_list, graph_for_evaluate_realworld, Active_State.negative_active)
setup_seed_node(negative_seed_id_list, graph_for_evaluate_uniform, Active_State.negative_active)


positiveSeedFromRealWorld, graphFromRealWorld = greedy(graph_for_realworld, number_of_Positive_Seed)
positiveSeedFromUniform, graphFromUniform = greedy(graph_for_uniform, number_of_Positive_Seed)


print("Realworld: Positive activate number and negative activate number are: " + str(
    graphFromRealWorld.get_Positive_and_Negative_Nodes_number()))
print("Pick positive seed node ID are: " + str(positiveSeedFromRealWorld))

print("Uniform: Positive activate number and negative activate number are: " + str(
    graphFromUniform.get_Positive_and_Negative_Nodes_number()))
print("Pick positive seed node ID are: " + str(positiveSeedFromUniform))

finalRealworldScore, _ = evaluation(positiveSeedFromRealWorld, graph_for_evaluate_realworld)
finalUniformScore, _ = evaluation(positiveSeedFromUniform, graph_for_evaluate_uniform)

print("\n\n\n")
print("The final positive nodes for real world distribution for evaluation is: " + str(finalRealworldScore))
print("The final positive nodes for uniform distribution for evaluation is: " + str(finalUniformScore))


# graph.plot_graph()

