# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

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
    [2nd Edition: p 75, 3rd Edition: p 87]

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    s = problem.getStartState()
    visited_states = [s]
    frontier = util.Stack()
    frontier.push((s, []))
    while not frontier.isEmpty():
        state_path = frontier.pop()
        if problem.isGoalState(state_path[0]):
            return state_path[1]
        visited_states.append(state_path[0])
        for successor in problem.getSuccessors(state_path[0]):
            if not successor[0] in visited_states:
                frontier.push((successor[0], state_path[1] + [successor[1]]))
    return []
    

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]
    """
    "*** YOUR CODE HERE ***"
    s = problem.getStartState()
    visited_states = [s]
    frontier = util.Queue()
    frontier.push((s, []))
    while not frontier.isEmpty():
        state_path = frontier.pop()
        if problem.isGoalState(state_path[0]):
            return state_path[1]
        for successor in problem.getSuccessors(state_path[0]):
            if not successor[0] in visited_states:
                frontier.push((successor[0], state_path[1] + [successor[1]]))
                visited_states.append(successor[0])
    return []

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    s = problem.getStartState()    
    #hashing costs of visited states in case we repeat a state with a lower cost
    str_key = False
    try:
        visited_states = {s: 0}
    except TypeError:
        visited_states = {str(s): 0}
        str_key = True
    frontier = util.PriorityQueueWithFunction(lambda x: x[2])
    frontier.push((s, [], 0))
    while not frontier.isEmpty():
        state_path = frontier.pop()
        if problem.isGoalState(state_path[0]):
            return state_path[1]
        for successor in problem.getSuccessors(state_path[0]):
            cost = state_path[2] + successor[2]
            successor_key = str(successor[0]) if str_key else successor[0]            
            if (not successor_key in visited_states) or cost < visited_states[successor_key]:
                frontier.push((successor[0], state_path[1] + [successor[1]], cost))
                visited_states[successor_key] = cost
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    s = problem.getStartState()
    cost_0 = heuristic(s, problem)
    #hashing costs of visited states in case we repeat a state with a lower cost
    str_key = False
    try:
        visited_states = {s: cost_0}
    except TypeError:
        visited_states = {str(s): cost_0}
        str_key = True
        
    frontier = util.PriorityQueueWithFunction(lambda x: x[2])
    frontier.push((s, [], cost_0))
    while not frontier.isEmpty():
        state_path = frontier.pop()
        if problem.isGoalState(state_path[0]):
            return state_path[1]
        for successor in problem.getSuccessors(state_path[0]):
            cost = state_path[2] - heuristic(state_path[0], problem) + successor[2] + heuristic(successor[0], problem)
            successor_key = str(successor[0]) if str_key else successor[0]            
            if (not successor_key in visited_states) or cost < visited_states[successor_key]:
                frontier.push((successor[0], state_path[1] + [successor[1]], cost))
                visited_states[successor_key] = cost
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
