import unittest
import unittest.mock
import SSW555_Group_Project
import io
import datetime
import sys
import logging

# Set DEBUG True if you want to see expected/actual values.
DEBUG = False

class Test_US34(unittest.TestCase):

    def setUp(self):
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
        #self.log.debug(SSW555_Group_Project.GedcomFile._individual_dt)

    def print_testcasedetails(self,expected,actual):
        if DEBUG==True:
            self.log.debug("Test Case: %s",self.id())
            self.log.debug("Expected Value: %s" %expected)
            self.log.debug("  Actual Value: %s" %actual)
            self.log.debug("Test Passed? %s" %(expected==actual))         


    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_US34_30days(self,mocked_stdout):

        self.person.birth = datetime.datetime.date(self.today - datetime.timedelta(days=30))
        SSW555_Group_Project.GedcomFile.list_recent_births(self.gedcom)

        expected = "RECENT BIRTH: US35: Name: %s, Individual: ID %s, born %d days ago! Birthday: %s\n" \
                %(self.person.name, self.person.id, 30, self.person.birth)

        self.assertEqual(mocked_stdout.getvalue(), expected)
        self.print_testcasedetails(expected, mocked_stdout.getvalue())
   
    
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_US34_0days(self,mocked_stdout):
        self.person.birth = datetime.date(self.today.year, self.today.month, self.today.day)       
        SSW555_Group_Project.GedcomFile.list_recent_births(self.gedcom)
        expected = "RECENT BIRTH: US35: Name: %s, Individual: ID %s, born %d days ago! Birthday: %s\n" \
                %(self.person.name, self.person.id, 0, self.person.birth)

        self.assertEqual(mocked_stdout.getvalue(), expected)
        self.print_testcasedetails(expected, mocked_stdout.getvalue())

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_US34_31days(self,mocked_stdout):

        self.person.birth = datetime.datetime.date(self.today - datetime.timedelta(days=31))
        SSW555_Group_Project.GedcomFile.list_recent_births(self.gedcom)

        expected = ""

        self.assertEqual(mocked_stdout.getvalue(), expected)
        self.print_testcasedetails(expected, mocked_stdout.getvalue())


    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_US34_neg1days(self,mocked_stdout):

        self.person.birth = datetime.datetime.date(self.today + datetime.timedelta(days=1))
        SSW555_Group_Project.GedcomFile.list_recent_births(self.gedcom)

        expected = ""

        self.assertEqual(mocked_stdout.getvalue(), expected)
        self.print_testcasedetails(expected, mocked_stdout.getvalue())


if __name__ == '__main__':
    if DEBUG == True:
        logging.basicConfig( stream=sys.stderr )
        logging.getLogger("Test").setLevel(logging.DEBUG)
    unittest.main()
