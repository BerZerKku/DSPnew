# -*- coding: utf-8 -*-
'''
Created on 10 май 2014г.

@author: Хозяин
'''

import unittest
import my_func

#------------------------------------------------------------------------------
class TestMyFunc(unittest.TestCase):
    """${short_summary_of_testcase}
    """
#     def setUp(self):
# #        self.testFrame = TabCheck()
#         self.app = QtGui.QApplication(sys.argv)
#           self.form = TabCheck()

#       def tearDown(self):
#           """${no_tearDown_required}
#           """
#           pass  # skip tearDown
    def testIntToStrHex(self):
        """ (self) -> None
        
            �������� ���������� ������ ������� intToStrHex.
        """
        self.assertEqual(my_func.intToStrHex(12), '0C')
        self.assertEqual(my_func.intToStrHex(12, num=4), '000C')
        self.assertEqual(my_func.intToStrHex(2049), '0801')
        self.assertEqual(my_func.intToStrHex(2049, num=2), '01')
        self.assertEqual(my_func.intToStrHex(2049, arch="le"), '0108')

        self.assertRaises(TypeError, my_func.intToStrHex, "1")
        self.assertRaises(TypeError, my_func.intToStrHex, 12, '12')
        self.assertRaises(ValueError, my_func.intToStrHex, 12, None, "d")

    def testStrHexToInt(self):
        """ (self) -> None
        
            �������� ���������� ������ ������� strHexToInt.
        """
        self.assertEqual(my_func.strHexToInt("CC0"), 3264)
        self.assertEqual(my_func.strHexToInt("CC0", "be"), 3264)
        self.assertEqual(my_func.strHexToInt("12"), 18)
        self.assertEqual(my_func.strHexToInt("0CC0", "le"), 49164)

        self.assertRaises(ValueError, my_func.strHexToInt, "CC0", "d")
        self.assertRaises(TypeError, my_func.strHexToInt, 12)
        self.assertRaises(ValueError, my_func.strHexToInt, ":1")

    def testCharToStrHex(self):
        """ (self) -> None
            �������� ���������� ������ ������� charToStrHex.
        """
        self.assertEqual(my_func.charToStrHex("1"), "31")
        self.assertEqual(my_func.charToStrHex("A"), "41")
        self.assertEqual(my_func.charToStrHex("123"), "313233")

        self.assertRaises(TypeError, my_func.charToStrHex, 12)

    def testStrHexToChar(self):
        """ (self) -> None
            �������� ���������� ������ ������� strHexToChar.
        """
        self.assertEqual(my_func.strHexToChar("31"), "1")
        self.assertEqual(my_func.strHexToChar("41"), "A")
        self.assertEqual(my_func.strHexToChar("313233"), "123")

        self.assertRaises(TypeError, my_func.strHexToChar, 12)
        self.assertRaises(ValueError, my_func.strHexToChar, "1")
        self.assertRaises(ValueError, my_func.strHexToChar, ":1")

    def testHextoFloat(self):
        """ (self) -> None
        
            �������� ���������� ������ ������� hexToFloat.
        """
        
        val = 18.899999618530273
        self.assertEqual(my_func.strHexToFloat("41973333"), val)
        val = 4.18142498403995e-08
        self.assertEqual(my_func.strHexToFloat("41973333", "le"), val)
        val = 36806.078125
        self.assertEqual(my_func.strHexToFloat("470FC614"), val)

        self.assertRaises(TypeError, my_func.strHexToFloat, 12)
        self.assertRaises(ValueError, my_func.strHexToFloat, "41973333", "d")
        self.assertRaises(ValueError, my_func.strHexToFloat, ":70FC614")

    def testFloatToStrHex(self):
        """ (self) -> None
        
            �������� ���������� ������ ������� floatToHex.
        """
        self.assertEqual(my_func.floatToStrHex(3.99), "407F5C29")
        self.assertEqual(my_func.floatToStrHex(3.99, "le"), "295C7F40")
        self.assertEqual(my_func.floatToStrHex(12.18), "4142E148")

        self.assertRaises(TypeError, my_func.floatToStrHex, 12)
        self.assertRaises(ValueError, my_func.floatToStrHex, 12.5, "d")

    def testFindCoeffDSP(self):
        """ (self) -> None
        
            �������� ���������� ������ ������� findCoeff.
        """
        self.assertEqual(my_func.findCoeffDSP('0001', 16, '803e', 1000),
                         '0 + (16 * freq)')
        self.assertEqual(my_func.findCoeffDSP('C001', 16, 'C07C', 1000),
                         '-64 + (32 * freq)')

