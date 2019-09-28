"""
Author: Yu Liang.
Greedy functions for Fake News Diffusion project.
"""
from Data_Structure import *
import copy

def greedy(graph: Graph, numberOfSeedNodes: int) -> ([int], Graph): # Return the best positive node.
    graph_for_iteration = graph.copy_graph()  # Don't modify the original graph!!! Deep copy it!!!
    nodeIDChoosen = []
    highest_utility_graph = Graph()
    previous_highest_utility_for_positive_node = 0

    if numberOfSeedNodes + len(negative_seed_id_list) > len(graph.nodeGraph):
        print("Number of Positive Seed nodes is too much.")
        numberOfSeedNodes = len(graph.nodeGraph) - len(negative_seed_id_list)
        if numberOfSeedNodes < 0:
            raise ValueError("Number of Negative Node is too much. Fail to run any algorithm on it.")

    for iterations in range(numberOfSeedNodes): # Greedy add multiple times of positive seed node inside the graph.
        graph_copy = graph_for_iteration.copy_graph()
        current_highest_margin_gain = 0
        currentNodeIDChoosen = 0
        current_highest_utility_graph = graph.copy_graph()

        for nodeID in range(len(graph_copy.nodeGraph.nodes.items())):
            # nodeID += 1
            node = graph_copy.nodeGraph.node[nodeID]
            if node['active_state'] == Active_State.negative_active or node['active_state'] == \
                    Active_State.positive_active:
                continue

            # Run the greedy algorithm, see the result.
            node['active_state'] = Active_State.positive_active
            # print("Current Set up Node ID: " + str(nodeID))
            while graph_copy.try_activate_single_step(): # Iterate to the final step.
                pass
            positiveNodeNumber, negativeNodeNumber = graph_copy.get_Positive_and_Negative_Nodes_number()
            if (positiveNodeNumber - previous_highest_utility_for_positive_node) >= current_highest_margin_gain:
                current_highest_margin_gain = (positiveNodeNumber - previous_highest_utility_for_positive_node)
                currentNodeIDChoosen = nodeID
                current_highest_utility_graph = graph_copy.copy_graph()
            graph_copy = graph_for_iteration.copy_graph()
        if currentNodeIDChoosen < 0:
            raise ValueError("Error getting node ID < 0")
        graph_for_iteration.nodeGraph.node[currentNodeIDChoosen]['active_state'] = Active_State.positive_active
        highest_utility_graph = current_highest_utility_graph
        nodeIDChoosen.append(currentNodeIDChoosen)
        previous_highest_utility_for_positive_node = \
            current_highest_utility_graph.get_Positive_and_Negative_Nodes_number()[0]

    return nodeIDChoosen, highest_utility_graph




