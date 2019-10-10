"""
Contains various environments for the agent
This will probably evolve to use gym_minigrid/gym,
but for now it will be a simple nxn grid without visualization
"""
#***********IMPORTS***********
from abc import ABCMeta, abstractmethod
#*****************************

class BaseEnv(metaclass=ABCMeta):
    """
    Every environment needs to define the state of the agent in
    the environment and the interactions of the agent in the world
    base_env defines the bare minimum functions and variables
    that need to be defined for a given environment
    """
    def __init__(self, goal=None, start=None, reward=1):
        self.agent_location = None
        self.goal = goal
        self.start = start
        self.reward = reward

    @abstractmethod
    def generate_env(self):
        """
        Procedure to create the world
        """

    @abstractmethod
    def get_reward(self, state):
        """
        Returns the reward for a given state
        """

    @abstractmethod
    def apply_agent_action(self, action):
        """
        Applies a given action of the agent onto the environment
        """

    @abstractmethod
    def reset_env(self):
        """
        Returns the agent/environment back to its initial state
        """


class Grid():
    """
    Represents a space in grid world, can have different states that affect the agent including
    -Blocking movement (State = 'b')
    -Allowing the agent to move into grid (State = 'a')

    var:
        state = State of the grid
        neighbor = Dictionary of neighbors, key is direction of next state.
                   For simple GridWorld, this is "up", "down", "left", and "right"
        reward = reward for being in a given state
        ID = ID given to state, useful for debugging
    """
    def __init__(self, state=None, id= None):
        if state is None:
            raise AttributeError('Grid requires a state')

        self.state = state
        self.neighbors = {}
        self.reward = 0
        self.id = id

        def set_reward(self, reward):
            self.reward = reward

        def get_reward(self):
            return self.reward

class GridWorld(BaseEnv):
    """
    Simple grid world, for a 3x3 grid world has states as follows
    1 2 3
    4 5 6 
    7 8 9

    with the following indices
    0 1 2
    3 4 5
    6 7 8 

    The default goal is the top right corner
    The default starting location is the bottom left corner

    Args:
        goal: Where the agent wants to end up (USE INDEX!!!)
        start: Where the agents starts from in the environment (USE INDEX!!!)
        grids:List of objects to represent different states of agent
        size: Size of the grid world (rectangular or square shape)

    raises:
        TypeError: If goal/start are not int or None

    """
    def __init__(self, size=(3, 3)):
        super(GridWorld, self).__init__()
        self.grids = []
        self.generate_env(size)

        self.size = size

        if self.goal is None:
            self.goal = self.grids[map_states(size[0] * size[1])-1]
        elif self.goal is int:
            self.goal = self.grids[map_states(self.goal)]
        else:
            raise TypeError

        if self.start is None:
            self.start = self.grids[map_states(0)]
        elif self.start is int:
            self.start = self.grids[map_states(self.start)]
        else:
            raise TypeError


    def map_states(self, state):
        """
        This class is used to map a state index from the original grid world to the grid world with walls around it.

        This is useful if you want to abstract away the walls
        
                   B B B B B
        1 2 3      B 1 2 3 B
        4 5 6 =>   B 4 5 6 B
        7 8 9      B 7 8 9 B
       10 11 12   B 10 11 12 B
                   B B B B B

        Index mapping for (3,4) case
        0 -> 6
        1 -> 7
        2 -> 8
        3 -> 11
        4 -> 12
        5 -> 13
        6 -> 16
        7 -> 17
        8 -> 18
        9 -> 21
        10 -> 22
        11 -> 23

        Idea: Get row index, multiply by col + 2, add modulo + 1
        f(state) = row_index+1 * walled_gridworld_x + (state % walled_grid_world_x) + 1
        Args:
            state: index in original gridworld that we'd like to access
        
        Returns:
            corresponding index in walled gridworld
        
        """
        row_id = int(state / (self.size[0])) + 1
        offset = state % self.size[0] + 1
        return row_id * (self.size[0] + 2) + offset

    def generate_env(self, size):
        """
        When generating the world, add extra blocking grids around the environment
                 B B B B B
        1 2 3    B 1 2 3 B
        4 5 6 => B 4 5 6 B
        7 8 9    B 7 8 9 B
                 B B B B B

        """
        new_size_x = size[0] + 2
        new_size_y = size[1] + 2
        #First Generate Grids
        for i in range(new_size_y):
            for j in range(new_size_x):
                if i == 0 or j == 0 or i == new_size_y-1 or j == new_size_x-1:
                    self.grids.append(Grid('b', id = i * new_size_y + j ))
                else:
                    self.grids.append(Grid('a', id = i * new_size_y + j))
        #Assign neighbors to grids
        for counter, grid in enumerate(self.grids):
            #Assign right
            if counter % new_size_x != new_size_x-1:
                grid.neighbors['right'] = self.grids[counter + 1]
            #Assign left
            if counter % new_size_x != 0:
                grid.neighbors['left'] = self.grids[counter - 1]
            #Assign up
            if int(counter / new_size_x) % new_size_y != 0:
                grid.neighbors['up'] = self.grids[counter - new_size_x]
            #Assign down
            if int(counter / new_size_x) % new_size_y != new_size_y-1:
                grid.neighbors['down'] = self.grids[counter + new_size_x]

    def get_reward(self, state):
        return 0 if state != self.goal else self.agent_location.get_reward()

    def apply_agent_action(self, action):
        self.agent_location = self.agent_location.neighbors[action]

    def reset_env(self):
        self.agent_location = self.start

    def get_pretty(self):
        """
        Returns a pretty graphic, useful for debugging and testing code
        """
        ret_string = ""
        for counter, grid in enumerate(self.grids):
            ret_string += grid.state
            #Add offset of 2 because the maze is surronded by blocking grids
            if counter % (self.size[0] + 2) == self.size[0] +2 - 1:
                ret_string += "\n"
        return ret_string

