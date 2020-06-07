'''The purpose of this program is to read a GEDCOM file, print "--> <input line>", and print "<-- <level>|<tag>|<valid?> : Y or N|<arguments>" '''

from typing import Iterator, Tuple, IO, List, Dict
import datetime
import os
from prettytable import PrettyTable

class family:
    def __init__(self, id):
        self.id = id
        self.married = False
        self.marriage_date = str()
        self.husband_id = str()
        self.wife_id = str()
        self.children = list()
        self.divorced = False
        self.divorce_date = str()

    def return_list(self):
        return [self.id, self.married, self.marriage_date, self.husband_id, self.wife_id, self.children, self.divorced, self.divorce_date]


class indiv:
    def __init__(self, id):
        # Grab the ID and default everything else.
        self.id = id
        self.name = str()
        self.sex = str()
        self.birth = datetime.date(1,1,1)
        self.age = "TBD"
        self.living = True
        self.death_date = "NA"
        self.child = str()
        self.spouse = str()
        self.famc = "NA"
        self.fams = list() 
        self.ex_spouses = list()

    def return_list(self):
        return [self.name, self.sex, self.birth, self.age, self.living, self.death_date, self.child, self.spouse, self.famc, self.fams, self.ex_spouses]


    def setAge(self): 
        if self.living:
            today = datetime.date.today()
        else:
            today = self.death_date
        self.age = (today - self.birth).days//365  #TBD: Not perfect. leap years, etc.

