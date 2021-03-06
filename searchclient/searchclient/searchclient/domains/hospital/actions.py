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

# pos_add and pos_sub are helper methods for performing element-wise addition and subtractions on positions
# Ex: Given two positions A = (1, 2) and B = (3, 4), pos_add(A, B) == (4, 6) and pos_sub(B, A) == (2,2)
from utils import pos_add, pos_sub

direction_deltas = {
    'N': (-1, 0),
    'S': (1, 0),
    'E': (0, 1),
    'W': (0, -1),
}

# An action class must implement three types be a valid action:
# 1) is_applicable(self, agent_index, state) which return a boolean describing whether this action is valid for
#    the agent with 'agent_index' to perform in 'state' independently of any other action performed by other agents.
# 2) result(self, agent_index, state) which modifies the 'state' to incorporate the changes caused by the agent
#    performing the action. Since we *always* call both 'is_applicable' and 'conflicts' prior to calling 'result',
#    there is no need to check for correctness.
# 3) conflicts(self, agent_index, state) which returns information regarding potential conflicts with other actions
#    performed concurrently by other agents. More specifically, conflicts can occur with regard to the following
#    two invariants:
#    A) Two objects may not have the same destination.
#       Ex: '0  A1' where agent 0 performs Move(E) and agent 1 performs Push(W,W)
#    B) Two agents may not move the same box concurrently,
#       Ex: '0A1' where agent 0 performs Pull(W,W) and agent 1 performs Pull(E,E)
#    In order to check for these, the conflict method should return two lists:
#       a) destinations which contains all newly occupied cells.
#       b) moved_boxes which contains the current position of boxes moved during the action, i.e. their position
#          prior to being moved by the action.
# Note that 'agent_index' is the index of the agent in the state.agent_positions list which is often but *not always*
# the same as the numerical value of the agent character.


class NoOpAction:

    def __init__(self):
        self.name = "NoOp"

    def is_applicable(self, agent_index,  state):
        # Optimization. NoOp can never change the state if we only have a single agent
        return len(state.agent_positions) > 1

    def result(self, agent_index, state):
        pass

    def conflicts(self, agent_index, state):
        current_agent_position, _ = state.agent_positions[agent_index]
        destinations = [current_agent_position]
        boxes_moved = []
        return destinations, boxes_moved


class MoveAction:

    def __init__(self, agent_direction):
        self.agent_delta = direction_deltas.get(agent_direction)
        self.name = "Move(%s)" % agent_direction

    def calculate_positions(self, current_agent_position):
        return pos_add(current_agent_position, self.agent_delta)

    def is_applicable(self, agent_index, state):
        current_agent_position, _ = state.agent_positions[agent_index]
        new_agent_position = self.calculate_positions(current_agent_position)
        return state.free_at(new_agent_position)

    def result(self, agent_index, state):
        current_agent_position, agent_char = state.agent_positions[agent_index]
        new_agent_position = self.calculate_positions(current_agent_position)
        state.agent_positions[agent_index] = (new_agent_position, agent_char)

    def conflicts(self, agent_index, state):
        current_agent_position, _ = state.agent_positions[agent_index]
        new_agent_position = self.calculate_positions(current_agent_position)
        # New agent position is a destination because it is unoccupied before the action and occupied after the action.
        destinations = [new_agent_position]
        # Since a Move action never moves a box, we can just return the empty value.
        boxes_moved = []
        return destinations, boxes_moved


