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

from collections import deque

class FrontierDFS:

    def __init__(self):
        # Your code here...
        self.queue = deque()
        self.set = set()

    def prepare(self, goal_description):
        # Prepare is called at the beginning of a search and since we will sometimes reuse frontiers for multiple
        # searches, prepares must ensure that state is cleared.
        
        # Your code here...
        self.queue.clear()
        self.set.clear()
 
    def add(self, state):
        # Your code here...
        self.queue.append(state)
        self.set.add(state)
  
    def pop(self):
        # Your code here...
        state = self.queue.pop()
        self.set.remove(state)
        return state

    def is_empty(self):
        # Your code here...
        return len(self.queue) == 0

    def size(self):
        # Your code here...
        return len(self.queue)

    def contains(self, state):
        # Your code here...
        return state in self.set

