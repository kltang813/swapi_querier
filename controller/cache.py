from controller.csv_util import csv_reader, csv_writer
from controller.logging_utils import logging
from datetime import datetime, timedelta
from collections import OrderedDict
from model import *

import schedule
import os

logger = logging.getLogger('Cache')


PERSON_HEADER = ['id', 'name', 'gender', 'homeworld', 'starships', 
                 'vehicles', 'query_date']
PLANET_HEADER = ['id', 'name', 'population', 'climate', 'query_date']
STARSHIP_HEADER = ['id', 'model', 'class', 'hdrive_rating', 'cost', 
                   'manufacturer', 'query_date']
VEHICLE_HEADER = ['id', 'name', 'model', 'cost', 'query_date']

CACHE_REFRESH_DELTA = timedelta(7)  # remove cache entry if it is >= 7 days old

class Cache:
    def __init__(self, person_cache, planet_cache, starship_cache, vehicle_cache):
        self.person_cache = person_cache 
        self.planet_cache = planet_cache
        self.starship_cache = starship_cache
        self.vehicle_cache = vehicle_cache

        self.parse_from_cache()

        schedule.every(10).minutes.do(self.write_to_cache)
        schedule.every().day.at("00:00").do(self.remove_outdated_entries)

    def parse_from_cache(self):
        today = datetime.now().date()

        # Store objects in OrderedDict so that we can maintain sorted order by query date
        self.persons = OrderedDict()
        self.planets = OrderedDict() 
        self.starships = OrderedDict()
        self.vehicles = OrderedDict()

        if os.path.isfile(self.person_cache):
            for row in csv_reader(self.person_cache): 
                query_date = datetime.strptime(row[6], '%d-%m-%Y').date()
                if today - query_date < CACHE_REFRESH_DELTA:
                    self.persons[row[1].lower()] = Person(id_num=row[0], 
                                             name=row[1],
                                             gender=row[2],
                                             homeworld=row[3], 
                                             starships=row[4].split(',') if len(row[4]) > 0 else None, 
                                             vehicles=row[5].split(',') if len(row[5]) > 0 else None, 
                                             query_date=query_date)
        else: 
            os.makedirs(os.path.dirname(self.person_cache), exist_ok=True)

        if os.path.isfile(self.planet_cache):
            for row in csv_reader(self.planet_cache): 
                query_date = datetime.strptime(row[4], '%d-%m-%Y').date()
                if today - query_date < CACHE_REFRESH_DELTA:
                    self.planets[row[0]] = Planet(id_num=row[0], 
                                             name=row[1], 
                                             population=row[2],
                                             climate=row[3], 
                                             query_date=query_date)
        else: 
            os.makedirs(os.path.dirname(self.planet_cache), exist_ok=True)

        if os.path.isfile(self.starship_cache):
            for row in csv_reader(self.starship_cache): 
                query_date = datetime.strptime(row[6], '%d-%m-%Y').date()
                if today - query_date < CACHE_REFRESH_DELTA:
                    self.starships[row[0]] = Starship(id_num=row[0], 
                                                 model=row[1],
                                                 s_class=row[2], 
                                                 hdrive_rating=row[3],
                                                 cost=row[4], 
                                                 manufacturer=row[5],
                                                 query_date=query_date)
        else:
            os.makedirs(os.path.dirname(self.starship_cache), exist_ok=True)

        if os.path.isfile(self.vehicle_cache):
            for row in csv_reader(self.vehicle_cache):
                query_date = datetime.strptime(row[4], '%d-%m-%Y').date()
                if today - query_date < CACHE_REFRESH_DELTA:
                    self.vehicles[row[0]] = Vehicle(id_num=row[0],
                                               name=row[1],
                                               model=row[2],
                                               cost=row[3],
                                               query_date=query_date)
        else: 
            os.makedirs(os.path.dirname(self.vehicle_cache), exist_ok=True)


    def write_to_cache(self):
        def get_cache_entries(obj_list, header):
            for o in obj_list: 
                o = o.to_cache_dict()

                entry = list()
                for h in header:
                    entry.append(o[h])
                yield entry

        if len(self.persons) > 0:
            csv_writer(self.person_cache, get_cache_entries(self.persons.values(), PERSON_HEADER))
        if len(self.planets) > 0:
            csv_writer(self.planet_cache, get_cache_entries(self.planets.values(), PLANET_HEADER))
        if len(self.starships) > 0: 
            csv_writer(self.starship_cache, get_cache_entries(self.starships.values(), STARSHIP_HEADER))
        if len(self.vehicles) > 0: 
            csv_writer(self.vehicle_cache, get_cache_entries(self.vehicles.values(), VEHICLE_HEADER))


    def remove_outdated_entries(self):
        today = datetime.now().date()


        for p_k in list(self.persons.keys()):
            if today - self.persons[p_k].query_date >= CACHE_REFRESH_DELTA:
                del self.persons[p_k]

        for pl_k in list(self.planets.keys()):
            if today - self.planets[pl_k].query_date >= CACHE_REFRESH_DELTA:
                del self.planets[pl_k]

        for s_k in list(self.starships.keys()):
            if today - self.starships[s_k].query_date >= CACHE_REFRESH_DELTA:
                del self.starships[s_k]

        for v_k in list(self.vehicles.keys()):
            if today - self.vehicles[v_k].query_date >= CACHE_REFRESH_DELTA:
                del self.vehicles[v_k]

    def add_person(self, person):
        if person.name.lower() in self.persons:
            logger.info('Person ID already exists in cache. Skipping.')
        else: 
            self.persons[person.name.lower()] = person

    def add_planet(self, planet):
        if planet.id in self.planets:
            logger.info('Planet ID already exists in cache. Skipping.')
        else:
            self.planets[planet.id] = planet

    def add_starship(self, starship):
        if starship.id in self.starships:
            logger.info('Starship ID already exists in cache. Skipping.')
        else: 
            self.starships[starship.id] = starship

    def add_vehicle(self, vehicle):
        if vehicle.id in self.vehicles:
            logger.info('Vehicle ID already exists in cache. Skipping.')
        else: 
            self.vehicles[vehicle.id] = vehicle

    def get_person(self, name):
        if name.lower() in self.persons:
            return [self.persons[name.lower()]]
        else:
            return None

    def get_planet(self, id_num):
        if id_num in self.planets:
            return self.planets[id_num]
        else: 
            return None

    def get_starship(self, id_num):
        if id_num in self.starships:
            return self.starships[id_num]
        else: 
            return None

    def get_vehicle(self, id_num):
        if id_num in self.vehicles:
            return self.vehicles[id_num]
        else: 
            return None