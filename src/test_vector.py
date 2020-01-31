# -*- coding: utf-8 -*-
import unittest, vector, mark_util

class VectorTests(unittest.TestCase):
    def test_block_check_exist_in_mark(self):
        Txt = ("..XXX"
               "XXXXX"
               "XXXX."
               "XXX..")
        MarkGenerated = mark_util.mark_from_string(Txt, 5, "X")
        BlockCheck, PixelProblem, CoordsOfBlock = vector.block_check_exist_in_mark(MarkGenerated, 0, 1, 2, 3)
        self.assertEqual(BlockCheck, True)

        BlockCheck, PixelProblem, CoordsOfBlock = vector.block_check_exist_in_mark(MarkGenerated, 0, 1, 4, 3)
        self.assertEqual(BlockCheck, False)

    def test_block_nonoverlap_search_in_mark(self):
        Txt = ("..XXX"
               "XXXXX"
               "XXXX."
               "XXX..")
        MarkGenerated = mark_util.mark_from_string(Txt, 5, "X")
        BlocksInMark = vector.block_nonoverlap_search_in_mark(MarkGenerated)

        BlocksWanted = {3: [(0, 1)],
                        2: [(2, 0), (0, 1)],
                        1: [(2, 0), (3, 0), (4, 0), (0, 1), (1, 1),
                            (2, 1), (3, 1), (4, 1), (0, 2), (1, 2),
                            (2, 2), (3, 2), (0, 3), (1, 3), (2, 3)]}
        self.assertEqual(BlocksInMark, BlocksWanted)

def run_all_tests(P):
    print("run all tests: Vector")
    global Prg
    Prg = P
    unittest.main(module="test_vector", verbosity=2, exit=False)
