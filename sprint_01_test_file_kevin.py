'''The purpose of this file is to test user stories US30 and US31'''

from SSW555_Group_Project import Individual, GedcomFile
import unittest
from typing import IO, Dict

class GedcomFileTest(unittest.TestCase):
    '''Tests the methods implemented for US30 & US31:
        -find_all_people_living_and_married
        -find_all_people_living_over_thirty_and_never_married
    '''

    test_file_name: str = 'p1.ged'

    def test_find_all_people_living_and_married(self) -> None:
        '''Tests that the method correctly identifies all individuals, by ID and name, that are alive and married.
        '''

        gedcom: GedcomFile = GedcomFile()
        gedcom.read_file(GedcomFileTest.test_file_name)
        gedcom.validate_tags_for_output()
        
        gedcom.update_validated_list()
        gedcom.parse_validated_gedcom()
        gedcom.family_set_spouse_names()
        
        result: Dict[str, str] = gedcom.find_all_people_living_and_married()

        expected: Dict[str, str] = {'@I2@' : 'Sankar /Sam/',
                                    '@I3@' : 'Sunitha /Krish/',
                                    '@I5@' : 'Baby /Chung/',
                                    '@I6@' : 'Leela /Pritish/',}

        self.assertEqual(result, expected)

    def test_find_all_people_living_over_thirty_and_never_married(self) -> None:
        '''Tests that the method correctly identifies all individuals, by ID and name, that are alive
            over 30 yrs old, and have never been married.
        '''

        gedcom: GedcomFile = GedcomFile()
        gedcom.read_file(GedcomFileTest.test_file_name)
        gedcom.validate_tags_for_output()
        
        gedcom.update_validated_list()
        gedcom.parse_validated_gedcom()
        gedcom.family_set_spouse_names()
        
        result: Dict[str, str] = gedcom.find_all_people_living_over_thirty_and_never_married()

        expected: Dict[str, str] = {}

        self.assertEqual(result, expected)




if __name__ == '__main__':
    unittest.main(exit= False, verbosity= 2)