import unittest
import unittest.mock
import SSW555_Group_Project
import io
import datetime
import sys
import logging

# Set True if you want to see expected/actual values.
TC_VERBOSE = False

class Test_US35(unittest.TestCase):

    def setUp(self):
        SSW555_Group_Project.GedcomFile._individual_dt.clear()
        self.gedcom = SSW555_Group_Project.GedcomFile()
        self.person = SSW555_Group_Project.Individual()
        self.person.id = "@I_test1@"
        self.person.living = True
        self.person.name = "Test Subject"
        self.person.famc = "@F_test1@"
        self.person.fams = "@F_test2@"
        SSW555_Group_Project.GedcomFile._individual_dt[self.person.id]=self.person
        self.today = datetime.datetime.today()
        self.log = logging.getLogger("Test")

    def print_testcasedetails(self,expected,actual):
        if TC_VERBOSE==True:
            self.log.debug("Test Case: %s",self.id())
            self.log.debug("Expected Value: %s" %expected)
            self.log.debug("  Actual Value: %s" %actual)
            self.log.debug("Test Passed? %s" %(expected==actual))         


    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_US35_30days(self,mocked_stdout):

        self.person.birth = datetime.datetime.date(self.today - datetime.timedelta(days=30))
        SSW555_Group_Project.GedcomFile.US35_list_recent_births(self.gedcom)

        expected = "RECENT BIRTH: US35: Name: %s, Individual: ID %s, born %d days ago! Birthday: %s\n" \
                %(self.person.name, self.person.id, 30, self.person.birth)

        self.assertEqual(mocked_stdout.getvalue(), expected)
        self.print_testcasedetails(expected, mocked_stdout.getvalue())
   
    
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_US35_0days(self,mocked_stdout):
        self.person.birth = datetime.date(self.today.year, self.today.month, self.today.day)       
        SSW555_Group_Project.GedcomFile.US35_list_recent_births(self.gedcom)
        expected = "RECENT BIRTH: US35: Name: %s, Individual: ID %s, born %d days ago! Birthday: %s\n" \
                %(self.person.name, self.person.id, 0, self.person.birth)

        self.assertEqual(mocked_stdout.getvalue(), expected)
        self.print_testcasedetails(expected, mocked_stdout.getvalue())

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_US35_31days(self,mocked_stdout):

        self.person.birth = datetime.datetime.date(self.today - datetime.timedelta(days=31))
        SSW555_Group_Project.GedcomFile.US35_list_recent_births(self.gedcom)

        expected = ""

        self.assertEqual(mocked_stdout.getvalue(), expected)
        self.print_testcasedetails(expected, mocked_stdout.getvalue())


    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_US35_neg1days(self,mocked_stdout):

        self.person.birth = datetime.datetime.date(self.today + datetime.timedelta(days=1))
        SSW555_Group_Project.GedcomFile.US35_list_recent_births(self.gedcom)

        expected = ""

        self.assertEqual(mocked_stdout.getvalue(), expected)
        self.print_testcasedetails(expected, mocked_stdout.getvalue())






