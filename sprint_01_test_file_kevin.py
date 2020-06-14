'''The purpose of this file is to test user stories US30 and US31'''

from SSW555_Group_Project import Individual, GedcomFile
import unittest

class GedcomFileTest(unittest.TestCase):
    '''Tests the methods implemented for US30 & US31:
        -list_all_people_living_and_married
        -list_all_people_over_thirty_and_never_married
    '''

    def test_list_all_people_living_and_married(self):
        '''Tests that the correct number and names of individuals are identified'''

        