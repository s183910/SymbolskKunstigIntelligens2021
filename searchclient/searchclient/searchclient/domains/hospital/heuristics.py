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
import itertools
from utils import pos_add, pos_sub, APPROX_INFINITY


class HospitalGoalCountHeuristics:

    def __init__(self):
        pass

    def preprocess(self, level):
        # This function will be called a single time prior to the search allowing us to preprocess the level such as
        # pre-computing lookup tables or other acceleration structures
        pass

    def h(self, state, goal_description):
        # Your code goes here...
        return 0


class HospitalAdvancedHeuristics:

    def __init__(self):
        pass

    def preprocess(self, level):
        # This function will be called a single time prior to the search allowing us to preprocess the level such as
        # pre-computing lookup tables or other acceleration structures
        pass


    def h(self, state, goal_description):

        # Your heuristic goes here...
        return 0