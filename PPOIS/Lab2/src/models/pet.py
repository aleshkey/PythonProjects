class Pet:
    name = ''
    birth_date = ''
    date_of_last_admission = ''
    veterinarians_name = ''
    diagnosis = ''

    def __str__(self) -> str:
        return "name: "+self.name+", birth date: "+self.birth_date+", veterinarians name: "+self.veterinarians_name+\
                ", date of last admission: "+self.date_of_last_admission+", diagnosis: "+self.diagnosis
    