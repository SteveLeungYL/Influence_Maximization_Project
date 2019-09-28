"""
Author: Yu Liang.
Data Structure file for Fake News Diffusion project.

"""
from enum import Enum
import numpy as np
import copy
from Global_Variables import *

class Active_State(Enum):
    not_active = 0
    negative_active = -1
    positive_active = 1

class Node:
    nodeID:int = 0
    parentNodeID = dict() #The edge collection between current node the next node. The value is the weight information.
    active_state = Active_State.not_active
    active_threshold = 1

    def __init__(self, nodeID:int, active_state = Active_State.not_active, active_threshold = active_Threshold, nextNodeID = dict()):
        self.nodeID = nodeID
        self.active_state = active_state
        self.active_threshold = active_threshold
        self.parentNodeID = nextNodeID

    def add_Parent_Node(self, parentNodeID:int, weight:float):
        if parentNodeID not in self.parentNodeID:
            self.parentNodeID[parentNodeID] = weight
        else:
            raise ValueError("Duplicated setting for target node weight. Errors when adding target node id.")


class Graph:
    nodeDict = dict() # {nodeID:Node}

    def __init__(self, nodeList: [Node] = [], csvFile:str = "", nodeDict = dict()):
        for node in nodeList:
            nodeID = node.nodeID
            if nodeID not in self.nodeDict:
                self.nodeDict[nodeID] = node
            else:
                raise ValueError("Have duplicated node ID inside the node list structure. Error throw when "
                                 "initializing the Graph class.")
        if csvFile != "":
            self.read_from_csv(csvFile=csvFile)

        if nodeDict != dict():
            self.nodeDict = copy.deepcopy(nodeDict)

    def copy_graph(self):
        return Graph(nodeDict=self.nodeDict)

    def read_from_csv(self, csvFile: str):
        node_data = np.genfromtxt(csvFile, delimiter=' ')
        sourceNodeIDList = node_data[:, 0]
        targetNodeIDList = node_data[:, 1]
        # weight = node_data[:, 2] # No weight data in current sample file yet.
        weight = len(sourceNodeIDList) * [1]

        for i in range(len(sourceNodeIDList)):
            if targetNodeIDList[i] == sourceNodeIDList[i]:
                raise ValueError("Source Node ID equals to Target Node ID. Error.")
            # Set up source node and target node mentioned in the input csv file.
            if sourceNodeIDList[i] not in self.nodeDict:
                newNode = Node(nodeID=sourceNodeIDList[i], nextNodeID=dict())
                self.nodeDict[sourceNodeIDList[i]] = newNode
            if targetNodeIDList[i] not in self.nodeDict:
                newNode = Node(targetNodeIDList[i], nextNodeID=dict())
                self.nodeDict[targetNodeIDList[i]] = newNode
            # Set up node connections with weight.
            targetNode = self.nodeDict[targetNodeIDList[i]]
            targetNode.add_Parent_Node(parentNodeID=sourceNodeIDList[i], weight=weight[i])

    def get_node(self, nodeID:int) -> Node:
        if nodeID not in self.nodeDict:
            node = self.nodeDict[nodeID]
        else:
            raise ValueError("Cannot find nodeID inside the Graph.")
        return node

    def try_activate_single_step(self) -> bool:
        isAnyChangesOfGraph = False

        modifiedNodeDict = copy.deepcopy(self.nodeDict) # Deep copy, changes on the modified node will not influence
        # the original graph. Making sure the single step behavior.
        for nodeID in self.nodeDict:
            node = self.nodeDict[nodeID]
            modifiedNode = modifiedNodeDict[nodeID]
            if node.active_state == Active_State.positive_active or node.active_state == Active_State.negative_active:
                continue
            negativeActivationWeight = 0
            positiveActivationWeight = 0
            for parentNodeID in node.parentNodeID:
                parentNode = self.nodeDict[parentNodeID]
                if parentNode.active_state == Active_State.negative_active:
                    negativeActivationWeight += node.parentNodeID[parentNodeID] # This is weight.
                elif parentNode.active_state == Active_State.positive_active:
                    positiveActivationWeight += node.parentNodeID[parentNodeID] # This is weight.
            # Do negative activation first, then do positive activation. If both works, positive activation dominant.
            if negativeActivationWeight >= node.active_threshold:
                modifiedNode.active_state = Active_State.negative_active
                isAnyChangesOfGraph = True
            if positiveActivationWeight >= node.active_threshold:
                modifiedNode.active_state = Active_State.positive_active
                # print(str(nodeID) + " activated. \n")
                isAnyChangesOfGraph = True
        self.nodeDict = modifiedNodeDict  #Apply single step changes to the current graph.
        return isAnyChangesOfGraph

    def get_Positive_and_Negative_Nodes_number(self) -> (int, int):
        positiveNumber, negativeNumber = 0, 0
        for nodeID in self.nodeDict:
            node = self.nodeDict[nodeID]
            if node.active_state == Active_State.positive_active:
                positiveNumber += 1
            elif node.active_state == Active_State.negative_active:
                negativeNumber += 1
        return positiveNumber, negativeNumber