## Herunder forsøges indsættelse af push action
class PushAction:
    def __init__(self, agent_direction, box_direction):
        self.agent_delta = direction_deltas.get(agent_direction)
        self.box_delta = direction_deltas.get(box_direction)
        self.name = "Push(%s,%s)" % (agent_direction, box_direction)

    def calculate_agent_positions(self, current_agent_position):
        return pos_add(current_agent_position, self.agent_delta)
    
    # function for box position
    def calculate_box_positions(self, current_box_position):
        return pos_add(current_box_position, self.box_delta)

    def is_applicable(self, agent_index, state):
        current_agent_position, agent_char = state.agent_positions[agent_index]
        # calculate box position based on position and direction of agent
        current_box_position = self.calculate_agent_positions(current_agent_position)

        box_index, box_char = state.box_at(current_box_position)

        # Check if box is present at location
        if box_index == -1:
            return False
        # Check if agent color matches box color
        if state.level.colors[box_char] != state.level.colors[agent_char]:
            return False
        
        # Calculate new box position
        new_box_position = self.calculate_box_positions(current_box_position)

        # returns true if new box position is free
        return state.free_at(new_box_position) 

    def result(self, agent_index, state):
        current_agent_position, agent_char = state.agent_positions[agent_index]
        # calculate box position based on position and direction of agent
        current_box_position = self.calculate_agent_positions(current_agent_position)
        
        # save which box will be moved
        box_index, box_char = state.box_at(current_box_position)

        # find new position of box and agent, after Push
        new_box_position = self.calculate_box_positions(current_box_position)
        new_agent_position = self.calculate_agent_positions(current_agent_position)

        # update agent and box positions 
        state.agent_positions[agent_index] = (new_agent_position, agent_char)
        state.box_positions[box_index] = (new_box_position, box_char)


    def conflicts(self, agent_index, state):
        current_agent_position, agent_char = state.agent_positions[agent_index]
        current_box_position = self.calculate_agent_positions(current_agent_position)
        new_agent_position = current_box_position
        new_box_position = self.calculate_box_positions(current_box_position)
        
        # New agent position is a destination because it is unoccupied before the action and occupied after the action.
        destinations = [new_box_position]
        # Since a Move action never moves a box, we can just return the empty value.
        boxes_moved = [current_box_position]
        return destinations, boxes_moved

## Herunder forsøges indsættelse af pull action
class PullAction:
    def __init__(self, agent_direction, box_direction):
        self.agent_delta = direction_deltas.get(agent_direction)
        self.box_delta = direction_deltas.get(box_direction)
        self.name = "Pull(%s,%s)" % (agent_direction, box_direction)

    def calculate_agent_positions(self, current_agent_position):
        return pos_add(current_agent_position, self.agent_delta)
    
    # function for box position
    def calculate_box_positions(self, current_box_position):
        return pos_add(current_box_position, self.box_delta)

    def is_applicable(self, agent_index, state):
        current_agent_position, agent_char = state.agent_positions[agent_index]
        # calculate box position based on position of agent and direction of box
        current_box_position = pos_sub(current_agent_position, self.box_delta)

        box_index, box_char = state.box_at(current_box_position)

        # Check if box is present at location
        if box_index == -1:
            return False
        # Check if agent color matches box color
        if state.level.colors[box_char] != state.level.colors[agent_char]:
            return False
        
        # Calculate new agent position
        new_agent_position = self.calculate_agent_positions(current_agent_position)
        
        # returns true if new agent position is free
        return state.free_at(new_agent_position) 

    def result(self, agent_index, state):
        current_agent_position, agent_char = state.agent_positions[agent_index]
        # calculate current box position based on position of agent, and direction of box
        current_box_position = pos_sub(current_agent_position, self.box_delta)
        
        # save which box will be moved
        box_index, box_char = state.box_at(current_box_position)

        # find new position of box and agent, after Push
        new_box_position = current_agent_position
        new_agent_position = self.calculate_agent_positions(current_agent_position)
    
        # update agent and box positions 
        state.agent_positions[agent_index] = (new_agent_position, agent_char)
        state.box_positions[box_index] = (new_box_position, box_char)


    def conflicts(self, agent_index, state):
        current_agent_position, agent_char = state.agent_positions[agent_index]
        current_box_position = pos_sub(current_agent_position, self.box_delta)
        
        new_agent_position = self.calculate_agent_positions(current_agent_position)
        new_box_position = current_agent_position
        
        # New agent position is a destination because it is unoccupied before the action and occupied after the action.
        destinations = [new_agent_position]
        # Since a Move action never moves a box, we can just return the empty value.
        boxes_moved = [current_box_position]
        return destinations, boxes_moved




# ******

class StickyMoveAction:

    def __init__(self, agent_direction):
        self.agent_delta = direction_deltas.get(agent_direction)
        self.name = "Move(%s)" % agent_direction

    def calculate_positions(self, current_agent_position):
        return pos_add(current_agent_position, self.agent_delta)

