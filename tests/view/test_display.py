from view.display import person_str
from model import * 


import pytest


@pytest.fixture
def person():
    return Person("1", "Luke Skywalker", "male", "1", 
            starships=["12", "22"], vehicles=["14", "30"])


@pytest.fixture
def planet():
    return Planet("1", "Tatooine", "200000", "arid")


@pytest.fixture
def starships():
    return [
        Starship("12", "T-65 X-wing", "Starfighter", "1.0", 
            "149999", "Incom Corporation"),
        Starship("22", "Lambda-class T-4a shuttle", "Armed government transport",
            "1.0", "240000", "Sienar Fleet Systems")
        ]

@pytest.fixture
def vehicles():
    return [
        Vehicle("14", "Snowspeeder", "t-47 airspeeder", "unknown"),
        Vehicle("30", "Imperial Speeder Bike", "74-Z speeder bike", "8000")
        ]

def test_person_str(person, planet, starships, vehicles):
    assert person_str(person, starships, vehicles, planet) \
        == 'Name: Luke Skywalker\n'\
        + 'Gender: male\n'\
        + 'Starships: \n'\
        + '\t - Model: T-65 X-wing\n'\
        + '\t   Class: Starfighter\n'\
        + '\t   Hyperdrive Rating: 1.0\n'\
        + '\t   Cost: 149999 credit(s)\n'\
        + '\t   Manufacturer: Incom Corporation\n\n'\
        + '\t - Model: Lambda-class T-4a shuttle\n'\
        + '\t   Class: Armed government transport\n'\
        + '\t   Hyperdrive Rating: 1.0\n'\
        + '\t   Cost: 240000 credit(s)\n'\
        + '\t   Manufacturer: Sienar Fleet Systems\n\n'\
        + 'Vehicles: \n' \
        + '\t - Name: Snowspeeder\n' \
        + '\t   Model: t-47 airspeeder\n'\
        + '\t   Cost: unknown\n\n'\
        + '\t - Name: Imperial Speeder Bike\n'\
        + '\t   Model: 74-Z speeder bike\n'\
        + '\t   Cost: 8000 credit(s)\n\n' \
        + 'Homeworld: \n'\
        + '\tName: Tatooine\n'\
        + '\tPopulation: 200000\n'\
        + '\tClimate: arid'
