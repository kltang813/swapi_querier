from controller.cache import Cache
from model import *

from collections import OrderedDict
from datetime import datetime
from shutil import rmtree
import pytest
import os


CACHE_ROOT = './.tmp_cache'
PERSON_CACHE = '{}/person.txt'.format(CACHE_ROOT)
PLANET_CACHE = '{}/planet.txt'.format(CACHE_ROOT)
STARSHIP_CACHE = '{}/starship.txt'.format(CACHE_ROOT)
VEHICLE_CACHE = '{}/vehicle.txt'.format(CACHE_ROOT)


@pytest.fixture
def expected_persons():
    return OrderedDict({
        'luke skywalker': Person("1", "Luke Skywalker", "male", "1", 
            starships=["12", "22"], vehicles=["14", "30"])
        })


@pytest.fixture
def expected_planets():
    return OrderedDict({
        '1': Planet("1", "Tatooine", "200000", "arid")
        })


@pytest.fixture
def expected_starships():
    return OrderedDict({
        '12': Starship("12", "T-65 X-wing", "Starfighter", "1.0", 
            "149999", "Incom Corporation"),
        '22': Starship("22", "Lambda-class T-4a shuttle", "Armed government transport",
            "1.0", "240000", "Sienar Fleet Systems")
        })

@pytest.fixture
def expected_vehicles():
    return OrderedDict({
        '14': Vehicle("14", "Snowspeeder", "t-47 airspeeder", "unknown"),
        '30': Vehicle("30", "Imperial Speeder Bike", "74-Z speeder bike", "8000")
        })


@pytest.fixture
def cache(expected_persons, expected_planets, expected_starships, expected_vehicles):
    cache = Cache(PERSON_CACHE, PLANET_CACHE, STARSHIP_CACHE, VEHICLE_CACHE)
    cache.add_person(expected_persons['luke skywalker'])
    cache.add_planet(expected_planets['1'])
    cache.add_starship(expected_starships['12'])
    cache.add_starship(expected_starships['22'])
    cache.add_vehicle(expected_vehicles['14'])
    cache.add_vehicle(expected_vehicles['30'])
    return cache

def clear_cache(): 
    rmtree(CACHE_ROOT)


def test_add_person(cache, expected_persons): 
    assert cache.persons == expected_persons


def test_add_planet(cache, expected_planets):
    assert cache.planets == expected_planets


def test_add_starships(cache, expected_starships):
    assert cache.starships == expected_starships


def test_add_vehicles(cache, expected_vehicles):
    assert cache.vehicles == expected_vehicles


def test_write_to_cache(cache):
    cache.write_to_cache()

    with open(PERSON_CACHE) as f:
        assert f.read() == '1,"Luke Skywalker",male,1,"12,22","14,30",{}'\
            .format(datetime.now().strftime('%d-%m-%Y'))

    with open(PLANET_CACHE) as f:
        assert f.read() == '1,Tatooine,200000,arid,{}'.format(datetime.now().strftime("%d-%m-%Y"))

    with open(STARSHIP_CACHE) as f:
        assert f.read() == '12,"T-65 X-wing",Starfighter,1.0,149999,"Incom Corporation",{}\n'.format(datetime.now().strftime("%d-%m-%Y")) \
            + '22,"Lambda-class T-4a shuttle","Armed government transport",1.0,240000,"Sienar Fleet Systems",{}'.format(datetime.now().strftime("%d-%m-%Y"))

    with open(VEHICLE_CACHE) as f:
        assert f.read() == '14,Snowspeeder,"t-47 airspeeder",unknown,{}\n'.format(datetime.now().strftime('%d-%m-%Y'))\
            + '30,"Imperial Speeder Bike","74-Z speeder bike",8000,{}'.format(datetime.now().strftime('%d-%m-%Y'))

    clear_cache()


