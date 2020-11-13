# Author: Stanislav Yakush <st.yakush@yandex.ru>
""" LevelDB viewer """

import sys
import argparse
import plyvel
import colorful

from terminaltables import SingleTable

TABLE_HEADER = ["Key", "Value"]

MAX_VALUE_LEN = 60

def splitstring(data, maxlen):
    """ Split string by length """
    return "\n".join((data[i:maxlen + i] for i in range(0, len(data), maxlen)))

def show_database(path):
    """ Show database """
    try:
        db = plyvel.DB(path, create_if_missing=False, paranoid_checks=True)
    except plyvel.Error as ex:
        print("Can\'t open DB: {}".format(ex))
        return -1

    table_data = [TABLE_HEADER]

    for key, value in db:
        table_data.append([colorful.white(key), splitstring(repr(value), MAX_VALUE_LEN)])

    db.close()

    table = SingleTable(table_data)

    table.inner_row_border = True

    print(table.table)

    return 0

def main():
    """ Main """
    parser = argparse.ArgumentParser(description="LevelDB viewer")

    parser.add_argument("--path", type=str, help="Path to the database")
    args = parser.parse_args()

    if not args.path:
        parser.print_usage()
        return -1

    return show_database(args.path)

if __name__ == "__main__":
    sys.exit(main())
