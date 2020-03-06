from controller.swapi_querier import *
from controller.cache import Cache
from model import * 

from collections import OrderedDict
import requests
import pytest


CACHE_ROOT = './.tmp_cache'
PERSON_CACHE = '{}/person.txt'.format(CACHE_ROOT)
PLANET_CACHE = '{}/planet.txt'.format(CACHE_ROOT)
STARSHIP_CACHE = '{}/starship.txt'.format(CACHE_ROOT)
VEHICLE_CACHE = '{}/vehicle.txt'.format(CACHE_ROOT)


@pytest.fixture
def cache():
    return Cache(PERSON_CACHE, PLANET_CACHE, STARSHIP_CACHE, VEHICLE_CACHE)


def test_get_id_num():
    assert get_id_num('https://swapi.co/api/people/1') == '1'
    assert get_id_num('https://swapi.co/api/planets/3') == '3'
    assert get_id_num('https://swapi.co/api/starships/5/') == '5'


def test_search_person(requests_mock, cache):
    requests_mock.get('https://swapi.co/api/people/?search=r2', 
        text="{"
        '"count": 1,'
        '"next": null,'
        '"previous": null,'
        '"results": ['
        '{'
            '"name": "R2-D2",'
            '"height": "96",'
            '"mass": "32",'
            '"hair_color": "n/a",'
            '"skin_color": "white, blue",'
            '"eye_color": "red",'
            '"birth_year": "33BBY",'
            '"gender": "n/a",'
            '"homeworld": "https://swapi.co/api/planets/8/",'
            '"films": ['
                '"https://swapi.co/api/films/2/",'
                '"https://swapi.co/api/films/5/",'
                '"https://swapi.co/api/films/4/",'
                '"https://swapi.co/api/films/6/",'
                '"https://swapi.co/api/films/3/",'
                '"https://swapi.co/api/films/1/",'
                '"https://swapi.co/api/films/7/"'
            '],'
            '"species": ['
                '"https://swapi.co/api/species/2/"'
            '],'
            '"vehicles": [],'
            '"starships": [],'
            '"created": "2014-12-10T15:11:50.376000Z",'
            '"edited": "2014-12-20T21:17:50.311000Z",'
            '"url": "https://swapi.co/api/people/3/"'
        '}'
    ']}')
    expected_person = Person('3', 'R2-D2', 'n/a', '8')

    assert search_person('r2', cache) == [expected_person]
    assert cache.persons == OrderedDict({'r2-d2': expected_person})


def test_search_person_nonexistent(requests_mock, cache):
    requests_mock.get('https://swapi.co/api/people/?search=potato', 
        text='{'
            '"count": 0,'
            '"next": null,'
            '"previous": null,'
            '"results": []'
        '}')

    assert search_person('potato', cache) == list()


def test_search_person_timeout(requests_mock, cache):
    requests_mock.get('https://swapi.co/api/people/?search=r2',
        exc=requests.exceptions.ConnectionError)
    assert search_person('r2', cache) == None


def test_get_planet(requests_mock, cache):
    requests_mock.get('https://swapi.co/api/planets/3/',
        text='{'
            '"name": "Yavin IV",'
            '"rotation_period": "24",'
            '"orbital_period": "4818",'
            '"diameter": "10200",'
            '"climate": "temperate, tropical",'
            '"gravity": "1 standard",'
            '"terrain": "jungle, rainforests",'
            '"surface_water": "8",'
            '"population": "1000",'
            '"residents": [],'
            '"films": ['
                '"https://swapi.co/api/films/1/"'
            '],'
            '"created": "2014-12-10T11:37:19.144000Z",''"edited": "2014-12-20T20:58:18.421000Z",'
            '"url": "https://swapi.co/api/planets/3/"'
        '}')

    expected_planet = Planet('3', 'Yavin IV', "1000", "temperate, tropical")
    assert get_planet('3', cache) == expected_planet
    assert cache.planets == OrderedDict({'3': expected_planet})


