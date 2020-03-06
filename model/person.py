from model.rebelparticulars import RebelParticulars

from datetime import datetime


class Person(RebelParticulars): 
    """
    Information about a Person.
    """
    def __init__(self, id_num, name, gender, homeworld, 
            query_date=None, starships=None, vehicles=None):
        """
        Inputs:
        -----
        id_num: str
            ID number of person
        name: str
            Name of person
        gender: str
            Gender of person
        homeworld: str
            ID number of person's homeworld
        query_date: date (optional)
            Date of query
        starships: list of str
            ID numbers of starships owned by person
        vehicles: list of str
            ID numbers of vehicles owned by person
        """
        self.id = id_num
        self.name = name 
        self.gender = gender 
        self.homeworld = homeworld
        self.starships = starships or list()
        self.vehicles = vehicles or list()
        self.query_date = query_date or datetime.now().date()

    def to_cache_dict(self):
        return {'id': self.id, 
                'name': self.name, 
                'gender': self.gender,
                'homeworld': self.homeworld, 
                'starships': ','.join(self.starships) if self.starships else '', 
                'vehicles': ','.join(self.vehicles) if self.vehicles else '', 
                'query_date': self.query_date.strftime('%d-%m-%Y')}

    def __eq__(self, other):
        return (self.id == other.id and
            self.name == other.name and
            self.gender == other.gender and 
            self.homeworld == other.homeworld and
            self.starships == other.starships and
            self.vehicles == other.vehicles and
            self.query_date == other.query_date)