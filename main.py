from controller.swapi_querier import search_person, get_planet, get_starship, get_vehicle
from config import person_cache, planet_cache, starship_cache, vehicle_cache
from controller.cache import Cache
from view.display import *


if __name__ == '__main__':
    display_greeting()
    cache = Cache(person_cache, planet_cache, starship_cache, vehicle_cache)

    while True:
        try:
            query = get_query()
            res = cache.get_person(query) or search_person(query, cache)

            if res is None: 
                display_error()
            else:
                if len(res) == 0:
                    display_unknown()
                    continue

                for r in res:
                    starships = [cache.get_starship(s) or get_starship(s, cache) for s in r.starships]
                    vehicles = [cache.get_vehicle(v) or get_vehicle(v, cache) for v in r.vehicles] \
                                if r.vehicles is not None else None
                    homeworld = cache.get_planet(r.homeworld) or get_planet(r.homeworld, cache)

                    display_person(r, starships, vehicles, homeworld)

        except KeyboardInterrupt:
            print()
            display_farewell()
            cache.write_to_cache()
            break