class GedcomFile:
    '''class GedcomFile'''

    _valid_tags: Dict[str, str] = {  'INDI' : '0', 'NAME' : '1', 'SEX' : '1', 'BIRT' : '1', 'DEAT' : '1', 'FAMC' : '1',
                                'FAMS' : '1', 'FAM' : '0', 'MARR' : '1', 'HUSB' : '1', 'WIFE' : '1', 'CHIL' : '1', 
                                'DIV' : '1', 'DATE' : '2', 'HEAD' : '0', 'TRLR' : '0', 'NOTE' : '0', } #key = tag : value = level
    
    
    # list has following format: [name,sex,birth,age.living,death,child,spouse,famc,fams]
    _Indiv_dt: Dict[str, list] = dict()
    _Family_dt: Dict[str, list] = dict()

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

    def write_to_txt_file(self, output_file_name: str) -> None:
        '''Writes the final formatted input and output lines to a txt file'''

        output_file: IO = open(f'{output_file_name}.txt', 'w')

        with output_file:
            for input_line, output_line in zip(self._input, self._output):
                output_file.write(f'--> {input_line}\n{output_line}\n')
        
        
    def update_validated_list(self) -> None:
        locallist = list()
        for entry in self._output:
            level, tag, validity, arg = entry.split("|")
            level = int(level[-1])
            if validity == 'Y':
                self._validated_list.append([level, tag, arg])
                
        #for entry in self._validated_list:
        #    print(entry)

    def convert_gedcom_date_to_datetime(date_str):
        day, month, year = date_str.split(" ")
        day = int(day)
        year = int(year)
        month = datetime.datetime.strptime(month, '%b').month
        return datetime.date(year, month, day)


    def record_individuals(self) -> None:
        # Flags indicating that we're in the middle of a higher-level record.
        indi_record = False
        birth_record = False
        death_record=False
        family_record = False
        
        for index in range (0, len(self._validated_list)):

          
            #print(self._validated_list[index][0])
            if self._validated_list[index][0] == 0:
                if indi_record == True:
                   # OK, we've finished processing the individual. Find relational information
                   indi_record = False
                   person.setAge()
                   
                   #print("person: ",person.id)
                   #print("person_return_list :", person.return_list())
                   self._Indiv_dt.update({id : person.return_list()})
                   #for entry in GedcomFile._Indiv_dt:
                   #print(GedcomFile._Indiv_dt)                   

                if "INDI" in self._validated_list[index][1] and indi_record == False:
                    # OK, we're now processing an Individual.
                    indi_record = True
                    
                    # Grab the ID and default everything else.
                    id = self._validated_list[index][2]
                    person = indiv(id)
            
            if indi_record == True:
                if birth_record:
                    if "DATE" in self._validated_list[index][1]:
                        date = self._validated_list[index][2]
                        person.birth = GedcomFile.convert_gedcom_date_to_datetime(date)
                        birth_record=False
                elif death_record:
                    if "DATE" in self._validated_list[index][1]:
                        date = self._validated_list[index][2]
                        person.death_date = GedcomFile.convert_gedcom_date_to_datetime(date)
                        death_record=False
    
                if "NAME" in self._validated_list[index][1]:
                    person.name = self._validated_list[index][2]
                elif "SEX" in self._validated_list[index][1]:
                    person.sex = self._validated_list[index][2]
                elif "BIRT" in self._validated_list[index][1]:
                    birth_record=True
                elif "DEAT" in self._validated_list[index][1]:
                    person.living = False
                    death_record=True
                elif "FAMC" in self._validated_list[index][1]:
                    person.famc = self._validated_list[index][2]
                elif "FAMS" in self._validated_list[index][1]:
                    person.fams.append(self._validated_list[index][2])     

    def print_individuals_pretty(self) -> None:
        x = PrettyTable()
        x.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse", "Ex-Spouses"]
        
        for entry in self._Indiv_dt:
            
            ex_spouses = ""
            for ex in self._Indiv_dt[entry][10]:
                ex_spouses=ex_spouses + ex + ","
            # remove last comma             
            ex_spouses = ex_spouses[0:-1]  

            temp_list = [
                   entry,                    # ID 
                   self._Indiv_dt[entry][0], # Name
                   self._Indiv_dt[entry][1], # Gender
                   self._Indiv_dt[entry][2], # Birthday
                   self._Indiv_dt[entry][3], # Age
                   self._Indiv_dt[entry][4], # Alive
                   self._Indiv_dt[entry][5], # Death
                   self._Indiv_dt[entry][6], # Child
                   self._Indiv_dt[entry][7], # Spouse
                   ex_spouses]               # Exes
            #print(type(temp_list))
            x.add_row(temp_list)
        print(x)


    def record_families(self) -> None:
        # Flags indicating that we're in the middle of a higher-level record.
        family_record = False
        divorce_record = False
        marriage_record = False
        
        for index in range (0, len(self._validated_list)):

            #print(self._validated_list[index][0])
            if self._validated_list[index][0] == 0:
                if family_record == True:
                   # OK, we've finished processing the family. Find relational information
                   family_record = False

                   self._Family_dt.update({id : fam.return_list()})
                   #self._Indiv_dt.update({id : person.return_list()})
             
                if self._validated_list[index][1] == "FAM" and family_record == False:
                    # OK, we're now processing a Family.
                    family_record = True
                    
                    # Grab the ID and default everything else.
                    id = self._validated_list[index][2]
                    fam = family(id)
            
            if family_record == True:
                if divorce_record:
                    if "DATE" in self._validated_list[index][1]:
                        date = self._validated_list[index][2]
                        fam.divorced = True
                        fam.divorce_date = GedcomFile.convert_gedcom_date_to_datetime(date)
                        divorce_record=False
                elif marriage_record:
                    if "DATE" in self._validated_list[index][1]:
                        date = self._validated_list[index][2]
                        fam.married = True
                        fam.marriage_date = GedcomFile.convert_gedcom_date_to_datetime(date)
                        marriage_record=False
    
                if "HUSB" in self._validated_list[index][1]:
                    fam.husband_id = self._validated_list[index][2]
                elif "WIFE" in self._validated_list[index][1]:
                    fam.wife_id = self._validated_list[index][2]
                elif "CHIL" in self._validated_list[index][1]:
                    fam.children.append(self._validated_list[index][2])
                elif "MARR" in self._validated_list[index][1]:
                    marriage_record=True
                elif "DIV" in self._validated_list[index][1]:
                    divorce_record = True


    def print_families_pretty(self) -> None:
        x = PrettyTable()
        x.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]
                
        for entry in self._Family_dt:
            children = ""
            
            for child in self._Family_dt[entry][5]:
                children=children + child + ","
             
            # remove last comma             
            children = children[0:-1]    
                
            husband_id = self._Family_dt[entry][3]
            try:
                husband_name = self._Indiv_dt[husband_id][0]
            except KeyError:
                husband_name = "Unknown"

            wife_id =    self._Family_dt[entry][4]
            try:
                wife_name = self._Indiv_dt[wife_id][0]                    
            except KeyError:
                wife_name = "Unknown"
                
            temp_list = [
                   entry,                     # ID 
                   self._Family_dt[entry][2], # Married
                   self._Family_dt[entry][7], # Divorced
                   husband_id,                # Husband ID
                   husband_name,              # Husband Name
                   wife_id,                   # Wife ID
                   wife_name,                 # Wife Name
                   children]                  # Children

            x.add_row(temp_list)

        print(x)
      

    def update_individual_child_references(self) -> None:
        for familyID in self._Family_dt:
            for childID in self._Family_dt[familyID][5]:
                try:
                    self._Indiv_dt[childID][6] = familyID
                except KeyError:
                    continue


    def update_individual_spouse_references(self) -> None:

        for familyID in self._Family_dt:
            husbID = self._Family_dt[familyID][3]
            wifeID = self._Family_dt[familyID][4]
            
            if not self._Family_dt[familyID][6]:
                # OK, these are current marriages
                try:
                    self._Indiv_dt[husbID][7] = wifeID
                except KeyError:
                    continue
                try:
                    self._Indiv_dt[wifeID][7] = husbID 
                except KeyError:
                    continue
            else:
                # These marriages ended in divorce
                try:
                    self._Indiv_dt[husbID][10].append(wifeID)
                except KeyError:
                    continue
                try:
                    self._Indiv_dt[wifeID][10].append(husbID) 
                except KeyError:
                    continue
        
        
                



def main() -> None:
    '''Creates an output file'''

    file_name: str = input('Enter GEDCOM file name: ')
    #file_name: str = "p1.ged"
    output_file_name: str = input('Enter desired name for the output file: ')
    #output_file_name: str = "p1.output"
    
    gedcom: GedcomFile = GedcomFile()
    gedcom.read_file(file_name)
    gedcom.validate_tags_for_output()
    gedcom.write_to_txt_file(output_file_name)
    print('Done. Your output file has been created.')
    
    gedcom.update_validated_list()
    gedcom.record_individuals()
    gedcom.record_families()
    
    gedcom.update_individual_child_references()
    gedcom.update_individual_spouse_references() 
    
    gedcom.print_individuals_pretty()
    gedcom.print_families_pretty()

'''
    # DEBUG
    for entry in gedcom._validated_list:
        print(entry)
    
    for entry in gedcom._Family_dt:
        print(entry, ": ", gedcom._Family_dt[entry])    
        
    for entry in gedcom._Indiv_dt:
        print(entry, ": ", gedcom._Indiv_dt[entry])
'''

if __name__ == '__main__':
    main()
