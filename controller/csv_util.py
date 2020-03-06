def csv_reader(filepath): 
    """
    Simple reader for CSV files

    Inputs:
    -----
    filepath: str
        filepath of CSV file
    """
    with open(filepath) as f: 
        for row in f: 
            row = row.strip()
            r = list()
            part = '' 
            is_double_quoted = False

            for c in row: 
                if c == ',': 
                    if is_double_quoted is False:
                        r.append(part)
                        part = ''
                    else: 
                        part += c
                elif c == '\"': 
                    is_double_quoted = not is_double_quoted
                else: 
                    part += c
            if part != '': 
                r.append(part)

            yield r

def csv_writer(filepath, seqs):
    """
    Simple  writer for CSV files

    Inputs: 
    -----
    filepath: str
        filepath of CSV file
    seqs: generator producing lists of strings
        each row in list should represent a row in the CSV file
    """
    with open(filepath, 'w') as f:
        f.write('\n'.join([','.join(
                            ['"{}"'.format(r) 
                                if (' ' in r) or (',' in r) else r
                                for r in s])
                    for s in seqs]))


if __name__ == "__main__": 
    import sys

    rows = list()
    for r in csv_reader(sys.argv[1]): 
        rows.append(r)

    csv_writer('copy.csv', rows)