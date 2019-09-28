"""
Author: Yu Liang.
Evaluation functions and supports functions for Fake News Diffusion project.
"""
from Data_Structure import *
from Global_Variables import *
from Greedy_Algorithm import *

def setup_seed_node(seedNodeIDList:[int], graph:Graph, active_state:Active_State):
    for seedNodeID in seedNodeIDList:
        node = graph.nodeGraph.node[seedNodeID]
        node['active_state'] = active_state


def evaluation(positiveSeedNodeList:[int], graph:Graph):

    setup_seed_node(positiveSeedNodeList, graph, Active_State.positive_active)

    while graph.try_activate_single_step():
        pass
    positiveNodeNumber = graph.get_Positive_and_Negative_Nodes_number()[0]
    return positiveNodeNumber, graph