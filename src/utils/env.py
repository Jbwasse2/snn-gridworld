#Contains various environments for the agent
#This will probably evolve to use gym_minigrid/gym, but for now it will be a simple nxn grid without visualization

#***********IMPORTS***********
from abc import ABC
#*****************************

class BaseEnv():
    """
    Every environment needs to define the state of the agent in the environment and the interactions of the agent in the world
    base_env defines the bare minimum functions and variables that need to be defined for a given environment
    """
    def __init__(self, goal=None, start=None, reward=1):
        self.agent_location = None
        self.goal = goal
        self.start = None
        self.reward = reward

    @abc.abstractmethod
    def generate_env(self):
        raise NotImplemented

    @abc.abstractmethod
    def get_reward(self,state):
        """
        Returns the reward for a given state 
        """
        raise NotImplemented

    @abc.abstractmethod
    def apply_agent_action(self,action):
        """
        Applies a given action of the agent onto the environment
        """
        raise NotImplemented

    @abc.abstractmethod
    def reset_env(self):
        """
        Returns the agent/environment back to its initial state
        """
        raise NotImplemented


class Grid():
    """
    Represents a space in grid world, can have different states that affect the agent including
        -Blocking movement (State = 'b')
        -Allowing the agent to move into grid (State = 'a')
    """
    def __init__(state=None):
        if state is None:
            raise AttributeError('Grid requires a state')

        self.state = state

class GridWorld(baseEnv):
    """
    Simple grid world, for a 3x3 grid world has states as follows
    7 8 9
    4 5 6
    1 2 3

    Returns:
        None

    """
    def __init__(self, size=(3,3)):
    """
    The default goal is the top right corner
    The default starting location is the bottom left corner

    Args:
        goal: Where the agent wants to end up
        start: Where the agents starts from in the environment
    """
        if goal is None:
            self.goal = size[0] * size[1]
        if start is None:
            self.start = 1

        self.generate_env(size)


    def generate_env(self, size):
        """
        TODO
        When generating the world, add extra blocking grids around the environment
        """
        for i in range(size[0]+1):
            for j in range(size[1]+1):

    def get_reward(self,state):
        return 0 if state != goal else self.reward
        
   # TODO
    def apply_agent_action(self,action):
        pass
        
    def reset_env(self):
        self.agent_location = self.start
