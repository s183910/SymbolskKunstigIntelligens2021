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
d=0

def OR_search(state, path, action_set, goal_description,results):
    if (goal_description.is_goal(state)):
        return 0,[]
    # if state is on path: return False
    if state in path:
        return 0,False

    actions = state.get_applicable_actions(action_set)
    for action in actions:
        plan = [] 
        or_plan = AND_search(results(state,action),path, action_set, goal_description,results)
        if (plan != False):
            return action,plan
        
    return False
    
def AND_search(states, path, action_set, goal_description,results):
    
    for state in states:
        
        

    return

def and_or_graph_search(initial_state, action_set, goal_description, results):
    
    OR_search(initial_state, [], action_set)

    

    # Here you should implement AND-OR-GRAPH-SEARCH. We are going to use a different plan format than the one used
    # in the textbook.
    # The algorithm should return a pair (worst_case_length, or_plan) where the plan is of the following format
    # or_plan: A pair [action, and_plan] or an empty list [] in the base case, i.e. when a goal state is reached.
    # and_plan: A dictionary mapping states to or_plans.
    # So the following conditional plan from the slides:
    #   Suck; if s5 then (Right; Suck)
    # would here be represented as:
    # [
    #   Suck,
    #   {
    #     's7': [],
    #     's5':
    #     [
    #       Right,
    #       {
    #         's6':
    #         [
    #           Suck,
    #           {
    #             's8': []
    #           }
    # 	    ]
    #       }
    #     ]
    #   }
    # ]
    raise NotImplementedError()
