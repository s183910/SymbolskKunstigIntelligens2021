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

import random
from search_algorithms.and_or_graph_search import and_or_graph_search
from utils import *


def broken_results(state, action):
    standard_case = state.result(action)
    if standard_case.is_applicable(action):
        broken_case = standard_case.result(action)
        return [standard_case, broken_case]
    else:
        return [standard_case]


CHANCE_OF_EXTRA_ACTION = 0.5


def non_deterministic_agent_type(level, initial_state, action_library, goal_description):

    # Create an action set for a single agent.
    action_set = [action_library]

    # Call AND-OR-GRAPH-SEARCH to compute a conditional plan
    worst_case_length, plan = and_or_graph_search(initial_state, action_set, goal_description, broken_results)

    if worst_case_length is None:
        print("Failed to find strong plan!", file=sys.stderr)
        return

    print("Found plan of worst-case length", worst_case_length, file=sys.stderr)

    current_state = initial_state
    current_plan = plan

    while True:

        # If we have reached the goal, then we are done
        if goal_description.is_goal(current_state):
            break

        # Otherwise, read the next action to execute
        joint_action, conditional_plan = current_plan

        # Send the joint action to the server
        print(joint_action_to_string(joint_action), flush=True, file=sys.stderr)
        print(joint_action_to_string(joint_action), flush=True)
        _ = parse_response(read_line())
        current_state = current_state.result(joint_action)

        # Roll a dice to check whether this action will be executed twice.
        is_broken = random.random() < CHANCE_OF_EXTRA_ACTION
        is_applicable = current_state.is_applicable(joint_action)
        if is_broken and is_applicable:
            print(f"Ups! Extra {joint_action_to_string(joint_action)}", flush=True, file=sys.stderr)
            print(joint_action_to_string(joint_action), flush=True)
            _ = parse_response(read_line())
            current_state = current_state.result(joint_action)

        if current_state not in conditional_plan:
            # The agent reached a state not covered by the conditional plan. This should not occur using a correct
            # AND-OR-GRAPH-SEARCH implementation.
            print(f"Reached state not covered by plan!\n{current_state}", file=sys.stderr)
            break

        # Look up the current state in the conditional plan
        current_plan = conditional_plan[current_state]