def test_parse_from_cache(cache):
    os.makedirs(CACHE_ROOT, exist_ok=True)

    with open(PERSON_CACHE, 'w') as f:
        f.write('1,"Not A Person",female,30,,"30,20",{}\n'.format(datetime(2020,1, 1).strftime("%d-%m-%Y"))
                + '100,"Another Person",male,100,"33,44",1,{}\n'.format(datetime.now().strftime('%d-%m-%Y')))

    with open(PLANET_CACHE, 'w') as f:
        f.write('5,Earth,7530000000,"tropical,temperate",{}'.format(datetime.now().strftime('%d-%m-%Y')))

    with open(STARSHIP_CACHE, 'w') as f:
        f.write('3,"Some Starship","Very Good",1.0,300000,"Suzuki",{}'.format(datetime.now().strftime('%d-%m-%Y')))

    with open(VEHICLE_CACHE, 'w') as f:
        f.write('1000,Car,Sedan,1000,{}\n'.format(datetime.now().strftime('%d-%m-%Y'))
                + '3,"Electric Scooter","Motorized Kick Scooter",300,{}'.format(datetime.now().strftime('%d-%m-%Y')))

    cache.parse_from_cache()
    assert cache.persons == OrderedDict({
        'another person': Person('100','Another Person','male','100',
            starships=["33","44"], vehicles=["1"])
        })
    assert cache.planets == OrderedDict({
        '5': Planet('5', 'Earth', '7530000000', 'tropical,temperate')
        })
    assert cache.starships == OrderedDict({
        '3': Starship('3', 'Some Starship', 'Very Good', '1.0', '300000',
            'Suzuki')
        })
    assert cache.vehicles == OrderedDict({
        '1000': Vehicle('1000', 'Car', 'Sedan', '1000'),
        '3': Vehicle('3', 'Electric Scooter', 'Motorized Kick Scooter', '300')
        })

    clear_cache()


def test_remove_outdated_entries_person(cache, expected_persons):
    new_person = Person('3', 'Nobody', 'male', '11', query_date=datetime(2020,1,1).date(),
        starships=None, vehicles=None)
    cache.add_person(new_person)
    expected_persons['nobody'] = new_person
    assert cache.persons == expected_persons

    cache.remove_outdated_entries()
    del expected_persons['nobody']
    assert cache.persons == expected_persons


def test_remove_outdated_entries_planets(cache, expected_planets):
    new_planet = Planet('5', 'Mars', '0', 'arid', query_date=datetime(2020,1,1).date())
    cache.add_planet(new_planet)
    expected_planets['5'] = new_planet
    assert cache.planets == expected_planets

    cache.remove_outdated_entries()
    del expected_planets['5']
    assert cache.planets == expected_planets


def test_remove_outdated_entries_starships(cache, expected_starships):
    new_starship = Starship('23', 'Very Fast', 'Kite', '1.0', '300000', 'Paper', 
        query_date=datetime(2020,1,1).date())
    cache.add_starship(new_starship)
    expected_starships['23'] = new_starship
    assert cache.starships == expected_starships

    cache.remove_outdated_entries()
    del expected_starships['23']
    assert cache.starships == expected_starships


def test_remove_outdated_entries_vehicles(cache, expected_vehicles):
    new_vehicle = Vehicle('121', 'Skates', 'Inline', '10', query_date=datetime(2020,1,1).date())
    cache.add_vehicle(new_vehicle)
    expected_vehicles['121'] = new_vehicle
    assert cache.vehicles == expected_vehicles

    cache.remove_outdated_entries()
    del expected_vehicles['121']
    assert cache.vehicles == expected_vehicles


def test_get_person(cache, expected_persons):
    assert cache.get_person('luke skywalker') == [expected_persons['luke skywalker']]


def test_get_person_none(cache):
    assert cache.get_person('frog') is None


def test_get_planet(cache, expected_planets):
    assert cache.get_planet('1') == expected_planets['1']


def test_get_planet_none(cache):
    assert cache.get_planet('300') is None


def test_get_starship(cache, expected_starships):
    assert cache.get_starship('12') == expected_starships['12']


def test_get_starship_none(cache):
    assert cache.get_starship('300') is None


def test_get_vehicle(cache, expected_vehicles):
    assert cache.get_vehicle('30') == expected_vehicles['30']


def test_get_vehicle_none(cache):
    assert cache.get_vehicle('10232') is None