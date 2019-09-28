"""
Author: Yu Liang.
Data Structure file for Fake News Diffusion project.

"""
from enum import Enum
from Global_Variables import *
import networkx
import random
import matplotlib.pyplot as plt

class Active_State(Enum):
    not_active = 0
    negative_active = -1
    positive_active = 1

### Use the networkx version of the nodes instead.
# class Node:
#     nodeID:int = 0
#     parentNodeID = dict() #The edge collection between current node the next node. The value is the weight information.
#     active_state = Active_State.not_active
#     active_threshold = 1
#
#     def __init__(self, nodeID:int, active_state = Active_State.not_active, active_threshold = active_Threshold, nextNodeID = dict()):
#         self.nodeID = nodeID
#         self.active_state = active_state
#         self.active_threshold = active_threshold
#         self.parentNodeID = nextNodeID
#
#     def add_Parent_Node(self, parentNodeID:int, weight:float):
#         if parentNodeID not in self.parentNodeID:
#             self.parentNodeID[parentNodeID] = weight
#         else:
#             raise ValueError("Duplicated setting for target node weight. Errors when adding target node id.")


class Graph:
    nodeGraph = None

    def __init__(self, nodeGraph: networkx.DiGraph = None, local_file_directory:str = None, random_initialized:bool =
    False):
        if random_initialized == False and nodeGraph == None and local_file_directory == None:
            self.nodeGraph = None
        elif nodeGraph != None:
            self.nodeGraph = nodeGraph.to_directed() # Return deep copy.
        elif local_file_directory == None:
            self.nodeGraph = networkx.generators.random_graphs.erdos_renyi_graph(n=number_of_total_nodes,
                                                                                 p=possibility_of_edges_creation,
                                                                                 directed=True)
        else:
            self.read_from_local_file(local_file_directory=local_file_directory)

    def set_nodes_attributes(self, fDistribution=0.3333, r1Distribution=0.3333, r2Distribution=0.3333):
        r1Distribution += fDistribution
        r2Distribution += r1Distribution

        for nodeID in range(len(self.nodeGraph.nodes.items())):
            randomNumber = random.random()
            threshold = 0
            if randomNumber <= fDistribution:
                threshold = 1
            elif randomNumber <= r1Distribution:
                threshold = 2
            elif randomNumber <= r2Distribution+0.01:
                threshold = 3
            else:
                raise ValueError("Error checking the threshold distribution. Doesn't sum up to be 1.")
            self.nodeGraph.node[nodeID]['threshold'] = threshold
            self.nodeGraph.node[nodeID]['active_state'] = Active_State.not_active

    def copy_graph(self):
        return Graph(nodeGraph=self.nodeGraph.to_directed())

    def save_graph(self, directory:str):
        networkx.write_gpickle(self.nodeGraph, directory)

    def read_from_local_file(self, local_file_directory: str):
        self.nodeGraph = networkx.read_gpickle(local_file_directory)

    def get_node(self, nodeID:int):
        return self.nodeGraph.node[nodeID]

    def try_activate_single_step(self) -> bool:
        isAnyChangesOfGraph = False

        modifiedNodeGraph = self.nodeGraph.to_directed() # Deep copy, changes on the modified node will not influence
        # the original graph. Making sure the single step behavior.
        for nodeID in range(len(self.nodeGraph.nodes.items())):

            # Check active state.
            # nodeID += 1
            if self.nodeGraph.node[nodeID]['active_state'] == Active_State.positive_active or self.nodeGraph.node[nodeID]['active_state'] == \
                    Active_State.negative_active:
                continue

            negativeActivationWeight = 0
            positiveActivationWeight = 0
            for parentNodeID in modifiedNodeGraph.predecessors(nodeID):
                parentNode = modifiedNodeGraph.node[parentNodeID]
                if parentNode['active_state'] == Active_State.negative_active:
                    negativeActivationWeight += 1  # This is weight.
                elif parentNode['active_state'] == Active_State.positive_active:
                    positiveActivationWeight += 1  # This is weight.
            # Do negative activation first, then do positive activation. If both works, positive activation dominant.
            if negativeActivationWeight >= modifiedNodeGraph.node[nodeID]['threshold']:
                modifiedNodeGraph.node[nodeID]['active_state'] = Active_State.negative_active
                isAnyChangesOfGraph = True
            if positiveActivationWeight >= modifiedNodeGraph.node[nodeID]['threshold']:
                modifiedNodeGraph.node[nodeID]['active_state'] = Active_State.positive_active
                # print(str(nodeID) + " activated. \n")
                isAnyChangesOfGraph = True
        self.nodeGraph = modifiedNodeGraph  #Apply single step changes to the current graph.
        return isAnyChangesOfGraph

    def get_Positive_and_Negative_Nodes_number(self) -> (int, int):
        positiveNumber, negativeNumber = 0, 0
        for nodeID in range(len(self.nodeGraph.nodes.items())):
            # nodeID += 1
            node = self.nodeGraph.node[nodeID]
            if node['active_state'] == Active_State.positive_active:
                positiveNumber += 1
            elif node['active_state'] == Active_State.negative_active:
                negativeNumber += 1
        return positiveNumber, negativeNumber

    def plot_graph(self):
        networkx.draw(self.nodeGraph)
        plt.show()

