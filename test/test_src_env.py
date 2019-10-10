import sys, os
import unittest

CURRENT_TEST_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(CURRENT_TEST_DIR + "/../src")

from utils.env import GridWorld

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


