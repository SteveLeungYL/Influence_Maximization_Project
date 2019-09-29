"""
Author: Yu Liang.
Main calling functions for Fake News Diffusion project.
"""
from Data_Structure import *
from Greedy_Algorithm import *
from Global_Variables import *
from Evaluation import *
# input files and form the structure.

finalScoreRealWorldList = []
finalScoreUniformList = []

for epoch in range(10):
    print("Runtime " + str(epoch+1) + ": ")
    graph = Graph(random_initialized=True)
    graph_for_realworld = graph.copy_graph()
    graph_for_uniform = graph.copy_graph()
    graph_for_evaluate_realworld = graph.copy_graph()
    graph_for_evaluate_uniform = graph.copy_graph()

    graph.set_nodes_attributes()
    graph_for_realworld.set_nodes_attributes(fDistribution=real_world_distribution[0], r1Distribution=
    real_world_distribution[1], r2Distribution= real_world_distribution[2])
    graph_for_uniform.set_nodes_attributes(fDistribution=0.33333333333333, r1Distribution=0.33333333333333, r2Distribution=
    0.33333333333333 )
    graph_for_evaluate_realworld.set_nodes_attributes(fDistribution=evaluation_distribution[0],
                                                      r1Distribution=evaluation_distribution[1],
                                                      r2Distribution=evaluation_distribution[2])
    graph_for_evaluate_uniform.set_nodes_attributes(fDistribution=evaluation_distribution[0],
                                                      r1Distribution=evaluation_distribution[1],
                                                      r2Distribution=evaluation_distribution[2])

    setup_seed_node(negative_seed_id_list, graph_for_realworld, Active_State.negative_active)
    setup_seed_node(negative_seed_id_list, graph_for_uniform, Active_State.negative_active)
    setup_seed_node(negative_seed_id_list, graph_for_evaluate_realworld, Active_State.negative_active)
    setup_seed_node(negative_seed_id_list, graph_for_evaluate_uniform, Active_State.negative_active)


    positiveSeedFromRealWorld, graphFromRealWorld = greedy(graph_for_realworld, number_of_Positive_Seed)
    positiveSeedFromUniform, graphFromUniform = greedy(graph_for_uniform, number_of_Positive_Seed)


    print("Realworld: Positive activate number and negative activate number are: " + str(
        graphFromRealWorld.get_Positive_and_Negative_Nodes_number()))
    print("Realworld: Pick positive seed node ID are: " + str(positiveSeedFromRealWorld))

    # print("\n")

    print("Uniform: Positive activate number and negative activate number are: " + str(
        graphFromUniform.get_Positive_and_Negative_Nodes_number()))
    print("Uniform: Pick positive seed node ID are: " + str(positiveSeedFromUniform))

    finalSingleRealworldScore, _ = evaluation(positiveSeedFromRealWorld, graph_for_evaluate_realworld)
    finalSingleUniformScore, _ = evaluation(positiveSeedFromUniform, graph_for_evaluate_uniform)

    print("The positive nodes for real world distribution for evaluation is: " + str(finalSingleRealworldScore))
    print("The positive nodes for uniform distribution for evaluation is: " + str(finalSingleUniformScore))
    print("\n\n")

    finalScoreRealWorldList.append(finalSingleRealworldScore)
    finalScoreUniformList.append(finalSingleUniformScore)

print("\n\n\n")
print("The final average positive nodes for real world distribution for evaluation is: " + str(sum(
    finalScoreRealWorldList)/len(finalScoreRealWorldList)))
print("The final average positive nodes for uniform distribution for evaluation is: " + str(sum(
    finalScoreUniformList)/len(finalScoreUniformList)))


# graph.plot_graph()

