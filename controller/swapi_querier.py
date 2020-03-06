from controller.logging_utils import logging
from model import *

from time import sleep
import requests
import json
import re


logger = logging.getLogger('SWAPI_Querier')

TIMEOUT = 10  # Timeout in seconds
MAX_RETRIES = 10  # Max number of times to retry if connection failes
DELAY = 0.05  # Delay in seconds between connection retries

BASE_URL = 'https://swapi.co/api/'


def get_id_num(url):
    """
    Get id number from URL
    """
    return re.findall(r'.*/(\d+)/?$', url)[0]


def search_person(name, cache, max_retries=MAX_RETRIES):
    """
    Search for a person by name using SWAPI API

    Inputs: 
    -----
    name: str
        Complete or part of name of a person

    Returns: 
    -----
    Person 
    """
    query_url = '{}people/?search={}'.format(BASE_URL, name)
    for i in range(max_retries):
        try:
            res = requests.get(query_url, timeout=TIMEOUT)
            if res.status_code == 200:
                json_res = json.loads(res.text)

                persons = list()
                for r in json_res['results']:
                    p = Person(id_num=get_id_num(r['url']),
                               name=r['name'], 
                               gender=r['gender'], 
                               homeworld=get_id_num(r['homeworld']), 
                               starships=[get_id_num(s) for s in r['starships']], 
                               vehicles=[get_id_num(v) for v in r['vehicles']])
                    cache.add_person(p)
                    persons.append(p)
                return persons
            else:
                logger.warning('Query for {} failed with {}. {} retries left.'.format(name, res.status_code, MAX_RETRIES-i))
        except requests.exceptions.Timeout: 
            logger.warning('Query for {} timed out. {} retries left.'.format(name, MAX_RETRIES-i))
            sleep(DELAY)
        except requests.exceptions.ConnectionError:
            logger.warning('No connection.')
            break

    return None


def get_planet(id_num, cache, max_retries=MAX_RETRIES):
    query_url = '{}planets/{}/'.format(BASE_URL, id_num)

    for i in range(max_retries):
        try: 
            res = requests.get(query_url, timeout=TIMEOUT)

            if res.status_code == 200:
                json_res = json.loads(res.text)
                pl = Planet(id_num=id_num,
                            name=json_res['name'],
                            population=json_res['population'], 
                            climate=json_res['climate'])
                cache.add_planet(pl)
                return pl
            else: 
                logger.warning('Query for planet {} failed with {}. {} retries left.'.format(id_num, res.status_code, MAX_RETRIES-i))
        except requests.exceptions.Timeout: 
            logger.warning('Query for planet {} timed out. {} retries left.'.format(id_num, MAX_RETRIES-i))
            sleep(DELAY)
        except requests.exceptions.ConnectionError:
            logger.warning('No connection.')
            break

    return None


def get_starship(id_num, cache, max_retries=MAX_RETRIES):
    query_url = '{}starships/{}/'.format(BASE_URL, id_num)

    for i in range(max_retries):
        try: 
            res = requests.get(query_url, timeout=TIMEOUT)

            if res.status_code == 200:
                json_res = json.loads(res.text)
                s = Starship(id_num=id_num,
                             model=json_res['model'], 
                             s_class=json_res['starship_class'],
                             hdrive_rating=json_res['hyperdrive_rating'],
                             cost=json_res['cost_in_credits'],
                             manufacturer=json_res['manufacturer'])
                cache.add_starship(s)
                return s
            else: 
                logger.warning('Query for starship {} failed with {}. {} retries left.'.format(id_num, res.status_code, MAX_RETRIES-i))
        except requests.exceptions.Timeout:
            logger.warning('Query for planet {} timed out. {} retries left.'.format(id_num, MAX_RETRIES-i))
            sleep(DELAY)
        except requests.exceptions.ConnectionError:
            logger.warning('No connection.')
            break


def get_vehicle(id_num, cache, max_retries=MAX_RETRIES):
    query_url = '{}vehicles/{}/'.format(BASE_URL, id_num)

    for i in range(max_retries):
        try: 
            res = requests.get(query_url, timeout=TIMEOUT)

            if res.status_code == 200:
                json_res = json.loads(res.text)
                v = Vehicle(id_num=id_num,
                            name=json_res['name'], 
                            model=json_res['model'], 
                            cost=json_res['cost_in_credits'])
                cache.add_vehicle(v)
                return v
            else: 
                logger.warning('Query for vehicle {} failed with {}. {} retries left.'.format(id_num, res.status_code, MAX_RETRIES-i))
        except requests.exceptions.Timeout:
            logger.warning('Query for vehicle {} timed out. {} retries left.'.format(id_num, MAX_RETRIES-i))
            sleep(delay)
        except requests.exceptions.ConnectionError:
            logger.warning('No connection.')
            break
