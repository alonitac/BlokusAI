from board import Board
from search import SearchProblem, Node, a_star_search
import util
import numpy as np


class BlokusFillProblem(SearchProblem):
    """
    A one-player Blokus game as a search problem.
    This problem is implemented for you. You should NOT change it!
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.expanded = 0

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        """
        state: Search state
        Returns True if and only if the state is a valid goal state
        """
        return not any(state.pieces[0])

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, 1) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)



#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################
class BlokusCornersProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=[(0, 0)]):
        self.targets = targets.copy()
        self.expanded = 0
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        return -1 not in [state.get_position(0, 0),
                        state.get_position(0, state.board_w - 1),
                        state.get_position(state.board_h - 1, 0),
                        state.get_position(state.board_h - 1, state.board_w - 1)]

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return sum([move.piece.get_num_tiles() for move in actions])


def blokus_corners_heuristic(state, problem):
    tiles = np.matrix(np.where(state.state == 0)).T
    corners = [(0, 0), (0, state.board_w - 1), (state.board_h - 1, 0), (state.board_w - 1, state.board_h - 1)]
    total = 0
    for target in corners:
        distance_components = abs(tiles - target)  # for matrix notation of Manhattan distance
        manhattan_dist = distance_components[:, 0] + distance_components[:, 1]
        md_array = np.squeeze(np.array(manhattan_dist))
        min_dist = np.min(manhattan_dist)

        condition = np.matrix(np.where(md_array == min_dist)).T
        min_components = distance_components[condition].tolist()

        if min_dist == 1:
            min_dist = float(np.inf)
        elif min_dist > 1:
            if any(t in min_components for t in [[[min_dist, 0]], [[0, min_dist]]]):
                min_dist += 1
            else:
                min_dist -= 1
        else:
            min_dist = float(min_dist)

        total += min_dist

    return total


class BlokusCoverProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=[(0, 0)]):
        self.targets = targets.copy()
        self.expanded = 0
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        return -1 not in [state.get_position(y, x) for x, y in self.targets]

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return sum([move.piece.get_num_tiles() for move in actions])


def blokus_cover_heuristic(state, problem):
    tiles = np.matrix(np.where(state.state == 0)).T
    total = 0
    for target in problem.targets:
        distance_component = abs(tiles - target)  # for matrix notation of Manhattan distance
        manhattan_dist = distance_component[:, 0] + distance_component[:, 1]
        md_array = np.squeeze(np.array(manhattan_dist))
        min_dist = np.min(manhattan_dist)
        condition = np.matrix(np.where(md_array == min_dist)).T
        min_components = distance_component[condition].tolist()

        if min_dist == 1:
            min_dist = float(np.inf)

        elif min_dist > 1:
            if any(t in min_components for t in [[min_dist, 0], [0, min_dist]]):
                min_dist += 1
            else:
                min_dist -= 1

        total += min_dist
    return total


class ClosestLocationSearch:
    """
    In this problem you have to cover all given positions on the board,
    but the objective is speed, not optimality.
    """
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=[(0, 0)]):
        self.targets = targets.copy()
        self.expanded = 0
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.starting_point = starting_point
        self.target = self.find_closest_target(self.board, self.starting_point)
        self.clean_board = Board(board_w, board_h, 1, piece_list, starting_point)

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def get_successors(self, state):
        """
        state: Search state
        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]

    def is_goal_state(self, state):
        return -1 not in [state.get_position(y, x) for x, y in self.targets]

    def find_closest_target(self, state, starting_point):
        remaining_targets = [(x, y) for x, y in self.targets if state.get_position(y, x) == -1]
        if not remaining_targets:
            return -1, -1
        distances = np.zeros(len(remaining_targets))
        for i, target in enumerate(remaining_targets):
            distance_components = (starting_point[0] - target[0], starting_point[1] - target[1])
            distance = abs(distance_components[0]) + abs(distance_components[1])
            distances[i] = distance
        idx = np.argmin(distances)
        return remaining_targets[idx]

    def heuristic(self, state, target):
        tiles = np.matrix(np.where(state.state == 0)).T
        distance_component = abs(tiles - target)  # for matrix notation of Manhattan distance
        manhattan_dist = distance_component[:, 0] + distance_component[:, 1]
        md_array = np.squeeze(np.array(manhattan_dist))
        min_dist = np.min(manhattan_dist)
        condition = np.matrix(np.where(md_array == min_dist)).T
        min_components = distance_component[condition].tolist()

        if min_dist == 1:
            min_dist = float(np.inf)

        elif min_dist > 1:
            if any(t in min_components for t in [[min_dist, 0], [0, min_dist]]):
                min_dist += 1
            else:
                min_dist -= 1
        return min_dist

    def solve(self):
        """
        This method should return a sequence of actions that covers all target locations on the board.
        This time we trade optimality for speed.
        Therefore, your agent should try and cover one target location at a time. Each time, aiming for the closest uncovered location.
        You may define helpful functions as you wish.
        Probably a good way to start, would be something like this --
        current_state = self.board.__copy__()
        backtrace = []
        while ....
            actions = set of actions that covers the closets uncovered target location
            add actions to backtrace
        return backtrace
        """
        fringe = util.PriorityQueue()
        start_state = self.get_start_state()
        fringe.push(Node(start_state, None, None, 0,
                         params={'target': self.find_closest_target(start_state, self.starting_point)}), 0)
        closed = {}

        while not fringe.isEmpty():
            current_node = fringe.pop()

            if self.is_goal_state(current_node.state):
                print('Reach Goal')
                return current_node.get_action_trace_back()
            if closed.get(current_node.state) is None:
                x, y = current_node.params['target']
                successors = self.get_successors(current_node.state)
                for successor, action, step_cost in successors:
                    cost_so_far = current_node.cost_so_far + step_cost
                    successor_target = (x, y)
                    if successor.get_position(y, x) != -1:
                        successor_target = self.find_closest_target(successor, (x, y))
                        cost_so_far = step_cost
                        if successor_target == (-1, -1):
                            return current_node.get_action_trace_back() + [action]

                    fringe.push(
                        Node(successor, action, current_node,
                             cost_so_far, params={'target': successor_target}),
                        cost_so_far + self.heuristic(successor, successor_target)
                    )

                    closed[current_node.state] = True

        print('Cannot solve the problem')
        return []


