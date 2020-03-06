from model.rebelparticulars import RebelParticulars

from datetime import datetime


class Vehicle(RebelParticulars): 
    """
    Information about a Vehicle
    """
    def __init__(self, id_num, name, model, cost, query_date=None): 
        """
        Input:
        ----
        id_num: str
            ID number of vehicle
        name: str
            Name of vehicle
        model: str
            Model name of vehicle
        cost: str
            Cost of vehicle in credits
        query_date: date (optional)
            Query date
        """
        self.id = id_num
        self.name = name
        self.model = model
        self.cost = cost
        self.query_date = query_date or datetime.now().date()

    def to_cache_dict(self):
        return {'id': self.id, 
                'name': self.name, 
                'model': self.model, 
                'cost': self.cost, 
                'query_date': self.query_date.strftime('%d-%m-%Y')}

    def __eq__(self, other):
        return ((self.id, self.name, self.model, self.cost, self.query_date)
            == (other.id, other.name, other.model, other.cost, other.query_date))