class Test_US34(unittest.TestCase):
    test_subjects = list()

    def setUp(self):
        self.maxDiff = None
        SSW555_Group_Project.GedcomFile._individual_dt.clear()
        SSW555_Group_Project.GedcomFile._family_dt.clear()
        self.gedcom = SSW555_Group_Project.GedcomFile()

        # Create 2 pairs husband/wife. This creates the individuals and families.
        for i in range(0,4):

            if i%2 == 0:
                self.family = SSW555_Group_Project.Family()
                self.family.id = "@F_Stest" + str(i//2)
                SSW555_Group_Project.GedcomFile._family_dt[self.family.id] = self.family

            self.person = SSW555_Group_Project.Individual()
            self.person.id = "@I" + str(i) + "@"
            self.person.living = True
            self.person.name = "Test " + "Subject"+ str(i)
            self.person.famc = "@F_Ctest" + str(i)
            self.person.fams = "@F_Stest" + str(i//2)

            if i%2 == 0:
                self.person.sex = "M"
                self.family.husband_id = self.person.id
                self.family.husband_name = self.person.name
            else:
                self.person.sex = "F"
                self.family.wife_id = self.person.id
                self.family.wife_name = self.person.name

            SSW555_Group_Project.GedcomFile._individual_dt[self.person.id] = self.person

        self.log = logging.getLogger("Test")

    def print_testcasedetails(self,expected,actual):
        if TC_VERBOSE==True:
            self.log.debug("Test Case: %s",self.id())
            self.log.debug("Expected Value: %s" %expected)
            self.log.debug("  Actual Value: %s" %actual)
            self.log.debug("Test Passed? %s" %(expected==actual))         


    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_US34_spouseExactly2xAge(self,mocked_stdout):
        husband_age = 18
        wife_age = husband_age * 2
        SSW555_Group_Project.GedcomFile._individual_dt["@I0@"].age = husband_age
        SSW555_Group_Project.GedcomFile._individual_dt["@I1@"].age = wife_age
        
        wife_age = 35
        husband_age = wife_age * 2
        SSW555_Group_Project.GedcomFile._individual_dt["@I2@"].age = husband_age
        SSW555_Group_Project.GedcomFile._individual_dt["@I3@"].age = wife_age

        SSW555_Group_Project.GedcomFile.US34_list_large_age_differences(self.gedcom)

        expected = ""

        self.assertEqual(mocked_stdout.getvalue(), expected)
        self.print_testcasedetails(expected, mocked_stdout.getvalue())



    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_US34_spouseGreater2xAge(self,mocked_stdout):
        husband_age = 18
        wife_age = (husband_age * 2) + 1
        SSW555_Group_Project.GedcomFile._individual_dt["@I0@"].age = husband_age
        SSW555_Group_Project.GedcomFile._individual_dt["@I1@"].age = wife_age
        husband_name = SSW555_Group_Project.GedcomFile._individual_dt["@I0@"].name
        wife_name = SSW555_Group_Project.GedcomFile._individual_dt["@I1@"].name
        family_id = SSW555_Group_Project.GedcomFile._individual_dt["@I0@"].fams
        
        expected_1 = "ANOMALY: US34: FAMILY: %s Name: %s, id: %s, age: %d is more than 2x in age as spouse: %s, id: %s, age: %d" \
            %(family_id, wife_name, "@I1@", wife_age, husband_name,  "@I0@", husband_age )

        wife_age = 35
        husband_age = (wife_age * 2) + 1
        SSW555_Group_Project.GedcomFile._individual_dt["@I2@"].age = husband_age
        SSW555_Group_Project.GedcomFile._individual_dt["@I3@"].age = wife_age
        husband_name = SSW555_Group_Project.GedcomFile._individual_dt["@I2@"].name
        wife_name = SSW555_Group_Project.GedcomFile._individual_dt["@I3@"].name
        family_id = SSW555_Group_Project.GedcomFile._individual_dt["@I2@"].fams

        expected_2 = "ANOMALY: US34: FAMILY: %s Name: %s, id: %s, age: %d is more than 2x in age as spouse: %s, id: %s, age: %d" \
            %(family_id, husband_name, "@I2@", husband_age, wife_name,  "@I3@", wife_age ) 

        expected = expected_1 + "\n" + expected_2 + "\n"

        SSW555_Group_Project.GedcomFile.US34_list_large_age_differences(self.gedcom)

        self.assertEqual(mocked_stdout.getvalue(), expected)
        self.print_testcasedetails(expected, mocked_stdout.getvalue())


    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_US34_spouseNegAge(self,mocked_stdout):
        husband_age = -18
        wife_age = -8
        SSW555_Group_Project.GedcomFile._individual_dt["@I0@"].age = husband_age
        SSW555_Group_Project.GedcomFile._individual_dt["@I1@"].age = wife_age

        wife_age = -35
        husband_age = -17
        SSW555_Group_Project.GedcomFile._individual_dt["@I2@"].age = husband_age
        SSW555_Group_Project.GedcomFile._individual_dt["@I3@"].age = wife_age

        expected = ""

        SSW555_Group_Project.GedcomFile.US34_list_large_age_differences(self.gedcom)

        self.assertEqual(mocked_stdout.getvalue(), expected)
        self.print_testcasedetails(expected, mocked_stdout.getvalue())


if __name__ == '__main__':
    if TC_VERBOSE == True:
        logging.basicConfig( stream=sys.stderr )
        logging.getLogger("Test").setLevel(logging.DEBUG)
    unittest.main()
