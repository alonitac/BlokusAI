"""
In search.py, you will implement generic search algorithms
"""

import util


class Node:
    def __init__(self, state, action, parent, cost_so_far, params={}):
        self.action = action
        self.cost_so_far = cost_so_far
        self.parent = parent
        self.state = state
        self.params = params

    def get_action_trace_back(self):
        trace = []
        node = self
        while node.parent is not None:
            trace = [node.action] + trace
            node = node.parent

        return trace


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def depth_first_search(problem):
    fringe = util.Stack()
    start_state = problem.get_start_state()
    fringe.push(Node(start_state, None, None, 0))
    closed = {}

    while not fringe.isEmpty():
        current_node = fringe.pop()

        if problem.is_goal_state(current_node.state):
            print("Reach Goal")
            return current_node.get_action_trace_back()
        elif closed.get(current_node.state) is None:
            successors = problem.get_successors(current_node.state)
            for successor, action, step_cost in successors:
                cost_so_far = current_node.cost_so_far + step_cost
                fringe.push(Node(successor, action, current_node, cost_so_far))
                closed[current_node.state] = True
    return []


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    fringe = util.Queue()
    start_state = problem.get_start_state()
    fringe.push(Node(start_state, None, None, 0))
    closed = {}

    while not fringe.isEmpty():
        current_node = fringe.pop()

        if problem.is_goal_state(current_node.state):
            print("Reach Goal")
            return current_node.get_action_trace_back()
        elif closed.get(current_node.state) is None:
            successors = problem.get_successors(current_node.state)
            for successor, action, step_cost in successors:
                cost_so_far = current_node.cost_so_far + step_cost
                fringe.push(Node(successor, action, current_node, cost_so_far))
                closed[current_node.state] = True
    return []


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    """
    return a_star_search(problem, null_heuristic)


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    fringe = util.PriorityQueue()
    start_state = problem.get_start_state()
    fringe.push(Node(start_state, None, None, 0), 0)
    closed = {}

    while not fringe.isEmpty():
        current_node = fringe.pop()

        if problem.is_goal_state(current_node.state):
            print('Reach Goal')
            return current_node.get_action_trace_back()
        elif closed.get(current_node.state) is None:
            successors = problem.get_successors(current_node.state)
            for successor, action, step_cost in successors:
                cost_so_far = current_node.cost_so_far + step_cost
                fringe.push(
                    Node(successor, action, current_node, cost_so_far),
                    cost_so_far + heuristic(successor, problem)
                )

                closed[current_node.state] = True

    print('Cannot solve the problem')
    return []


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
