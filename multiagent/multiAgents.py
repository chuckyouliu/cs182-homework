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
        
    #if distance is only 2 check for a wall between
    def blocked_by_wall(self, xy1, xy2, walls):
        if xy1[0] == xy2[0]:
            return walls[xy1[0]][xy1[1] + 1 if xy1[1] < xy2[1] else xy1[1] - 1]
        elif xy1[1] == xy2[1]:
            return walls[xy1[0] + 1 if xy1[0] < xy2[0] else xy1[0] - 1][xy1[1]]
        else:
            return False
    
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
        capsule_worth = 15
        food_worth = 5
        ghost_tolerance = 5
        walls = successorGameState.getWalls()        
        score = successorGameState.getScore() - currentGameState.getScore()
        score *= 10
        min_distance_food = newFood.width + newFood.height
        min_distance_capsule = min_distance_food
        new_capsules = successorGameState.getCapsules()
        old_capsules = currentGameState.getCapsules()   
        capsule_bonus = min_distance_food*capsule_worth*(len(old_capsules) - len(new_capsules))
        
        #go for the nearest capsule
        for capsule in new_capsules:
            dist = manhattanDistance(capsule, newPos)
            if dist < min_distance_capsule:
                if dist != 2 or not self.blocked_by_wall(capsule, newPos, walls):
                    min_distance_capsule = dist
        
        #go to nearest food taking into account walls for manhattanDistance
        for x in range(0, newFood.width):
            for y in range(0, newFood.height):
                if newFood[x][y]:
                    dist = manhattanDistance((x,y), newPos)
                    if dist < min_distance_food:
                        if not self.blocked_by_wall((x,y), newPos, walls):
                            min_distance_food = dist
        
        #check for ghosts nearby and reduce score based on manhattanDistance
        for i in range(0, len(newGhostStates)):
            ghost_coords = newGhostStates[i].getPosition()
            distance = manhattanDistance(ghost_coords, newPos)
            if distance < ghost_tolerance and newScaredTimes[i] == 0:
                score -= (ghost_tolerance - distance)*capsule_worth

        #make sure min_distances are not the starting numbers
        if min_distance_food == newFood.width + newFood.height:
            min_distance_food = -1
        if min_distance_capsule == newFood.width + newFood.height:
            min_distance_capsule = -1
        
        return score - min_distance_food*food_worth - min_distance_capsule*capsule_worth + capsule_bonus

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
        """
        "*** YOUR CODE HERE ***"  
        return self.pacman_helper(self.evaluationFunction, self.depth, gameState)["action"]
    
    def pacman_helper(self, evalFn, depth, gameState):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return {"score": evalFn(gameState), "action": Directions.STOP}
        else:
            pac_actions = gameState.getLegalActions(0)
            move = {"score": self.ghost_helper(evalFn, depth, gameState.generateSuccessor(0, pac_actions[0]), 1),
                    "action": pac_actions[0]}
            for i in range(1, len(pac_actions)):
                score = self.ghost_helper(evalFn, depth, gameState.generateSuccessor(0, pac_actions[i]), 1)
                if score > move["score"]:
                    move = {"score": score,
                            "action": pac_actions[i]}
            return move
    
    def ghost_helper(self, evalFn, depth, gameState, ghost_index):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return evalFn(gameState)
        else:
            ghost_actions = gameState.getLegalActions(ghost_index)
            if ghost_index < gameState.getNumAgents() - 1:
                score = self.ghost_helper(evalFn, depth, gameState.generateSuccessor(ghost_index, ghost_actions[0]), ghost_index+1)          
                for action_index in range(1, len(ghost_actions)):
                    score = min(self.ghost_helper(evalFn, depth, gameState.generateSuccessor(ghost_index, ghost_actions[action_index]), ghost_index+1), score)
                return score   
            else:
                score = self.pacman_helper(evalFn, depth-1, gameState.generateSuccessor(ghost_index, ghost_actions[0]))["score"]
                for action_index in range(1, len(ghost_actions)):
                    score = min(score, self.pacman_helper(evalFn, depth-1, gameState.generateSuccessor(ghost_index, ghost_actions[action_index]))["score"])
                return score


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.pacman_helper(self.evaluationFunction, self.depth, gameState, -float("inf"), float("inf"))["action"]
    
    def pacman_helper(self, evalFn, depth, gameState, alpha, beta):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return {"score": evalFn(gameState), "action": Directions.STOP}
        else:
            pac_actions = gameState.getLegalActions(0)
            move = {"score": -float("inf"), "move": None}
            for action in pac_actions:
                score = self.ghost_helper(evalFn, depth, gameState.generateSuccessor(0, action), 1, alpha, beta)
                if score > move["score"]:
                    move = {"score": score,
                            "action": action}
                    if score > beta:
                        return move
                    alpha = max(alpha, move["score"])
                    
            return move
    
    def ghost_helper(self, evalFn, depth, gameState, ghost_index, alpha, beta):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return evalFn(gameState)
        else:
            ghost_actions = gameState.getLegalActions(ghost_index)
            if ghost_index < gameState.getNumAgents() - 1:
                score = float("inf")               
                for action in ghost_actions:
                    score = min(self.ghost_helper(evalFn, depth, gameState.generateSuccessor(ghost_index, action), ghost_index+1, alpha, beta), score)
                    if score < alpha:
                        return score
                    beta = min(beta, score)
                return score   
            else:
                score = float("inf")             
                for action in ghost_actions:
                    score = min(score, self.pacman_helper(evalFn, depth-1, gameState.generateSuccessor(ghost_index, action), alpha, beta)["score"])
                    if score < alpha:
                        return score
                    beta = min(beta, score)
                return score

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
        return self.pacman_helper(self.evaluationFunction, self.depth, gameState)["action"]
    
    def pacman_helper(self, evalFn, depth, gameState):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return {"score": evalFn(gameState), "action": Directions.STOP}
        else:
            pac_actions = gameState.getLegalActions(0)
            move = {"score": self.ghost_helper(evalFn, depth, gameState.generateSuccessor(0, pac_actions[0]), 1),
                    "action": pac_actions[0]}
            for i in range(1, len(pac_actions)):
                score = self.ghost_helper(evalFn, depth, gameState.generateSuccessor(0, pac_actions[i]), 1)
                if score > move["score"]:
                    move = {"score": score,
                            "action": pac_actions[i]}
            return move
    
    def ghost_helper(self, evalFn, depth, gameState, ghost_index):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return evalFn(gameState)
        else:
            ghost_actions = gameState.getLegalActions(ghost_index)
            if ghost_index < gameState.getNumAgents() - 1:
                score = 0.
                for action in ghost_actions:
                    score += self.ghost_helper(evalFn, depth, gameState.generateSuccessor(ghost_index, action), ghost_index+1)
                return score/len(ghost_actions)
            else:
                score = 0.
                for action in ghost_actions:
                    score += self.pacman_helper(evalFn, depth-1, gameState.generateSuccessor(ghost_index, action))["score"]
                return score/len(ghost_actions)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

