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
    """
    def __init__(self, state=None):
        if state is None:
            raise AttributeError('Grid requires a state')

        self.state = state
        self.neighbor = {}

class GridWorld(BaseEnv):
    """
    Simple grid world, for a 3x3 grid world has states as follows
    7 8 9
    4 5 6
    1 2 3

    The default goal is the top right corner
    The default starting location is the bottom left corner

    Args:
        goal: Where the agent wants to end up
        start: Where the agents starts from in the environment
        grids:List of objects to represent different states of agent

    """
    def __init__(self, size=(3, 3)):
        super(GridWorld, self).__init__()
        if self.goal is None:
            self.goal = size[0] * size[1]
        if self.start is None:
            self.start = 1
        self.grids = []
        self.generate_env(size)


    def generate_env(self, size):
        """
        When generating the world, add extra blocking grids around the environment
                 B B B B B
        1 2 3    B 1 2 3 B
        4 5 6 => B 4 5 6 B
        7 8 9    B 7 8 9 B
                 B B B B B
        """
        #First Generate Grids
        for i in range(size[0]+2):
            for j in range(size[1]+2):
                if i == 0 or j == 0 or i == size[0]+1 or j == size[1]+1:
                    self.grids.append(Grid('b'))
                else:
                    self.grids.append(Grid('a'))
        #Assign neighbors to grids
        for counter, grid in enumerate(self.grids):
            #Assign right
            if counter % size[0] != size[0]-1:
                grid.neighbors['right'] = self.grids[counter + 1]
            #Assign left
            if counter % size[0] != 0:
                grid.neighbors['left'] = self.grids[counter - 1]
            #Assign up
            if int(counter / size[0]) % size[1] != 0:
                grid.neighbors['up'] = self.grids[counter - size[0]]
            #Assign down
            if int(counter / size[0]) % size[1] != size[1]-1:
                grid.neighbors['down'] = self.grids[counter + size[0]]

    def get_reward(self, state):
        return 0 if state != self.goal else self.reward

    def apply_agent_action(self, action):
        self.agent_location = self.agent_location.neighbors[action]

    def reset_env(self):
        self.agent_location = self.start
