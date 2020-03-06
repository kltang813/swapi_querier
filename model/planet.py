from model.rebelparticulars import RebelParticulars

from datetime import datetime


class Planet(RebelParticulars): 
    """
    Information about a Planet.
    """
    def __init__(self, id_num, name, population, climate, query_date=None):
        """
        Inputs:
        -----
        id_num: str
            ID number of planet
        name: str
            Name of planet
        population: str
            Population size of planet
        climate: str
            Climakte of planet
        query_date: date (optional)
            Date of query
        """
        self.id = id_num
        self.name = name
        self.population = population
        self.climate = climate
        self.query_date = query_date or datetime.now().date()

    def to_cache_dict(self): 
        return {'id': self.id, 
                'name': self.name, 
                'population': self.population, 
                'climate': self.climate, 
                'query_date': self.query_date.strftime('%d-%m-%Y')}

    def __eq__(self, other):
        return((self.id, self.name, self.population, self.climate, self.query_date)
            == (other.id, other.name, other.population, other.climate, other.query_date))