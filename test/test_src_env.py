import sys, os
import unittest

CURRENT_TEST_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(CURRENT_TEST_DIR + "/../src")

from env import GridWorld

class testGridWorld(unittest.TestCase):
    def testCreate(self):
        gridworld = GridWorld()
        results = gridworld.get_pretty()
        target = "bbbbb\nbaaab\nbaaab\nbaaab\nbbbbb\n"
        self.assertEqual(results,target)

    def testCreateRect(self):
        gridworld = GridWorld(size= (3,4))
        results = gridworld.get_pretty()
        target = "bbbbb\nbaaab\nbaaab\nbaaab\nbaaab\nbbbbb\n"
        self.assertEqual(results,target)

    def testCreateRect2(self):
        gridworld = GridWorld(size= (4,3))
        results = gridworld.get_pretty()
        target = "bbbbbb\nbaaaab\nbaaaab\nbaaaab\nbbbbbb\n"
        self.assertEqual(results,target)

    def testMap_states(self):
        gridworld = GridWorld(size= (3,4))
        start = [0,1,2,3,4,5,6,7,8,9,10,11]
        target = [6,7,8,11,12,13,16,17,18,21,22,23]
        results = list(map(gridworld.map_states, start))
        self.assertEqual(results,target)

    def testNeighbors(self):
        """
        #Check that 1, 5, and 9 have the correct neighbors
                 B B B B B
        1 2 3    B 1 2 3 B
        4 5 6 => B 4 5 6 B
        7 8 9    B 7 8 9 B
                 B B B B B
        """
        gridworld = GridWorld()
        
        #Check 1, index is 0
        grid_1 = gridworld.grids[gridworld.map_states(0)]
        grid_1_neighbors = list(grid_1.neighbors.values())
        grid_1_neighbors_ids = [grid.id for grid in grid_1_neighbors] 
        results = list(set(grid_1_neighbors_ids) - set([None]))
        results.sort()
        target = [2,4]
        self.assertEqual(results,target)
        
        #Check 5, index is 4
        grid_5 = gridworld.grids[gridworld.map_states(4)]
        grid_5_neighbors = list(grid_5.neighbors.values())
        grid_5_neighbors_ids = [grid.id for grid in grid_5_neighbors] 
        results = list(set(grid_5_neighbors_ids) - set([None]))
        results.sort()
        target = [2,4,6,8]
        self.assertEqual(results,target)

        #Check 9, index is 8
        grid_9 = gridworld.grids[gridworld.map_states(8)]
        grid_9_neighbors = list(grid_9.neighbors.values())
        grid_9_neighbors_ids = [grid.id for grid in grid_9_neighbors] 
        results = list(set(grid_9_neighbors_ids) - set([None]))
        results.sort()
        target = [6,8]
        self.assertEqual(results,target)