# incorporate preconditions Exercise 1.1
    def is_applicable(self, agent_index, state):
        current_agent_position, agent_char = state.agent_positions[agent_index]
        new_agent_position = self.calculate_positions(current_agent_position)

        all_goals = state.level.agent_goal_at(current_agent_position) == agent_char
       
        return state.free_at(new_agent_position) and  not all_goals 

    def result(self, agent_index, state):
        current_agent_position, agent_char = state.agent_positions[agent_index]
        new_agent_position = self.calculate_positions(current_agent_position)
        state.agent_positions[agent_index] = (new_agent_position, agent_char)

    def conflicts(self, agent_index, state):
        current_agent_position, _ = state.agent_positions[agent_index]
        new_agent_position = self.calculate_positions(current_agent_position)
        # New agent position is a destination because it is unoccupied before the 
        # action and occupied after the action.
        destinations = [new_agent_position]
        # Since a Move action never moves a box, we can just return the empty value.
        boxes_moved = []
        return destinations, boxes_moved


## Herunder indsættes sticky push action
class StickyPushAction:
    def __init__(self, agent_direction, box_direction):
        self.agent_delta = direction_deltas.get(agent_direction)
        self.box_delta = direction_deltas.get(box_direction)
        self.name = "Push(%s,%s)" % (agent_direction, box_direction)

    def calculate_agent_positions(self, current_agent_position):
        return pos_add(current_agent_position, self.agent_delta)
    
    # function for box position
    def calculate_box_positions(self, current_box_position):
        return pos_add(current_box_position, self.box_delta)

    def is_applicable(self, agent_index, state):
        current_agent_position, agent_char = state.agent_positions[agent_index]
        # calculate box position based on position and direction of agent
        current_box_position = self.calculate_agent_positions(current_agent_position)

        box_index, box_char = state.box_at(current_box_position)

        # Check if box is present at location
        if box_index == -1:
            return False
        # Check if agent color matches box color
        if state.level.colors[box_char] != state.level.colors[agent_char]:
            return False
        
        # Calculate new box position
        new_box_position = self.calculate_box_positions(current_box_position)
       
        # New for exercise 1.1 Mavis2
        all_goals_box = state.level.box_goal_at(current_box_position) == box_char
        all_goals_agent = state.level.agent_goal_at(current_agent_position) == agent_char

        # returns true if new box position is free
        return state.free_at(new_box_position) and not all_goals_agent and not all_goals_box 

    def result(self, agent_index, state):
        current_agent_position, agent_char = state.agent_positions[agent_index]
        # calculate box position based on position and direction of agent
        current_box_position = self.calculate_agent_positions(current_agent_position)
        
        # save which box will be moved
        box_index, box_char = state.box_at(current_box_position)

        # find new position of box and agent, after Push
        new_box_position = self.calculate_box_positions(current_box_position)
        new_agent_position = self.calculate_agent_positions(current_agent_position)

        # update agent and box positions 
        state.agent_positions[agent_index] = (new_agent_position, agent_char)
        state.box_positions[box_index] = (new_box_position, box_char)

    def conflicts(self, agent_index, state):
        current_agent_position, agent_char = state.agent_positions[agent_index]
        current_box_position = self.calculate_agent_positions(current_agent_position)
        new_agent_position = current_box_position
        new_box_position = self.calculate_box_positions(current_box_position)
        
        # New agent position is a destination because it is unoccupied before the action 
        # and occupied after the action.
        destinations = [new_agent_position, new_box_position]
        # Since a Move action never moves a box, we can just return the empty value.
        boxes_moved = [current_box_position]
        return destinations, boxes_moved

