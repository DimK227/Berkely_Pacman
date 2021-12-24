# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    from util import Stack

    path1=[]
    visited=set()
    fringe = Stack()                                                            #DFS is implemented with stack
    if problem.isGoalState(problem.getStartState()):                            #If we reach at goal state return the path(empty in this case)
        return []
    fringe.push((problem.getStartState(),[]));                                  #Push the initial state to the fringe
    while(True):
        if fringe.isEmpty():                                                    #If fringe is empty there is no solution
            return []
        node,path1 = fringe.pop()                                               #Pop a node and its path from the finge
        visited.add(node);                                                      #Visit the node

        if problem.isGoalState(node):                                           #If we reach at goal state return the path
            return path1
        successors = problem.getSuccessors(node)                                #Get the successors of the node
        for i in successors:                                                    #For each successor
            if i[0] not in visited:                                             #If we haven't visited this node
                path2 = path1 + [i[1]]                                          #Extend the path
                fringe.push((i[0],path2))                                       #Push the new data to the fringe

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    from util import Queue
    path1=[]
    visited=[]
    fringe = Queue()                                                            #DFS is implemented with queue
    if problem.isGoalState(problem.getStartState()):                            #If we reach at goal state return the path(empty in this case)
        return []
    fringe.push((problem.getStartState(),[]));                                  #Push the initial state to the fringe
    while(True):
        if fringe.isEmpty():                                                    #If fringe is empty there is no solution
            return []
        node,path1 = fringe.pop()                                               #Pop a node and its path from the finge
        visited.append(node)                                                    #Visit the node
        if problem.isGoalState(node):                                           #If we reach at goal state return the path
            return path1
        successors = problem.getSuccessors(node)                                #Get the successors of the node
        for i in successors:                                                    #For each successor
            if i[0] not in visited:                                             #If we haven't visited this node
                visited.append(i[0])                                            #In bfs we visit the successor nodes immediately
                path2 = path1 + [i[1]]                                          #Extend the path
                fringe.push((i[0],path2))                                       #Push the new data to the fringe
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    fringe = PriorityQueue()                                                    #UCS is implemented with priority queue (priority will be the total cost of a path)
    visited = set()
    start = problem.getStartState()
    if problem.isGoalState(start):                                              #If we reach at goal state return the path(empty in this case)
        return []
    fringe.push((start,[],0),0)                                                 #Push the initial state to the fringe
    while(True):
        if fringe.isEmpty():                                                    #If fringe is empty there is no solution
            return []

        node,path1,cost = fringe.pop()                                          #Pop a node its path and the cost of this path from the finge
        if problem.isGoalState(node):                                           #If we reach at goal state return the path
            return path1
        if node not in visited:                                                 #If we haven't visited the node yet
            visited.add(node)                                                    #Visit it
            successors = problem.getSuccessors(node)                            #Get the successors of the node
            for succ in successors:                                             #For each successor
                path2 = path1 + [succ[1]]                                       #Extend the path
                total_cost = problem.getCostOfActions(path2)                    #Compute the priority
                fringe.push((succ[0], path2, total_cost), total_cost)           #Push the new data to the fringe
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """

    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    fringe = PriorityQueue()                                                    #A* is implemented with priority queue(priority will be the sum of cost and heuristic value)
    visited = []
    start = problem.getStartState()                                             #Get the initial state of the problem
    if problem.isGoalState(start):                                              #If we reach at goal state return the path(empty in this case)
        return []
    fringe.push((start,[],0+heuristic(start,problem)),0+heuristic(start,problem))#Push the initial state to the fringe
    while(True):
        if fringe.isEmpty():                                                    #If fringe is empty there is no solution
            return []

        node,path1,cost = fringe.pop()                                          #Pop a node its path and the cost of this path from the finge
        if problem.isGoalState(node):                                           #If we reach at goal state return the path
            return path1

        if node not in visited:                                                 #If we haven't visited the node yet
            visited.append(node)                                              #Visit it
            successors = problem.getSuccessors(node)                            #Get the successors of the node
            for succ in successors:                                             #For each successor
                path2 = path1 + [succ[1]]                                       #Extend the path
                total_cost = problem.getCostOfActions(path2)                    #Compute the priority
                fringe.push((succ[0], path2, total_cost+heuristic(succ[0],problem)), total_cost+heuristic(succ[0],problem))     #Push the new data to the fringe
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch