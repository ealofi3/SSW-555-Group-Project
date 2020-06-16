'''The purpose of this program is to identify errors and anomalies in GEDCOM geneology files'''

from typing import Iterator, Tuple, IO, List, Dict, Set
from collections import defaultdict
import datetime
import os
from prettytable import PrettyTable

class Family:
    '''class Family'''
    _pretty_table_headers: List[str] = ['ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children']

    def __init__(self):
        '''Initializes the details for an instance of a family'''

        self.id: str = ''
        self.marriage_date: str = ''                         
        self.divorce_date: str = 'NA'                                 
        self.husband_id: str = ''
        self.husband_name: str = 'TBD'
        self.wife_id: str = ''
        self.wife_name: str = 'TBD'
        self.children: Set[str] = set()
        self.preceding_tag_related_to_date: str = ''

    def details(self, tag: str, argument: str) -> None:
        '''Assigns family detail based on a given tag'''
        
        if tag == 'FAM':
            self.id = argument
        
        if tag == 'HUSB':
            self.husband_id = argument

        if tag == 'WIFE':
            self.wife_id = argument
        
        if tag == 'CHIL':
            self.children.add(argument)
        
        if tag == 'MARR' or tag == 'DIV':
            self.preceding_tag_related_to_date = tag

        if tag == 'DATE':
            self.process_family_record_date_tag(argument)

    def process_family_record_date_tag(self, date_in_gedcom_format: str) -> None:
        '''Converts a date from the format set in a GEDCOM file (day, month, year) to
            the final desired format (year, month, day). Assigns the date to either marriage date or divorce date, based on its 
            preceding tag, which is either "MARR" or "DIV"
        '''

        day, month, year = date_in_gedcom_format.split(" ")
        day: int = int(day)
        year: int = int(year)
        month: int = datetime.datetime.strptime(month, '%b').month
        date_in_final_format: str = datetime.date(year, month, day)

        if self.preceding_tag_related_to_date == 'MARR':
            self.marriage_date = date_in_final_format

        elif self.preceding_tag_related_to_date == 'DIV':
            self.divorce_date = date_in_final_format
                
    def return_pretty_table_row(self) -> List[str]:
        '''Returns a list that is to be used as a row in the families pretty table'''

        return [self.id, self.marriage_date, self.divorce_date, self.husband_id, self.husband_name, self.wife_id, self.wife_name, (self.children or "None")]


class Individual:
    '''class Individual'''

    _headers_for_prettytable: List[str] = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]

    def __init__(self):
        '''Initializes the details for an instance of an individual'''

        self.id: str = ''
        self.name: str = ''
        self.sex: str = ''
        self.birth: str = ''
        self.age: str = ''
        self.living: str = True
        self.death_date: str = 'NA'
        self.famc: Set[str] = set()
        self.fams: Set[str] = set()
        self.preceding_tag_related_to_date: str = ''

    def details(self, tag: str, argument: str) -> None:
        '''Assigns family detail based on a given tag'''

        if tag == 'INDI':
            self.id = argument

        elif tag == 'NAME':
            self.name = argument

        elif tag == 'SEX':
            self.sex = argument

        elif tag == 'BIRT' or tag == 'DEAT':
            self.preceding_tag_related_to_date = tag
        
        elif tag == 'FAMC':
            self.famc.add(argument)
        
        elif tag == 'FAMS':
            self.fams.add(argument)

        elif tag == 'DATE':
            self.process_individual_record_date_tag(argument)

    def process_individual_record_date_tag(self, date_in_gedcom_format: str) -> None:
        '''Converts a date from the format set in a GEDCOM file (day, month, year) to
            the final desired format (year, month, day). Assigns the date to either marriage date or divorce date, based on its 
            preceding tag, which is either "BIRT" or "DEAT"
        '''

        day, month, year = date_in_gedcom_format.split(" ")
        day: int = int(day)
        year: int = int(year)
        month: int = datetime.datetime.strptime(month, '%b').month
        date_in_final_format: str = datetime.date(year, month, day)

        if self.preceding_tag_related_to_date == 'BIRT':
            self.birth = date_in_final_format

        elif self.preceding_tag_related_to_date == 'DEAT':
            self.death_date = date_in_final_format
            self.living = False
        #print(self.name)
        self.setAge()

    def setAge(self) -> None: 
        '''Calculates the age of an individual'''

        if self.living:
            today = datetime.date.today()
        else:
            today = self.death_date
        self.age = (today - self.birth).days//365  #TBD: Not perfect. leap years, etc.

    def return_pretty_table_row(self) -> List[str]:
        '''Returns a list that is to be used as a row for the individuals pretty table'''

        return [self.id, self.name, self.sex, self.birth, self.age, self.living, self.death_date, (self.famc or "None"), (self.fams or "NA")]

    def return_living_and_marital_details(self) -> Tuple[bool, int, str]:
        '''Implemented for US30 & US31. 
            Returns a tuple containing: individual's name as the first element, age as second element, a boolean as third element, and an int as the fourth element.
            -The boolean is True if individual is living, False if not.
            -The int reflects the # of families this individual has been a spouse of. If 0, the individual is/has not married. If greter than 0, the individual is married.
        '''

        return self.name, self.age, self.living, len(self.fams) 


