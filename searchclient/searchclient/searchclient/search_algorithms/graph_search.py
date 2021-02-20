# coding: utf-8
#
# Copyright 2021 The Technical University of Denmark
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import time
import memory
from domains.hospital.actions import *


def graph_search(initial_state, action_set, goal_description, frontier):
    global start_time
    
    # Set start time
    start_time = time.time()
    iterations = 0
    frontier.prepare(goal_description)

    # Clear the parent pointer and cost in order make sure that the initial state is a root node
    initial_state.parent = None
    initial_state.path_cost = 0

    # Here, you should implement the Graph-Search algorithm from R&N figure 3.7
    # The algorithm should here return a (boolean, list) pair where the boolean denotes
    # whether the algorithm successfully found a plan and the list is the found plan.
    # In the case of "failure to find a solution" you should therefore return False, [].
    # Some useful methods on the State class which you will need to use are:
    # node.extract_plan() - Returns the list of actions used to reach this state.
    # node.get_applicable_actions(action_set) - Returns a list containing the actions applicable in the state.
    # node.result(action) - Returns the new state reached by applying the action to the current state.
    # For the GoalDescription class, you will need to use
    # goal_description.is_goal(node) - Returns true if the state is a goal state.
    # You should also take a look at the frontiers in the strategies folder to see which methods they expose

    return_fixed_solution = False
    

    if return_fixed_solution:
        return True, [
            [MoveAction("S")],
            [MoveAction("S")],
            [MoveAction("E")],
            [MoveAction("E")],
            [MoveAction("E")],
            [MoveAction("E")],
            [MoveAction("E")],
            [MoveAction("E")],
            [MoveAction("E")],
            [MoveAction("E")],
            [MoveAction("E")],
            [MoveAction("E")],
            [MoveAction("S")],
            [MoveAction("S")],
        ]
    frontier.add(initial_state)
    expanded = set()

    while True:

        # Print a progress status message every 10000 iterations
        if iterations % 10000 == 0 and iterations != 0:
            print_search_status(expanded, frontier)

        # Ensure that we do not use more memory than allowed
        if memory.get_usage() > memory.max_usage:
            print('Maximum memory usage exceeded!', file=sys.stderr, flush=True)
            sys.exit(-1)
  
        # Your code here...
        # Exercise 2.2 - implementing graph search

        # define state as top of frontier and pop state 
        state = frontier.pop()

        # adds state to expanded
        expanded.add(state)
        
        # finds applicable actions in current state, and loops through these
        actions = state.get_applicable_actions(action_set)
        for action in actions:
            # finds new state based on applicable action
            new_state = state.result(action)
            # checks if new state has been visited before or is in frontier
            if ((new_state not in expanded) and (not frontier.contains(new_state))):
                # if not, new state is added to frontier
                frontier.add(new_state)

        iterations += 1

        # if state is goal, return True and route to goal
        if goal_description.is_goal(state): 
            print("memory:", memory.get_usage())
            print("states:", len(expanded))
            return True, state.extract_plan()

# A global variable used to keep track of the start time of the current search
start_time = 0

def print_search_status(expanded, frontier):
    global start_time
    if len(expanded) == 0:
        start_time = time.time()
    memory_usage_bytes = memory.get_usage()
    # Replacing the generated comma thousands separators with dots is neither pretty nor locale aware but none of
    # Pythons four different formatting facilities seems to handle this correctly!
    num_expanded = f"{len(expanded):8,d}".replace(',', '.')
    num_frontier = f"{frontier.size():8,d}".replace(',', '.')
    num_generated = f"{len(expanded) + frontier.size():8,d}".replace(',', '.')
    elapsed_time = f"{time.time() - start_time:3.3f}".replace('.', ',')
    memory_usage_mb = f"{memory_usage_bytes / (1024*1024):3.2f}".replace('.', ',')
    status_text = f"#Expanded: {num_expanded}, #Frontier: {num_frontier}, #Generated: {num_generated}," \
                  f" Time: {elapsed_time} s, Memory: {memory_usage_mb} MB"
    print(status_text, file=sys.stderr)
