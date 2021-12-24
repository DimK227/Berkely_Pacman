# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"

        newFoodList = newFood.asList()
                                                                                #Take food as list
        currentFoodList = currentGameState.getFood().asList()

        capsulesList = successorGameState.getCapsules()
                                                                                #Get the capsules
        NumberOfCapsules = len(capsulesList)

        newNumberOfFood = len(newFoodList)
                                                                                #Take the number of food dots
        currentNumberOfFood = len(currentFoodList)

        currentGhostList = currentGameState.getGhostPositions()
                                                                                #Take the ghosts
        newGhostList = successorGameState.getGhostPositions()

        ghostDistances = []
        foodDistances = []
        score = 0

        if newNumberOfFood == 0: return 9999                                    #If no food we win

        if newNumberOfFood < currentNumberOfFood:                               #If the new food dots are less than the current food dots
            score+=300
        else:
            score-= 100

        if action==Directions.STOP:                                             #Never stop!
            score -= 10

        if newPos in capsulesList:                                              #If we are in a capsule great!
            score += 100

        if len(newScaredTimes) > 0:                                             #If the ghosts are scared you must run
            if action==Directions.STOP:
                score -= 100


        for ghost in newGhostList:
             if util.manhattanDistance(ghost,newPos) == 0:                      #If we are in ghost we lose
                 return -10000
             if util.manhattanDistance(ghost,newPos) <= 5:                      #If the distance is less than 5 it's bad
                 score -= 20
             else:                                                              #else it's good!
                score+=50
        return score

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()

        def MaxValue(gameState,depth):
            actions = gameState.getLegalActions(0)                              #Take actions of pacman
            if gameState.isWin() or gameState.isLose() or depth+1 == self.depth:       #In these situations we are done
                return self.evaluationFunction(gameState)
            maximum = -float("inf")
            for a in actions:
                successor = gameState.generateSuccessor(0,a)
                maximum = max(MinValue(successor,depth+1,1), maximum)           #Find the max value
            return maximum

        def MinValue(gameState,depth,agent):
            actions = gameState.getLegalActions(agent)                          #Take actions of agent
            if gameState.isWin() or gameState.isLose():                         #In these situations we are done
                return self.evaluationFunction(gameState)
            minimum = float("inf")
            for a in actions:
                successor = gameState.generateSuccessor(agent,a)
                if agent == gameState.getNumAgents()-1:                         #If we have checked all agents
                    minimum = min(MaxValue(successor,depth), minimum)
                else:
                    minimum = min(MinValue(successor,depth,agent+1), minimum)
            return minimum

        #Deal with the root
        actions = gameState.getLegalActions(0)                                  #Get all the actions
        score = -float("inf")
        for a in actions:
            successor = gameState.generateSuccessor(0,a)
            value = MinValue(successor,0,1)                                     #Next level is min-level
            if value > score:
                minimaxDesicion = a
                                                                                #Find the minimaxDesicion
                score = value
        return minimaxDesicion
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def MaxValue(gameState,depth,alpha,beta):
            actions = gameState.getLegalActions(0)
            if gameState.isWin() or gameState.isLose() or depth+1 == self.depth:
                return self.evaluationFunction(gameState)
            maximum = -float("inf")
            for a in actions:
                successor = gameState.generateSuccessor(0,a)
                maximum = max(MinValue(successor,depth+1,1,alpha,beta), maximum)
                if (maximum > beta):                                            #In this case we are done
                    return maximum
                alpha = max(alpha, maximum)                                     #Fix the alpha
            return maximum

        def MinValue(gameState,depth,agent,alpha,beta):
            actions = gameState.getLegalActions(agent)
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            minimum = float("inf")
            for a in actions:
                successor = gameState.generateSuccessor(agent,a)
                if agent == gameState.getNumAgents()-1:
                    minimum = min(MaxValue(successor,depth,alpha,beta), minimum)
                else:
                    minimum = min(MinValue(successor,depth,agent+1,alpha,beta), minimum)
                if minimum < alpha:                                             #In this case we are done
                    return minimum
                beta = min(beta, minimum)                                       #Fix the beta
            return minimum


        actions = gameState.getLegalActions(0)
        score = -float("inf")
        alpha = -float("inf")
        beta = float("inf")
        for a in actions:
            successor = gameState.generateSuccessor(0,a)
            value = MinValue(successor,0,1,alpha,beta)
            if value > score:
                AlphaBetaDesicion = a                                           #Find the decision of AlphaBeta prunning
                score = value
                alpha = value
        return AlphaBetaDesicion
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def MaxValue(gameState,depth):
            actions = gameState.getLegalActions(0)
            if gameState.isWin() or gameState.isLose() or depth+1 == self.depth:
                return self.evaluationFunction(gameState)
            maximum = -float("inf")
            for a in actions:
                successor = gameState.generateSuccessor(0,a)
                maximum = max(ExpectedValue(successor,depth+1,1), maximum)
            return maximum

        def ExpectedValue(gameState,depth,agent):
            actions = gameState.getLegalActions(agent)
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            minimum = float("inf")
            final = 0
            if len(actions) == 0:
                return 0
            for a in actions:
                successor = gameState.generateSuccessor(agent,a)
                if agent == gameState.getNumAgents()-1:
                    minimum = MaxValue(successor,depth)
                    final+=minimum
                else:
                    minimum = ExpectedValue(successor,depth,agent+1)
                    final+=minimum
            return final/len(actions)                                           #This is the expected value

        actions = gameState.getLegalActions(0)
        score = -float("inf")
        for a in actions:
            successor = gameState.generateSuccessor(0,a)
            value = ExpectedValue(successor,0,1)
            if value > score:
                expectedDesicion = a                                            #Find the ecpected decision
                score = value
        return expectedDesicion
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    #Take all the necessary information
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood().asList()
    ghosts = currentGameState.getGhostPositions()
    capsules = currentGameState.getCapsules()
    newGhostStates = currentGameState.getGhostStates()
    ScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    score = 0
    if currentGameState.isWin():                                                #We Win!
        return float("inf")
    if currentGameState.isLose():                                               #We lose!
        return float("-inf")

    ghostDistances = []
    foodDistances = []
    capsulesDistances = []

    for ghost in ghosts:                                                        #Find the manhattan distance between ghost and pacman
        ghostDistances.append(util.manhattanDistance(pos,ghost))

    for f in food:                                                              #Find the manhattan distance between food and pacman
        foodDistances.append(util.manhattanDistance(pos,f))

    for capsule in capsules:                                                    #Find the manhattan distance between capsule and pacman
        capsulesDistances.append(util.manhattanDistance(pos,capsule))

    score+=sum(foodDistances)*(-10)

    score+=sum(ghostDistances)*(50)                                             #Fix the scores

    score+=sum(capsulesDistances)*(-10)



    if sum(ScaredTimes) > 0:                                                    #If the ghosts are scared
        score += sum(ScaredTimes) + (-10 * len(capsules)) + (-10 * sum(ghostDistances))
    else:
        score+=  sum(ghostDistances) + len(capsules)



    return score



    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction