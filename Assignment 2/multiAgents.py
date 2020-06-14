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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        prevFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        min_dist_food = -1
        foodList = newFood.asList()

        for i in foodList:
            dist = util.manhattanDistance(newPos, i)
            if min_dist_food >= dist or min_dist_food == -1:
                min_dist_food = dist

        ghost_close = 0
        ghost_dist = 1
        for j in successorGameState.getGhostPositions():
            dist = util.manhattanDistance(newPos, j)
            ghost_dist += dist
            if dist <= 1:
                ghost_close += 1

        return (1 / float(min_dist_food)) + successorGameState.getScore() - ghost_close - (1 / float(ghost_dist)) 
        

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
        def findMin(gameState, depth, agentIndex):
          minimum = ["", float("inf")]
          
          if not gameState.getLegalActions(agentIndex):
            return self.evaluationFunction(gameState)

          for i in gameState.getLegalActions(agentIndex):
            current = minOrMax(gameState.generateSuccessor(agentIndex, i), depth, agentIndex + 1)

            if type(current) is not list:
              temp = current
            else:
              temp = current[1]
            if temp < minimum[1]:
              minimum = [i, temp]

          return minimum

        def findMax(gameState, depth, agentIndex):
          maximum = ["", -float("inf")]

          if not gameState.getLegalActions(agentIndex):
            return self.evaluationFunction(gameState)

          for i in gameState.getLegalActions(agentIndex):
            current = minOrMax(gameState.generateSuccessor(agentIndex, i), depth, agentIndex + 1)

            if type(current) is not list:
              temp = current
            else:
              temp = current[1]
            if temp > maximum[1]:
              maximum = [i, temp]

          return maximum


        def minOrMax(gameState, depth, agentIndex):
          if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
            depth += 1

          if (depth == self.depth or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
          elif (agentIndex == 0):
            return findMax(gameState, depth, agentIndex)
          else:
            return findMin(gameState, depth, agentIndex)

        actions = minOrMax(gameState, 0, 0)
        return actions[0]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def minValue(gameState, depth, agentIndex, a, b):
          minimum = ["", float("inf")]

          if not gameState.getLegalActions(agentIndex):
            return self.evaluationFunction(gameState)

          for i in gameState.getLegalActions(agentIndex):
            current = minOrMax(gameState.generateSuccessor(agentIndex, i), depth, agentIndex + 1, a, b)

            if type(current) is not list:
              temp = current
            else:
              temp = current[1]

            if temp < minimum[1]:
              minimum = [i, temp]
            if temp < a:
              return [i, temp]
            b = min(b, temp)

          return minimum

        def maxValue(gameState, depth, agentIndex, a, b):
          maximum = ["", -float("inf")]

          if not gameState.getLegalActions(agentIndex):
            return self.evaluationFunction(gameState)

          for i in gameState.getLegalActions(agentIndex):
            current = minOrMax(gameState.generateSuccessor(agentIndex, i), depth, agentIndex + 1, a, b)

            if type(current) is not list:
              temp = current
            else:
              temp = current[1]

            if temp > maximum[1]:
              maximum = [i, temp]
            if temp > b:
              return [i, temp]
            a = max(a, temp)

          return maximum

        def minOrMax(gameState, depth, agentIndex, a, b):
          if agentIndex >= gameState.getNumAgents():
              depth += 1
              agentIndex = 0

          if (depth == self.depth or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
          elif (agentIndex == 0):
            return maxValue(gameState, depth, agentIndex, a, b)
          else:
            return minValue(gameState, depth, agentIndex, a, b)

        actionsList = minOrMax(gameState, 0, 0, -float("inf"), float("inf"))
        return actionsList[0]


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

        def expectFinder(gameState, depth, agentIndex):
            ghost_act = gameState.getLegalActions(agentIndex)
            probability = 1.0 / len(ghost_act)
            expectList = ["", 0]

            if not ghost_act:
                return self.evaluationFunction(gameState)

            for i in ghost_act:
                current = expectimax(gameState.generateSuccessor(agentIndex, i), depth, agentIndex + 1)

                if type(current) is list:
                    temp = current[1]
                else:
                    temp = current

                expectList[0] = i
                expectList[1] += temp * probability

            return expectList

        def maxValue(gameState, depth, agentIndex):
            actions = gameState.getLegalActions(agentIndex)
            maximum = ["", -float("inf")]

            if not actions:
                return self.evaluationFunction(gameState)

            for i in actions:
                current = expectimax(gameState.generateSuccessor(agentIndex, i), depth, agentIndex + 1)

                if type(current) is not list:
                    temp = current
                else:
                    temp = current[1]

                if temp > maximum[1]:
                    maximum = [i, temp]

            return maximum

        def expectimax(gameState, depth, agentIndex):
            if agentIndex >= gameState.getNumAgents():
                depth += 1
                agentIndex = 0

            if (depth == self.depth or gameState.isWin() or gameState.isLose()):
                return self.evaluationFunction(gameState)
            elif (agentIndex == 0):
                return maxValue(gameState, depth, agentIndex)
            else:
                return expectFinder(gameState, depth, agentIndex)

        newList = expectimax(gameState, 0, 0)
        return newList[0]
      

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did> 

      I calculated the distances from the pacman to the ghosts. 
      At the same time I am also checking for the proimity of the ghosts around the pacman
      at a distance of 1 all around. Then in the next part I get the number of available capsules.
      Finally combine all the calculations obtained.
    """
    "*** YOUR CODE HERE ***"
    foodList = currentGameState.getFood().asList()
    min_dist_food = -1
    pos_next = currentGameState.getPacmanPosition()

    for i in foodList:
      dist = util.manhattanDistance(pos_next, i)
      if min_dist_food >= dist or min_dist_food == -1:
        min_dist_food = dist

    ghost_dist = 1
    ghost_close = 0

    for j in currentGameState.getGhostPositions():
      dist = util.manhattanDistance(pos_next, j)
      ghost_dist += dist
      if dist <= 1:
        ghost_close += 1

    lenCapsules = len(currentGameState.getCapsules())

    return currentGameState.getScore() + (1 / float(min_dist_food)) - (1 / float(ghost_dist)) - ghost_close - lenCapsules

# Abbreviation
better = betterEvaluationFunction

