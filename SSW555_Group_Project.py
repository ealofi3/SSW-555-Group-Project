'''The purpose of this program is to read a GEDCOM file, print "--> <input line>", and print "<-- <level>|<tag>|<valid?> : Y or N|<arguments>" '''

from typing import Iterator, Tuple, IO, List, Dict
import datetime
import os

class family:
    def __init__(self, id):
        self.id = id
        self.married = False
        self.marriage_date = datetime.date(1,1,1)
        self.husband_id = str()
        self.wife_id = str()
        self.children = list()
        self.divorced = False
        self.divorce_date = datetime.date(1,1,1)

class indiv:
    def __init__(self, id):
        # Grab the ID and default everything else.
        self.id = id
        self.name = str()
        self.sex = str()
        self.birth = datetime.date(1,1,1)
        self.age = "TBD"
        self.living = True
        self.death_date = datetime.date(1,1,1)
        self.child = "TBD"
        self.spouse = "TBD"
        self.famc = "NA"
        self.fams = "NA"  

    def return_list(self):
        return [self.name, self.sex, self.birth, self.age, self.living, self.death_date, self.child, self.spouse, self.famc, self.fams]

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
                    person.fams = self._validated_list[index][2]     


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
    
    
    # DEBUG
    for entry in gedcom._validated_list:
        print(entry)

    for entry in gedcom._Indiv_dt:
        print(gedcom._Indiv_dt[entry])
    
if __name__ == '__main__':
    main()