## Herunder indsættes pull action
class StickyPullAction:
    def __init__(self, agent_direction, box_direction):
        self.agent_delta = direction_deltas.get(agent_direction)
        self.box_delta = direction_deltas.get(box_direction)
        self.name = "Pull(%s,%s)" % (agent_direction, box_direction)

    def calculate_agent_positions(self, current_agent_position):
        return pos_add(current_agent_position, self.agent_delta)
    
    # function for box position
    def calculate_box_positions(self, current_box_position):
        return pos_add(current_box_position, self.box_delta)

    def is_applicable(self, agent_index, state):
        current_agent_position, agent_char = state.agent_positions[agent_index]
        # calculate box position based on position of agent and direction of box
        current_box_position = pos_sub(current_agent_position, self.box_delta)

        box_index, box_char = state.box_at(current_box_position)

        # Check if box is present at location
        if box_index == -1:
            return False
        # Check if agent color matches box color
        if state.level.colors[box_char] != state.level.colors[agent_char]:
            return False
        
        # Calculate new agent position
        new_agent_position = self.calculate_agent_positions(current_agent_position)
        
        # New for exercise 1.1 Mavis2
        all_goals_box = state.level.box_goal_at(current_box_position) == box_char
        all_goals_agent = state.level.agent_goal_at(current_agent_position) == agent_char

        # returns true if new agent position is free and....
        return state.free_at(new_agent_position) and not all_goals_agent and not all_goals_box 

    def result(self, agent_index, state):
        current_agent_position, agent_char = state.agent_positions[agent_index]
        # calculate current box position based on position of agent, and direction of box
        current_box_position = pos_sub(current_agent_position, self.box_delta)
        
        # save which box will be moved
        box_index, box_char = state.box_at(current_box_position)

        # find new position of box and agent, after Push
        new_box_position = current_agent_position
        new_agent_position = self.calculate_agent_positions(current_agent_position)
    
        # update agent and box positions 
        state.agent_positions[agent_index] = (new_agent_position, agent_char)
        state.box_positions[box_index] = (new_box_position, box_char)


    def conflicts(self, agent_index, state):
        current_agent_position, agent_char = state.agent_positions[agent_index]
        current_box_position = pos_sub(current_agent_position, self.box_delta)
        
        new_agent_position = self.calculate_agent_positions(current_agent_position)
        new_box_position = current_agent_position
        
        # New agent position is a destination because it is unoccupied before the action 
        # and occupied after the action.
        destinations = [new_agent_position, new_box_position]
        # Since a Move action never moves a box, we can just return the empty value.
        boxes_moved = [current_box_position]
        return destinations, boxes_moved



# ******





# An action library for the multi agent pathfinding
DEFAULT_MAPF_ACTION_LIBRARY = [
    NoOpAction(),
    MoveAction("N"),
    MoveAction("S"),
    MoveAction("E"),
    MoveAction("W"),
]


# An action library for the full hospital domain
DEFAULT_HOSPITAL_ACTION_LIBRARY = [
    NoOpAction(),
    
    MoveAction("N"),
    MoveAction("S"),
    MoveAction("E"),
    MoveAction("W"),


    # Add Push and Pull actions here
    PushAction("N","N"),
    PushAction("N","S"),
    PushAction("N","E"),
    PushAction("N","W"),
    PushAction("S","N"),
    PushAction("S","S"),
    PushAction("S","E"),
    PushAction("S","W"),
    PushAction("E","N"),
    PushAction("E","S"),
    PushAction("E","E"),
    PushAction("E","W"),
    PushAction("W","N"),
    PushAction("W","S"),
    PushAction("W","E"),
    PushAction("W","W"),

    PullAction("N","N"),
    PullAction("N","S"),
    PullAction("N","E"),
    PullAction("N","W"),
    PullAction("S","N"),
    PullAction("S","S"),
    PullAction("S","E"),
    PullAction("S","W"),
    PullAction("E","N"),
    PullAction("E","S"),
    PullAction("E","E"),
    PullAction("E","W"),
    PullAction("W","N"),
    PullAction("W","S"),
    PullAction("W","E"),
    PullAction("W","W"),


]


# An action library for the hospital domain with sticky goals
STICKY_HOSPITAL_ACTION_LIBRARY = [
    NoOpAction(),
    
    StickyMoveAction("N"),
    StickyMoveAction("S"),
    StickyMoveAction("E"),
    StickyMoveAction("W"),

    StickyPushAction("N","N"),
    StickyPushAction("N","S"),
    StickyPushAction("N","E"),
    StickyPushAction("N","W"),
    StickyPushAction("S","N"),
    StickyPushAction("S","S"),
    StickyPushAction("S","E"),
    StickyPushAction("S","W"),
    StickyPushAction("E","N"),
    StickyPushAction("E","S"),
    StickyPushAction("E","E"),
    StickyPushAction("E","W"),
    StickyPushAction("W","N"),
    StickyPushAction("W","S"),
    StickyPushAction("W","E"),
    StickyPushAction("W","W"),

    StickyPullAction("N","N"),
    StickyPullAction("N","S"),
    StickyPullAction("N","E"),
    StickyPullAction("N","W"),
    StickyPullAction("S","N"),
    StickyPullAction("S","S"),
    StickyPullAction("S","E"),
    StickyPullAction("S","W"),
    StickyPullAction("E","N"),
    StickyPullAction("E","S"),
    StickyPullAction("E","E"),
    StickyPullAction("E","W"),
    StickyPullAction("W","N"),
    StickyPullAction("W","S"),
    StickyPullAction("W","E"),
    StickyPullAction("W","W"),


]