class MiniContestSearch:
    """
    In this problem you have to cover all given positions on the board.
    """
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=[(0, 0)]):
        self.targets = targets.copy()
        self.expanded = 0
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.starting_point = starting_point

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def get_successors(self, state):
        """
        state: Search state
        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]

    def is_goal_state(self, state):
        return -1 not in [state.get_position(y, x) for x, y in self.targets]

    def find_closest_target(self, state, starting_point):
        remaining_targets = [(x, y) for x, y in self.targets if state.get_position(y, x) == -1]
        if not remaining_targets:
            return -1, -1
        distances = np.zeros(len(remaining_targets))
        for i, target in enumerate(remaining_targets):
            distance_components = (starting_point[0] - target[0], starting_point[1] - target[1])
            distance = abs(distance_components[0]) + abs(distance_components[1])
            distances[i] = distance
        idx = np.argmin(distances)
        return remaining_targets[idx]

    def heuristic(self, state, targets):
        tiles = np.matrix(np.where(state.state == 0)).T
        total = 0
        for target in targets:
            distance_component = abs(tiles - target)  # for matrix notation of Manhattan distance
            manhattan_dist = distance_component[:, 0] + distance_component[:, 1]
            md_array = np.squeeze(np.array(manhattan_dist))
            min_dist = np.min(manhattan_dist)
            condition = np.matrix(np.where(md_array == min_dist)).T
            min_components = distance_component[condition].tolist()

            if min_dist == 1:
                min_dist = float(np.inf)

            elif min_dist > 1:
                if any(t in min_components for t in [[min_dist, 0], [0, min_dist]]):
                    min_dist += 1
                else:
                    min_dist -= 1

            total += min_dist
        return total

    def state_symmetry(self, state):
        """
        Returns all possible rotations and flips of the board.
        """
        variations = {}

        # rotate board
        for k in range(4):
            num_state = np.rot90(state.state, k=k)

            str_state = tuple(map(tuple, num_state)) # tuple(num_state) # self.state_to_string(num_state)
            if variations.get(str_state) is None:
                variations.update({str_state: True})
            else:
                pass

        # flip board and rotate the flipped board
        flipped_state = np.flip(num_state, axis=0)
        for k in range(4):
            num_state = np.rot90(flipped_state, k=k)
            str_state = tuple(map(tuple, num_state))
            if variations.get(str_state) is None:
                variations.update({str_state: True})
            else:
                pass

        return variations

    def solve(self):
        """
        This method returns a sequence of actions that covers all target locations on the board.
        """
        fringe = util.PriorityQueue()
        start_state = self.get_start_state()
        fringe.push(Node(start_state, None, None, 0), 0)
        closed = {}

        while not fringe.isEmpty():
            current_node = fringe.pop()
            variations = self.state_symmetry(current_node.state)

            if self.is_goal_state(current_node.state):
                print('Reach Goal')
                return current_node.get_action_trace_back()

            elif all(closed.get(key) is None for key in variations.keys()):
                # only expand node if none of its variations (rotations and flips) were discovered yet
                successors = self.get_successors(current_node.state)
                for successor, action, step_cost in successors:
                    cost_so_far = current_node.cost_so_far + step_cost
                    fringe.push(
                        Node(successor, action, current_node, cost_so_far),
                        cost_so_far + self.heuristic(successor, self.targets)
                    )

                    closed[list(variations.keys())[0]] = True

        print('Cannot solve the problem')
        return []
