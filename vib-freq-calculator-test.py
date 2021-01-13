"""
Unit test for funtions used in the Vibrational Frequency Calculator for Triatomic

@author: btb32
"""

import unittest

import vfc_functions as vfc

class DataExtraction(unittest.TestCase):
    
    def testGeometry(self):
        pathname ="./extracted/H2Ooutfiles/"
        filename = "H2O.r0.70theta75.0.out"
        expected = (0.7, 75.0)
        self.assertTupleEqual(vfc.get_gemeotry_energy(pathname,filename)[0:2], expected)
    def testEnergy(self):
        pathname ="./extracted/H2Ooutfiles/"
        filename = "H2O.r0.70theta75.0.out"
        expected = -75.7253171225
        self.assertEqual(vfc.get_gemeotry_energy(pathname,filename)[2], expected)
    def testAllFilesExtracted(self):
        pathname ="./extracted/H2Ooutfiles/"
        total = 2275
        self.assertEqual(len(vfc.dictionary_PES(pathname)), total)
        

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DataExtraction))

    unittest.TextTestRunner(verbosity=2).run(suite)
 