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
from search_algorithms.graph_search import graph_search


def serial_graph_search(initial_state, action_set, goal_description, frontier):
    
    # Here you should implement the SERIAL-GRAPH-SEARCH algorithm
    # Some methods you might find useful includes:
    # - 'goal_description.num_sub_goals()' and 'goal_description.get_sub_goal(sub_goal_index)'
    # - 'state.result_of_plan(plan)' which computes the resulting state from executing 'plan' starting in 'state'

    n_sub_goals = goal_description.num_sub_goals()
    
    plan = []

    for index in range(n_sub_goals):

        sub_goal = goal_description.get_sub_goal(index)

        success, sub_plan = graph_search(initial_state, action_set, sub_goal, frontier)

        if success:
            plan = plan + sub_plan
        else:
            return False, []

        initial_state = initial_state.result_of_plan(sub_plan)

    return True, plan


