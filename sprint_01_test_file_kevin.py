'''The purpose of this file is to test user stories US30 and US31'''

from SSW555_Group_Project import Individual, GedcomFile
import unittest
from typing import IO

class GedcomFileTest(unittest.TestCase):
    '''Tests the methods implemented for US30 & US31:
        -list_all_people_living_and_married
        -list_all_people_over_thirty_and_never_married
    '''

    test_file_name: str = 'sprint_01_test_GEDCOM_file.txt'

    def test_list_all_people_living_and_married(self):
        '''Tests that the correct number and names of individuals are identified'''

        gedcom: GedcomFile = GedcomFile()
        gedcom.read_file(GedcomFileTest.test_file_name)
        gedcom.validate_tags_for_output()
        
        gedcom.update_validated_list()
        gedcom.parse_validated_gedcom()
        gedcom.family_set_spouse_names()
        