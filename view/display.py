LINE_BREAK_HYPHENS = 25

def print_line_break(count=1):
    for i in range(count):
        print('-' * LINE_BREAK_HYPHENS)

def display_greeting():
    print_line_break(2)
    print('Imperial Military of the Galactic Empire\n'
          'Intelligence Division\n'
          'MyRebelQuery System v1.13.8')
    print_line_break(2)
    print('\nGreetings, Lord Vader.\n')
    print_line_break()


def display_farewell():
    print_line_break()
    print('\nFarewell, Lord Vader. May the Force serve you well.\n')
    print_line_break()


def get_query():
    print('Enter rebel\'s name (press ctrl-c to terminate): ', end='')
    inp = input().strip()
    print_line_break()
    return inp


def starship_str(s, indent_level=1):
    return('\t' * indent_level + ' - Model: {}\n'.format(s.model)
          + '\t' * indent_level + '   Class: {}\n'.format(s.s_class)
          + '\t' * indent_level + '   Hyperdrive Rating: {}\n'.format(s.hdrive_rating)
          + '\t' * indent_level + '   Cost: {}\n'.format('{} credit(s)'.format(s.cost) if s.cost != 'unknown' else 'unknown')
          + '\t' * indent_level + '   Manufacturer: {}\n'.format(s.manufacturer)) 


def vehicle_str(s, indent_level=1):
    return ('\t' * indent_level + ' - Name: {}\n'.format(s.name)
            + '\t' * indent_level + '   Model: {}\n'.format(s.model)
            + '\t' * indent_level + '   Cost: {}\n'.format('{} credit(s)'.format(s.cost) if s.cost != 'unknown' else 'unknown'))

def planet_str(pl, indent_level=1):
    return ('\t' * indent_level + 'Name: {}\n'.format(pl.name)
            + '\t' * indent_level + 'Population: {}\n'.format(pl.population)
            + '\t' * indent_level + 'Climate: {}'.format(pl.climate))

def person_str(p, starships, vehicles, homeworld):
  return ('Name: {}\n'.format(p.name)
            + 'Gender: {}\n'.format(p.gender)
            + 'Starships: {}\n'.format('\n' + '\n'.join([starship_str(s) for s in starships])
              if len(p.starships)>0 else '-')
            + 'Vehicles: {}\n'.format('\n' + '\n'.join([vehicle_str(v) for v in vehicles])
              if len(p.vehicles)>0 else '-')
            + 'Homeworld: \n{}'.format(planet_str(homeworld)))


def display_person(p, starships, vehicles, homeworld):
    print(person_str(p, starships, vehicles, homeworld))
    print_line_break()


def display_error():
    print('Apologies, Supreme Commander. There seems to be some problem with the connection.\nPlease try again later.')
    print_line_break()

def display_unknown():
    print('Apologies, Supreme Commander. There does not seem to be any rebel by that name.')
    print_line_break()