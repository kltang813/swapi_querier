from model.rebelparticulars import RebelParticulars

from datetime import datetime


class Starship(RebelParticulars):
    """
    Information about a Starship
    """ 
    def __init__(self, id_num, model, s_class, hdrive_rating, cost, manufacturer, query_date=None): 
        """
        Inputs:
        -----
        id_num: str
            ID number of starship
        model: str
            Model name of starship
        s_class: str
            Class of starship
        hdrive_rating: str
            Hyperdrive rating of starship
        cost: str
            Cost of starship in credits
        manufacturer: str
            Manufacturer of starship
        query_date: date (optional)
            Date of query
        """
        self.id = id_num
        self.model = model
        self.s_class = s_class
        self.hdrive_rating = hdrive_rating
        self.cost = cost
        self.manufacturer = manufacturer
        self.query_date = query_date or datetime.now().date()

    def to_cache_dict(self):
        return {'id': self.id, 
                'model': self.model, 
                'class': self.s_class, 
                'hdrive_rating': self.hdrive_rating,
                'cost': self.cost, 
                'manufacturer': self.manufacturer, 
                'query_date': self.query_date.strftime('%d-%m-%Y')}

    def __eq__(self, other):
        return ((self.id, self.model, self.s_class, self.hdrive_rating,
            self.cost, self.manufacturer, self.query_date)
        == (other.id, other.model, other.s_class, other.hdrive_rating,
            other.cost, other.manufacturer, other.query_date))