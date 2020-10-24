# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 17:16:15 2020

@author: btb32
"""

import unittest
import numpy as np
import VibFreqCalculator as vfc

class DataExtraction(unittest.TestCase):
    def testGeometry(self):
        filename = "H2O.r0.70theta75.0.out"
        expected = (0.7, 75.0)
        self.assertTupleEqual(vfc.gemeotry_energy(filename)[0:2], expected)
    def testEnergy(self):
        filename = "H2O.r0.70theta75.0.out"
        expected = -75.7253171225
        self.assertEqual(vfc.gemeotry_energy(filename)[2], expected)
    def testAllFilesExtracted(self):
        total = 2275
        self.assertEqual(len(vfc.bondlengths), total)
        self.assertEqual(len(vfc.bondangles), total)
        self.assertEqual(len(vfc.energies), total)
        
        

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DataExtraction))

    unittest.TextTestRunner(verbosity=2).run(suite)
 