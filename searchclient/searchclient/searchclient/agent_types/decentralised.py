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

from search_algorithms.serial_graph_search import serial_graph_search
from utils import *


def decentralised_agent_type(level, initial_state, action_library, goal_description, frontier):
    # Create an action set where all agents can perform all actions
    action_set = [action_library] * level.num_agents

    # Here you should implement the DECENTRALISED-AGENTS algorithm.
    # You can use the 'classic' agent type as a starting point for how to communicate with the server, i.e.
    # use 'print(joint_action_to_string(joint_action), flush=True)' to send a joint_action to the server and
    # use 'parse_response(read_line())' to read back an array of booleans indicating whether each individual action
    #   in the joint action succeeded.

    num_agents = level.num_agents

    plan = []

    for agent_index in range(num_agents):

        current_agent_position, agent_char = initial_state.agent_positions[agent_index]

        color = level.colors[agent_char]

        mono_problem = initial_state.color_filter(color)

        mono_plan = serial_graph_search(mono_problem, action_set, goal_description, frontier)

        plan.append(mono_plan)
        
    print(plan[0])


    # while any(plan):
    #     for agent_index in range(num_agents):
    #         if plan[agent_index]:


    return False


    