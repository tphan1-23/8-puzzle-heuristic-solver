# -*- coding: utf-8 -*-

"""----------------------------------------------------------------------------
# ------------------------------- #
#      a.3 the 8-puzzle           #
# ------------------------------- #
# Name: Thanh Phan
# Section: CSCI 3385
#
----------------------------------------------------------------------------"""

import heapq
import copy

# The following are used to generate start states:
from collections import deque
import random

goal_state = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]


def generate_random_start_w_fixed_depth(depth):
  """
  This works by starting from the goal state and basically doing BFS to reach
  all states at a particular depth. Once these states are found, one of them is
  # randomly selected to be the start state.
  """
  frontier = deque()
  visited = {str(goal_state)}
  depth_map = {0: [goal_state]}

  frontier.append((goal_state, 0))

  while frontier:
    state, d = frontier.popleft()

    if d == depth:
      break

    for action in get_actions(state):
      next_state = transition_model(state, action)

      if str(next_state) in visited:
        continue

      visited.add(str(next_state))
      frontier.append((next_state, d + 1))
      depth_map.setdefault(d + 1, []).append(next_state)

  if depth not in depth_map:
    raise ValueError("Depth too large for BFS horizon")

  return random.choice(depth_map[depth])


def goal_test(state):
  """
  # If state is the same as goal_state, then the function returns True. Otherwise,
  # it returns False.
  """
  if state == goal_state:
    return True
  else:
    return False


def print_state(state):
  """
  # Prints the state with some formatting.
  """
  print(f'{state[0][0]}|{state[0][1]}|{state[0][2]}')
  print('— — —')
  print(f'{state[1][0]}|{state[1][1]}|{state[1][2]}')
  print('— — —')
  print(f'{state[2][0]}|{state[2][1]}|{state[2][2]}\n')


def get_blank_pos(state):
  """
  # For the given state, returns a tuple describing the position of the blank
  # such that blank_pos[0] is the row index and blank_pos[1] is the column index.
  """
  for row_index, row in enumerate(state):
    if 0 in row:
      col_index = row.index(0)
      blank_pos = (row_index, col_index)
      return blank_pos


def get_actions(state):
  """
  # Returns the available actions that can be taken from state.
  """
  actions = ['u', 'd', 'l', 'r']  # ie up, down, left, right

  # First, we need to know the position of the blank.
  blank_pos = get_blank_pos(state)

  # If the blank is on the top row (row_index == 0), then 'u' will not be a possible action.
  # On the other hand, if the blank is on the bottom row (row_index == 2), then 's' will not
  # be a possible action.
  if blank_pos[0] == 0:
    actions.remove('u')
  elif blank_pos[0] == 2:
    actions.remove('d')

  # If the blank is in the left column (col_index == 0), then 'l' will not be possible.
  # Else, if it is in the right column (col_index == 2), then 'r' will not be possible.
  if blank_pos[1] == 0:
    actions.remove('l')
  elif blank_pos[1] == 2:
    actions.remove('r')

  return actions


def transition_model(state, action):
  """
  # Given the current state and an action, return the state that would result
  # by carrying out the action from the state.
  """
  blank_pos = get_blank_pos(state)

  next_state = copy.deepcopy(state)

  if action == 'u':
    # The tile that will be switched will have the same column as the blank,
    # but will be one row higher (i.e., blank_pos[0] - 1)
    swap_pos = (blank_pos[0] - 1, blank_pos[1])

  elif action == 'd':
    # The tile to swap is below the blank, so it is in row blank_pos[0] + 1
    swap_pos = (blank_pos[0] + 1, blank_pos[1])

  elif action == 'l':
    # The tile to swap is to the left of the blank, so it is in column blank_pos[1] - 1
    swap_pos = (blank_pos[0], blank_pos[1] - 1)

  elif action == 'r':
    # The tile to swap is to the right of the blank, so it is in column blank_pos[1] + 1
    swap_pos = (blank_pos[0], blank_pos[1] + 1)

  # swap_pos[0] == row index of where the blank is going
  # swap_pos[1] == col index of where the blank is going
  tile_to_swap = state[swap_pos[0]][swap_pos[1]]

  next_state[blank_pos[0]][blank_pos[1]] = tile_to_swap
  next_state[swap_pos[0]][swap_pos[1]] = 0

  return next_state


def breadth_first_search(start_state):

  # frontier is a list that we will base our priority queue on.
  frontier = []

  # This is where we will track how many nodes have been expanded which we can
  # use as a proxy measure for time complexity.
  expansion_count = 0

  # This is where we will keep up with states that have already been expanded,
  # with the idea of avoiding redundant node expansions and cycles.
  visited = set()

  # This implements a priority queue on frontier. For more info, see
  # https://docs.python.org/3/library/heapq.html
  heapq.heappush(frontier,
                (0, (start_state, [])))

  # For BFS, we can add a node to visited when it is generated (ie, added to
  # the frontier). This should prevent redundant paths. Python requires objects
  # to be hashable in order to be added to sets, so rather than add the 2d-array,
  # we will make it a string first.
  visited.add(str(start_state))

  # This while-loop will run until frontier is empty (ie, all nodes in the search
  # tree have been expanded) OR an expanded node passes the goal test.
  while frontier:

    # Pop the highest priority node off the frontier to expand.
    #    - curr_value is the score we use to determine priority. For BFS, this is
    # just the node's level on the search tree.
    #    - curr_node is a tuple of the form (curr_state, curr_path), which are
    # explained in the following lines.
    curr_value, curr_node = heapq.heappop(frontier)

    # curr_state is the state corresponding to the expanded node.
    # curr_path is the list of actions that define the path from the state of the
    # root node to curr_state. Remember that nodes in the search tree represent
    # paths.
    curr_state = curr_node[0]
    curr_path = curr_node[1]

    expansion_count += 1  # In other words,  x = x + 1

    if curr_state == goal_state:
      # If curr_state passes the goal test, then we have a solution!
      return curr_path, expansion_count

    # If it doesn't pass the goal test, we move on to generating child nodes, by
    # getting the available actions from the current state.
    curr_actions = get_actions(curr_state)

    # Generate child node from each action.
    for action in curr_actions:

      next_state = transition_model(curr_state, action)

      # If next_state is in visited, then we don't want to bother with it.
      if str(next_state) not in visited:

        # Otherwise, we want to generate the node in which case we need to know
        # the node's path (the parent path plus action) and the node's value
        # (the number of actions in its path, which is equivalent to its level
        # in the search tree).
        next_path = copy.deepcopy(curr_path)
        next_path.append(action)
        next_value = len(next_path)

        # Add the child node to the priority queue (our frontier) to generate it.
        heapq.heappush(frontier, (next_value, (next_state, next_path)))

        # Add the child node to visited.
        visited.add(str(next_state))