def test_get_planet_nonexistent(cache):
    import requests_mock
    requests_mock.Adapter().register_uri('GET', 
        url='https://swapi.co/api/planets/1000/', 
        status_code=404)
    assert get_planet('1000', cache, max_retries=1) == None


def test_get_planet_timeout(requests_mock, cache):
    requests_mock.get('https://swapi.co/api/planets/3/', 
        exc=requests.exceptions.ConnectionError)
    assert get_planet('3', cache) == None


def test_get_starship(requests_mock, cache):
    requests_mock.get('https://swapi.co/api/starships/9/', 
        text='{'
            '"name": "Death Star",'
            '"model": "DS-1 Orbital Battle Station",'
            '"manufacturer": "Imperial Department of Military Research, Sienar Fleet Systems",'
            '"cost_in_credits": "1000000000000",'
            '"length": "120000",'
            '"max_atmosphering_speed": "n/a",'
            '"crew": "342953",'
            '"passengers": "843342",'
            '"cargo_capacity": "1000000000000",'
            '"consumables": "3 years",'
            '"hyperdrive_rating": "4.0",'
            '"MGLT": "10",'
            '"starship_class": "Deep Space Mobile Battlestation",'
            '"pilots": [],'
            '"films": ['
                '"https://swapi.co/api/films/1/"'
            '],'
            '"created": "2014-12-10T16:36:50.509000Z",'
            '"edited": "2014-12-22T17:35:44.452589Z",'
            '"url": "https://swapi.co/api/starships/9/"'
        '}')

    expected_starship = Starship('9', 'DS-1 Orbital Battle Station', 'Deep Space Mobile Battlestation',
        '4.0', '1000000000000', 'Imperial Department of Military Research, Sienar Fleet Systems')

    assert get_starship('9', cache) == expected_starship
    assert cache.starships == OrderedDict({'9': expected_starship})


def test_get_starship_nonexistent(cache):
    import requests_mock
    requests_mock.Adapter().register_uri('GET', 
        url='https://swapi.co/api/starships/1000/', 
        status_code=404)
    assert get_starship('1000', cache, max_retries=1) == None


def test_get_starship_timeout(requests_mock, cache):
    requests_mock.get('https://swapi.co/api/starships/9/', 
        exc=requests.exceptions.ConnectionError)
    assert get_starship('9', cache) == None


def test_get_vehicle(requests_mock, cache):
    requests_mock.get('https://swapi.co/api/vehicles/4/', 
        text='{'
            '"name": "Sand Crawler",'
            '"model": "Digger Crawler",'
            '"manufacturer": "Corellia Mining Corporation",'
            '"cost_in_credits": "150000",'
            '"length": "36.8",'
            '"max_atmosphering_speed": "30",'
            '"crew": "46",'
            '"passengers": "30",'
            '"cargo_capacity": "50000",'
            '"consumables": "2 months",'
            '"vehicle_class": "wheeled",'
            '"pilots": [],'
            '"films": ['
                '"https://swapi.co/api/films/5/",'
                '"https://swapi.co/api/films/1/"'
                '],'
            '"created": "2014-12-10T15:36:25.724000Z",'
            '"edited": "2014-12-22T18:21:15.523587Z",'
            '"url": "https://swapi.co/api/vehicles/4/"'
        '}')

    expected_vehicle = Vehicle('4', 'Sand Crawler', 'Digger Crawler', '150000')

    assert get_vehicle('4', cache) == expected_vehicle
    assert cache.vehicles == OrderedDict({'4': expected_vehicle})


def test_get_vehicle_nonexistent(cache):
    import requests_mock
    requests_mock.Adapter().register_uri('GET', 
        url='https://swapi.co/api/vehicles/1000/', 
        status_code=404)
    assert get_vehicle('1000', cache, max_retries=1) == None


def test_get_vehicle_timeout(requests_mock, cache):
    requests_mock.get('https://swapi.co/api/vehicles/4/', 
        exc=requests.exceptions.ConnectionError)
    assert get_vehicle('4', cache) == None
