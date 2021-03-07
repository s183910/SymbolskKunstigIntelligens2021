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
        goals = goal_description.goals

        boxes = state.box_positions
    
        #for goal in goals:
        indexes = []

        sum_dist = 0

        #print(goals,file = sys.stderr)

        for goal in goals:
            for idx,box in enumerate(boxes):
                if (goal[1] == box[1]) and (idx not in indexes):     

                    # Define two points as position of box and goal
                    # x1 = goal[0][0]
                    # y1 = goal[0][1]

                    # x2 = box[0][0]
                    # y2 = box[0][1]

                    #Calculate euclidean distance between these points                    
                    sum_dist += math.sqrt((goal[0][0]-box[0][0])**2+(goal[0][1]-box[0][1])**2)
                    indexes.append(idx)
                    break

        return sum_dist/len(goals)






        #print(boxes, file = sys.stderr)
        
        #length = LA.norm([boxes,goals])
        
        #print(length,file=sys.stderr)
        # Your heuristic goes here...

        # n_goals = goal_description.num_sub_goals()

        # for index in range(goal_description.num_sub_goals()):
        #     sub_goal = goal_description.get_sub_goal(index)
        #     n_goals -= sub_goal.is_goal(state)

        # return n_goals