class GedcomFile:
    '''class GedcomFile'''

    _valid_tags: Dict[str, str] = {  'INDI' : '0', 'NAME' : '1', 'SEX' : '1', 'BIRT' : '1', 'DEAT' : '1', 'FAMC' : '1',
                                'FAMS' : '1', 'FAM' : '0', 'MARR' : '1', 'HUSB' : '1', 'WIFE' : '1', 'CHIL' : '1', 
                                'DIV' : '1', 'DATE' : '2', 'HEAD' : '0', 'TRLR' : '0', 'NOTE' : '0', } #key = tag : value = level
    
    _individual_dt: Dict[str, Individual] = dict()
    _family_dt: Dict[str, Family] = dict()
    _individuals_living_and_married: Dict[str, str] = dict()
    _individuals_living_over_thirty_and_never_married: Dict[str, str] = dict()

    def __init__(self) -> None:
        '''Sets containers to store the input and output lines'''

        self._input: List[str] = list()
        self._output: List[str] = list()
        self._validated_list: List[str] = list()        

    def read_file(self, file_name: str) -> None:
        '''Reads a GEDCOM file and populates the self._input list container with the lines from the GEDCOM file'''

        file: IO = open(file_name)

        with file:
            for line in file:
                self._input.append(line.strip())
    
    def validate_tags_for_output(self) -> None:
        '''Takes each line in the self._input list container, splits it, and determines whether tags are valid'''
        #print(self._input)
        for line in self._input:
            #skip blank lines
            if len(line) == 0:
                continue
            line: List[str] = line.split()
            level: str = line[0]
            tag: str = line[1]
            arguments: str = f'{" ".join(line[2:])}'

            if 'INDI' in line or 'FAM' in line:
                self.validate_tags_for_exceptions(line, level, tag)
            else:
                if tag in GedcomFile._valid_tags and level == GedcomFile._valid_tags[tag]:
                    self._output.append(f'<-- {level}|{tag}|Y|{arguments}')
                else:
                    self._output.append(f'<-- {level}|{tag}|N|{arguments}')
      
    def validate_tags_for_exceptions(self, line: List[str], level: str, default_tag: str) -> None:
        '''Validates the tags for any line that meets the formatting exception identified in Project02 description.
            Format exceptions identified are: '0 <id> INDI' and '0 <id> FAM'
        '''

        if line[-1] == 'INDI' or line[-1] == 'FAM':
            tag: str = line[-1]
            arguments: str = f'{line[1]}'

            if tag in GedcomFile._valid_tags and level == GedcomFile._valid_tags[tag]:
                self._output.append(f'<-- {level}|{tag}|Y|{arguments}')
            else:
                self._output.append(f'<-- {level}|{tag}|N|{arguments}')

        else:
            arguments: str = f'{line[-1]}'
            self._output.append(f'<-- {level}|{default_tag}|N|{arguments}')
        
    def update_validated_list(self) -> None:
        '''Create a list of validated gedcom entries'''
        for entry in self._output:
            level, tag, validity, arg = entry.split("|")
            level = int(level[-1])
            if validity == 'Y':
                self._validated_list.append([level, tag, arg])

    def parse_valid_entry(self) -> Tuple[str]:
        '''Generator to extract level, tag and argument from validated list'''

        for valid_line in self._validated_list: 
            level: int = int(valid_line[0])
            tag: str = valid_line[1]
            argument: str = valid_line[2]
            yield level, tag, argument

    def parse_validated_gedcom(self) -> None:
        '''Parses the gedcom entries for individuals and families'''
        
        # Default our flags to neither an individual or family
        individual_record = False
        family_record = False
        
        for level, tag, argument in self.parse_valid_entry():
            if tag == "INDI":
                # Subsequent records will define an individual
                individual_record = True
                family_record = False
                
                # Since this is the start - Create the Individual!
                individual: Individual = Individual()
                individual_id: str = argument
                self._individual_dt[individual_id] = individual
                
            elif tag == "FAM":
                # Subsequent records will define a family
                family_record = True
                individual_record = False
                
                # Since this is the start - Create the Family!
                family: Family = Family()
                family_id: str = argument
                self._family_dt[family_id] = family
                
            elif tag == "TRLR" or tag == "HEAD" or tag == "NOTE":
                 # this is neither a family or an individual.
                 family_record = False
                 individual_record = False
            
            # Record the details regarding this tag to the appropriate record type.
            if individual_record:
                individual.details(tag,argument)
            elif family_record:
                family.details(tag,argument)

    def print_individuals_pretty(self) -> PrettyTable:
        '''Prints a prettytable containing details for individuals'''

        individuals_pretty_table: PrettyTable = PrettyTable(field_names= Individual._headers_for_prettytable)
        
        for individual in self._individual_dt.values():
            individuals_pretty_table.add_row(individual.return_pretty_table_row())
        
        print("People")
        print(individuals_pretty_table)
        print("\n")

    def print_family_pretty(self) -> PrettyTable:
        '''Prints a prettytable containing details for individuals'''

        family_pretty_table: PrettyTable = PrettyTable(field_names= Family._pretty_table_headers)

        for family in self._family_dt.values():
            family_pretty_table.add_row(family.return_pretty_table_row())
        
        print("Families")
        print(family_pretty_table)
        print("\n")

    def family_set_spouse_names(self):
        for entry in self._family_dt:
            
            husband_id = self._family_dt[entry].husband_id
            try:
                husband_name = self._individual_dt[husband_id].name
            except KeyError:
                husband_name = "Unknown"      
            self._family_dt[entry].husband_name = husband_name   

            wife_id = self._family_dt[entry].wife_id
            try:
                wife_name = self._individual_dt[wife_id].name                    
            except KeyError:
                wife_name = "Unknown"  
                
            self._family_dt[entry].wife_name = wife_name 


    def list_large_age_differences(self) -> None:
        '''US 34: Determine married couples who have an age difference of 2x or more '''      
        
        for family in self._family_dt.values():
            
            try:
                husband = self._individual_dt[family.husband_id]
                wife = self._individual_dt[family.wife_id]
            except KeyError:
                #Individual doesn't exist, so skip this family.
                continue

            if type(husband.age) == str or type(wife.age) == str:
                # A birthdate was not provided for one of the spouses. Skip this family.
                continue

            if husband.age > (wife.age * 2):
                husband_is_older = True
            elif wife.age > (husband.age * 2):
                husband_is_older = False
            else:
                # No need to report this married couple.
                continue

            # OK, if we're still here, then we have an Anomaly to report. 
            print("ANOMALY: US34: FAMILY: %s " %family.id, end='')

            if husband_is_older:
                print("Name: %s, id: %s, age: %d is more than 2x in age as spouse: %s, id: %s, age: %d" \
                %(family.husband_name, family.husband_id, husband.age, family.wife_name,  family.wife_id, wife.age ))            
            else:
                print("Name: %s, id: %s, age: %d is more than 2x in age as spouse: %s, id: %s, age: %d" \
                %(family.wife_name, family.wife_id, wife.age, family.husband_name,  family.husband_id, husband.age ))

    def list_recent_births(self)->None:
        '''US35: List all people in a GEDCOM file who were born in the last 30 days'''
        for person in self._individual_dt.values():
            birth_date = person.birth
            if type(birth_date) != datetime.date:
                # Invalid entry
                continue
            today = datetime.date.today()
            age_days = (today - birth_date).days  # difference results in datetime.timedelta

            if age_days <= 30:
                print("RECENT BIRTH: US35: Name: %s, Individual: ID %s, born %d days ago! Birthday: %s" \
                %(person.name, person.id, age_days, birth_date))

    def parse_individuals_based_on_living_and_marital_details(self) -> None:
        '''US30 & US31: Identifies whether an individual is: Living and married, or Living, over 30 years old and has never been married. After identifying, stores the 
            individuals ID and Name in either the _individuals_living_and_married dictionary or the _individuals_living_over_thirty_and_never_married dictionary'''
        
        for individual_id, individual in self._individual_dt.items():
            name, age, alive, number_of_times_married = individual.return_living_and_marital_details()
            
            if alive == True and number_of_times_married > 0:
                GedcomFile._individuals_living_and_married[individual_id] = name
            
            elif alive == True and age > 30 and number_of_times_married == 0:
                GedcomFile._individuals_living_over_thirty_and_never_married[individual_id] = name

    def list_individuals_living_and_married(self) -> None:
        '''US30: Prints a prettytable that lists all individuals that are alive and married'''

        pretty_table_for_living_and_married_people: PrettyTable = PrettyTable(field_names=['ID', 'Name'])

        if len(GedcomFile._individuals_living_and_married) == 0:
            pretty_table_for_living_and_married_people.add_row(['None', 'None'])
        
        else:
            for individual_id, name in GedcomFile._individuals_living_and_married.items():
                pretty_table_for_living_and_married_people.add_row([individual_id, name])
        
        print(f'All Individuals Living and Married:\n{pretty_table_for_living_and_married_people}\n')

    def list_individuals_living_over_thirty_never_married(self) -> None:
        '''US31: Prints a prettytable that lists all individuals that are alive, over 30 yrs old, and have never been married'''

        pretty_table_for_living_over_thirty_never_married: PrettyTable = PrettyTable(field_names=['ID', 'Name'])

        if len(GedcomFile._individuals_living_over_thirty_and_never_married) == 0:
            pretty_table_for_living_over_thirty_never_married.add_row(['None', 'None'])
        
        else:
            for individual_id, name in GedcomFile._individuals_living_over_thirty_and_never_married.items():
                pretty_table_for_living_over_thirty_never_married.add_row([individual_id, name])
        
        print(f'All Individuals Living, Over 30, and Never Married:\n{pretty_table_for_living_over_thirty_never_married}\n')


def main() -> None:
    '''Runs main program'''

    # file_name: str = input('Enter GEDCOM file name: ')
    file_name: str = "p1.ged"
    
    gedcom: GedcomFile = GedcomFile()
    gedcom.read_file(file_name)
    gedcom.validate_tags_for_output()
    
    gedcom.update_validated_list()
    gedcom.parse_validated_gedcom()
    gedcom.family_set_spouse_names()
    
    gedcom.print_individuals_pretty()
    gedcom.print_family_pretty()

    # Print out User Story output from hereon:

    # US34: List large age differences
    gedcom.list_large_age_differences()

    # US35: List recent births
    gedcom.list_recent_births()

    #US30 & #US31
    gedcom.parse_individuals_based_on_living_and_marital_details()
    gedcom.list_individuals_living_and_married()
    gedcom.list_individuals_living_over_thirty_never_married()

if __name__ == '__main__':
    main()
