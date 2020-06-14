"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    frontier = util.Stack()
    frontier.push( (problem.getStartState(), []) )
    exploredSet = []
    exploredSet.append( problem.getStartState() )
    next_state = problem.getStartState()

    while not frontier.isEmpty() and not problem.isGoalState(next_state):
        state, actions = frontier.pop()
        exploredSet.append(state)
        for i in problem.getSuccessors(state):           
            if i[0] not in exploredSet:
                next_state = i[0]
                next_action = i[1]
                frontier.push( (next_state, actions + [next_action]) )
               
    return actions + [next_action]
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    exploredSet = []
    exploredSet.append( problem.getStartState() )
    frontier = util.Queue()
    for i in problem.getSuccessors(problem.getStartState()):
        frontier.push(i + (i[1],))

    actions = []

    while not frontier.isEmpty():
        state,_,_, actions = frontier.pop()     
        
        if problem.isGoalState(state):   
            break
        
        if state not in exploredSet:
            for i in problem.getSuccessors(state):
                if i[0] not in exploredSet:
                    frontier.push(i + ((actions + "," + i[1]), ))
        
        exploredSet.append(state)
    return actions.split(",")

    util.raiseNotDefined()



def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"

    exploredSet = []
    exploredSet.append(problem.getStartState())
    frontier = util.PriorityQueue()

    for i in problem.getSuccessors(problem.getStartState()):
        frontier.push(i + (i[1],) + (i[2],), i[2])

    actions = []

    while not(frontier.isEmpty()):
        state,_,_, actions, cost = frontier.pop()
    
        if problem.isGoalState(state):   
            break

        if state not in exploredSet:
            for i in problem.getSuccessors(state):
                if i[0] not in exploredSet:
                    next_cost = i + (actions + "," + i[1],) + (cost + i[2],)
                    frontier.push(next_cost, cost + i[2])
        exploredSet.append(state)

    return actions.split(",")
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"

    exploredSet = []
    exploredSet.append(problem.getStartState())
    
    frontier = util.PriorityQueue()
    for i in problem.getSuccessors(problem.getStartState()):
        cost = i[2] + heuristic(i[0], problem)
        frontier.push(i + (i[1],) + (i[2],) + (heuristic(i[0], problem),), cost)

    actions = []

    while not(frontier.isEmpty()):
        state,_,_, actions, cost,_ = frontier.pop()
       
        if problem.isGoalState(state):   
            break

        if state not in exploredSet:
            for i in problem.getSuccessors(state):
                if i[0] not in exploredSet:
                    next_cost = cost + i[2] 
                    nextRoute = actions + "," + i[1]
                    frontier.push(i + (nextRoute,) + (next_cost,) + (heuristic(i[0], problem),), next_cost + heuristic(i[0], problem))
        exploredSet.append(state)

    return actions.split(",")
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
