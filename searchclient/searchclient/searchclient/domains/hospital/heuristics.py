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
        

        # Get name and position of box and goals
        goals = goal_description.goals
        boxes = state.box_positions
        
        # index of boxes which have been allocated for specific goals
        indexes = []
        
        # sum of distances between goals and boxes
        sum_dist = 0

        # iterate over each goal, as each goal only needs one box, and the number of goals always is less or equal to the number of boxes
        for goal in goals:
            for idx, box in enumerate(boxes):
                # if box has not already been allocated to a specifik goal
                if (goal[1] == box[1]) and (idx not in indexes):     
                    # Calculate euclidian distance between these points and add to total distance             
                    # sum_dist += abs(goal[0][0]-box[0][0])+abs(goal[0][1]-box[0][1])
                    # Calculate euclidian distance between these points and add to total distance             
                    sum_dist += math.sqrt((goal[0][0]-box[0][0])**2+(goal[0][1]-box[0][1])**2)
                    
                    indexes.append(idx)
                    break
                
        # return average distance between all goals and allocated boxes
        return sum_dist/len(goals)




