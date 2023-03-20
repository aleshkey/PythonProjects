import xml.etree.ElementTree as ET

from Lab2.src.checkers.Checker import Checker
from Lab2.src.erorrs.DateIsNotValid import DateIsNotValid
from Lab2.src.models.pet import Pet


class PetDAO:

    path = ''

    SIZE = 20

    def read(self):
        tree = ET.parse(self.path)
        root = tree.getroot()
        pets = []
        for child in root:
            pet = Pet()
            pet.name = child.find("name").text
            pet.birth_date = child.find("birth_date").text
            pet.date_of_last_admission = child.find("date_of_last_admission").text
            pet.veterinarians_name = child.find("veterinarians_name").text
            pet.diagnosis = child.find("diagnosis").text
            pets.append(pet)
        return pets

    def write(self, lst: list):
        data = ET.Element('data')
        for elem in lst:
            pet = ET.SubElement(data, 'pet')
            name = ET.SubElement(pet, 'name')
            name.text = elem.name
            birth_date = ET.SubElement(pet, 'birth_date')
            birth_date.text = elem.birth_date
            date_of_last_admission = ET.SubElement(pet, 'date_of_last_admission')
            date_of_last_admission.text = elem.date_of_last_admission
            veterinarians_name = ET.SubElement(pet, 'veterinarians_name')
            veterinarians_name.text = elem.veterinarians_name
            diagnosis = ET.SubElement(pet, 'diagnosis')
            diagnosis.text = elem.diagnosis
        ET.ElementTree(data).write(self.path)

    def add(self, pet):
        lst = self.read()
        lst.insert(0, pet)
        self.write(lst)

    def find_by_name(self, name: str):
        return [x for x in self.read() if x.name == name]

    def find_by_birth_date(self, birth_date):
        if Checker.date_is_valid(birth_date):
            return [x for x in self.read() if x.birth_date == birth_date]
        else:
            raise DateIsNotValid("correct input dd.mm.yyyy")

    def find_by_date_of_last_admission(self, date_of_last_admission):
        if Checker.date_is_valid(date_of_last_admission):
            return [x for x in self.read() if x.date_of_last_admission == date_of_last_admission]
        else:
            raise DateIsNotValid("correct input dd.mm.yyyy")

    def find_by_veterinarians_name(self, veterinarians_name):
        return [x for x in self.read() if x.veterinarians_name == veterinarians_name]

    def find_by_part_or_diagnosis(self, part_of_diagnosis):
        return [x for x in self.read() if part_of_diagnosis.lower() in x.diagnosis.lower()]

    def combining(self, lst1, lst2):
        res = []
        for i in lst1:
            for j in lst2:
                if str(i) == str(j):
                    res.append(i)
        return res

    def get_page(self, index):
        lst = []
        if self.path != '':
            if len(self.read()) > self.SIZE * (index+1):
                for i in range(self.SIZE):
                    lst.append(self.read()[i + self.SIZE * index])
            else:
                r = len(self.read()) - self.SIZE*index
                for i in range(r):
                    lst.append(self.read()[i + self.SIZE*index])
            return lst

    def get_first_page(self):
        return self.get_page(0)

    def delete_by_name_and_birth_date(self, name, birth_date):
        pets = self.read()
        for pet in pets:
            if pet.name == name and pet.birth_date == birth_date:
                pets.remove(pet)
        self.write(pets)

    def delete_by_veterinarians_name_and_date_of_last_admission(self, veterinarians_name, date_of_last_admission):
        pets = self.read()
        for pet in pets:
            if pet.veterinarians_name == veterinarians_name and pet.date_of_last_admission == date_of_last_admission:
                pets.remove(pet)
        self.write(pets)

    def delete_by_part_of_diagnosis(self, part_of_diagnosis):
        pets = self.read()
        for pet in pets:
            if part_of_diagnosis in pet.diagnosis:
                pets.remove(pet)
        self.write(pets)
    def get_last_page(self):
        index = int((len(self.read())-1)/self.SIZE)
        return self.get_page(index)