def h1(state):
  """
  # Implementation of heuristic h_1 from class.
  """
  tiles_out_of_place = 0

  for row_i, row in enumerate(goal_state):
    for col_i, correct_tile in enumerate(row):
      # print(f'row_i: {row_i}, row: {row}, col_i: {col_i}, correct_tile: {correct_tile}')

      if correct_tile != state[row_i][col_i]:
        tiles_out_of_place += 1

  return tiles_out_of_place
  

def h2(state):
  """
  You will need to implement heuristic 2 here. Be sure to remove 'pass' when you add your code. 
  """
  distance = 0

  for r in range(3):
    for c in range(3):
      tile = state[r][c]
      if tile == 0:
        continue
      goal_r = (tile - 1) // 3
      goal_c = (tile - 1) % 3
      distance += abs(r - goal_r) + abs(c - goal_c)

  return distance

def greedy_search(start_state, heuristic):
  """
  # This implementation of greedy search uses a priority queue to keep up with the
  # search tree. The heapq package uses a priority queue that returns the item with
  # the smallest value first, which is what we want when actions have costs (rather than rewards).
  # For more on heapq, see https://docs.python.org/3/library/heapq.html.
  #
  # Greedy search algorithm: choose the cheapest node from the frontier based on
  # heuristic, and expand that node next.
  """
  visited = set()
  frontier = []

  expansion_count = 0

  # First, we generate the root node of the search tree: start_state. Note that
  # instead of using search tree depth for the value, we now use the estimated
  # forward cost according to the heuristic.
  heapq.heappush(frontier,
                 (heuristic(start_state), (start_state, [])))
  
  visited.add(str(start_state))


  """
  Your code will start below. Be sure to uncomment 'while frontier:' and then
  fill in the rest of the function.
  """
  # As long as the frontier is not empty, this loop will continue.
  
  while frontier:
    curr_h, curr_node = heapq.heappop(frontier)
    curr_state, curr_path = curr_node
    
    expansion_count += 1

    if goal_test(curr_state):
        return curr_path, expansion_count
    
    for action in get_actions(curr_state):
        next_state = transition_model(curr_state, action)
        
        if str(next_state) not in visited:
            next_path = copy.deepcopy(curr_path)
            next_path.append(action)

            priority = heuristic(next_state)
            
            heapq.heappush(frontier, (priority, (next_state, next_path)))
            visited.add(str(next_state))

def a_star_search(start_state, heuristic):
    visited = set()
    frontier = []

    expansion_count = 0

    heapq.heappush(frontier,
                   (heuristic(start_state), (start_state, [])))
    
    visited.add(str(start_state))

    while frontier:
        curr_f, curr_node = heapq.heappop(frontier)
        curr_state, curr_path = curr_node
        
        expansion_count += 1

        if goal_test(curr_state):
            return curr_path, expansion_count
        
        for action in get_actions(curr_state):
            next_state = transition_model(curr_state, action)
            
            if str(next_state) not in visited:
                next_path = copy.deepcopy(curr_path)
                next_path.append(action)

                g_cost = len(next_path)
                h_cost = heuristic(next_state)
                priority = g_cost + h_cost
                
                heapq.heappush(frontier, (priority, (next_state, next_path)))
                visited.add(str(next_state))

if __name__ == '__main__':
  start = generate_random_start_w_fixed_depth(10)
  print_state(start)
  print()

  print('BFS:')
  bfs_solution, bfs_expansions = breadth_first_search(start)
  print(bfs_solution)
  print(len(bfs_solution))
  print('num expansions: ' + str(bfs_expansions))
  print()
  
  depths = [4, 10, 20]

  print(f"{'Algorithm':<15} | {'Depth':<5} | {'Expansions':<10} | {'Cost':<5} | {'Path'}") 
  print("-" * 80)

  for d in depths:
    random_start = generate_random_start_w_fixed_depth(d)

    sol_greedy, greedy_h2_expansions = greedy_search(random_start, h2)
    print(f"{'Greedy h2':<15} | {d:<5} | {greedy_h2_expansions:<10} | {len(sol_greedy):<5} | {sol_greedy}")

    sol_astar, a_star_h2_expansions = a_star_search(random_start, h2)
    print(f"{'A* h2':<15} | {d:<5} | {a_star_h2_expansions:<10} | {len(sol_astar):<5} | {sol_astar}")


  
  

