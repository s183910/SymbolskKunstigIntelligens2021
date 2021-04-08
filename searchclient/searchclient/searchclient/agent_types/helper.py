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

from domains.hospital import HospitalGoalDescription
from search_algorithms.graph_search import graph_search
from utils import *


def negative_goals(helpee_position, obstacle_char, plan):
    negative_goals = []
    # Loop through all actions in plan
    for action in plan:
        # Get the direction helpee wants to move
        helpee_delta = action[0].agent_delta
        # Calculate the position that needs to be free
        free_state = (helpee_position[0] + helpee_delta[0], helpee_position[1] +  helpee_delta[1])
        # Define new sub_goal as the obstacle not being in free_state
        sub_goal = (free_state, obstacle_char, False)
        # Append to list of goals
        negative_goals.append(sub_goal)
        # Update state of helpee
        helpee_position = free_state
    
    return negative_goals




def helper_agent_type(level, initial_state, action_library, goal_description, frontier):

    # Here you should implement the HELPER-AGENT algorithm.
    # Some tips are:
    # - You can create an action set where only a specific agent is allowed to move as follows:
    #   action_set = [[GenericNoOp()]] * level.num_agents
    #   action_set[agent_index] = action_library
    # - You probably want to create a helper function for creating the set of negative obstacle subgoals.
    #   You can then create a new goal description using 'goal_description.create_new_goal_description_of_same_type'
    #   which takes a list of subgoals.

    _ , helpee_char = initial_state.agent_positions[0]
    helpee_color = level.colors[helpee_char]
 
    action_set = [[GenericNoOp()]] * level.num_agents    
    action_set[0] = action_library

    # Define mono problem and mono goal
    mono_problem = initial_state.color_filter(helpee_color)
    mono_goal = goal_description.color_filter(helpee_color)

    for index in range(mono_goal.num_sub_goals()):
            sub_goal = mono_goal.get_sub_goal(index)

            success, plan = graph_search(mono_problem, action_set, sub_goal, frontier)

            if not success:
                return False
            
            while any(plan):
                
                joint_action = [action_library[0]] * level.num_agents 
                joint_action[0] = plan[0][0]
                
                # Send the joint action to the server
                print(joint_action_to_string(joint_action), flush=True)

                # Uncomment the below line to print the executed actions to the command line for debugging purposes
                # print(joint_action_to_string(joint_action), file=sys.stderr, flush=True)

                # Read back whether the agents succeeded in performing the joint action
                execution_successes = parse_response(read_line())              
                
                if execution_successes[0]:
                    initial_state = initial_state.result(joint_action)
                    plan.pop(0)
                
                else:
                    helpee_delta = joint_action[0].agent_delta
                    helpee_position , helpee_char = initial_state.agent_positions[0]
                    obstacle_position = (helpee_position[0] + helpee_delta[0],helpee_position[1] + helpee_delta[1])
                    # print(helpee_position,file=sys.stderr)
                    # print(helpee_delta,file=sys.stderr)
                    # print(obstacle_position, file=sys.stderr)
                    obstacle_index, obstacle_char = initial_state.box_at(obstacle_position)
                    # helpee_position , helpee_char = initial_state.box_positions[0]
                    obstacle_color = level.colors[obstacle_char]

                    exists=0
                    for agent_index in range(level.num_agents):
                        _ , agent_char = initial_state.agent_positions[agent_index]
                        if agent_char == obstacle_char:
                            break

                    negative = negative_goals(helpee_position, obstacle_char, plan)
                    negative_goal_description = goal_description.create_new_goal_description_of_same_type(negative)
                    
                    helper_action_set = [[GenericNoOp()]] * level.num_agents    
                    helper_action_set[agent_index] = action_library

                    helper_success, helper_plan = graph_search(initial_state, helper_action_set, negative_goal_description, frontier)
                    
                    if helper_success:
                        while any(helper_plan):
                            joint_action = helper_plan.pop(0)
                            helper_action = joint_action[agent_index]

                            print(joint_action_to_string(joint_action), flush=True)
                            initial_state = initial_state.result(joint_action)
                        
