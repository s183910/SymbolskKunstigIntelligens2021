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

from numpy import linalg as LA
import sys
import itertools
from utils import pos_add, pos_sub, APPROX_INFINITY
import math

class HospitalGoalCountHeuristics:

    def __init__(self):
        pass

    def preprocess(self, level):
        # This function will be called a single time prior to the search allowing us to preprocess the level such as
        # pre-computing lookup tables or other acceleration structures
        pass

    def h(self, state, goal_description):
        # Your code goes here...
        n_goals = goal_description.num_sub_goals()

        for index in range(goal_description.num_sub_goals()):
            sub_goal = goal_description.get_sub_goal(index)
            n_goals -= sub_goal.is_goal(state)

        return n_goals


class HospitalAdvancedHeuristics:

    def __init__(self):
        pass

    def preprocess(self, level):
        # This function will be called a single time prior to the search allowing us to preprocess the level such as
        # pre-computing lookup tables or other acceleration structures
        
        
        pass


    def h(self, state, goal_description):

        # # Get name and position of box and goals
        goals = goal_description.box_goals
        boxes = state.box_positions
        # boxes which have been allocated to a goal
        used_boxes = []

        # sum of distances between goals and boxes
        dist = 0


        # we iterate over goals, as each goal only needs one box, and the number of goals always is less or equal to the number of boxes
        for goal in goals:
            for box_idx, box in enumerate(boxes):
                # continue if box is a match and has not already been allocated to a specific goal
                if (goal[1] == box[1] and (box_idx not in used_boxes)):     
                    # Calculate manhattan distance between these points and add to total distance   
                    used_boxes.append(box_idx)          
                    dist += abs(goal[0][0]-box[0][0])+abs(goal[0][1]-box[0][1])
                    break
        
        # Return average distance
        return dist/len(goals) 

