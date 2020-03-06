from controller.csv_util import * 

import os


TEST_FILEPATH = './tmp.csv'


def clear_test_file():
    os.remove(TEST_FILEPATH)


def test_csv_reader():
    with open(TEST_FILEPATH, 'w') as f:
        f.write('1,"1,2,3",4\n'
                '2,"2 3 4",5')

    assert list(csv_reader(TEST_FILEPATH)) \
        == [['1', '1,2,3', '4'], ['2', '2 3 4', '5']]

def test_csv_writer():
    seqs = [["I", "Like to eat", "pizza, nuggets, and cake"],
            ["but", "not", "vegetables"]]
    csv_writer(TEST_FILEPATH, seqs)

    with open(TEST_FILEPATH) as f:
        assert f.read() == 'I,"Like to eat","pizza, nuggets, and cake"\n'\
                           'but,not,vegetables'