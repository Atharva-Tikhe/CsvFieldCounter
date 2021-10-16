import csv
from collections import defaultdict as dd
import json
import time


class CsvFieldCounter:

    def __init__(self, input_file, output_file):
        '''This class gives out the various numbers of columns
        and their rows in a csv file
        :param input_file: input csv file to read.
        :param output_file: output json with column and row data.
        ...
        Two ways of using this class:
        :param output_file given: writes output to the file directly.
        :param output_file not given: user has to explicitly call count() on the object.
        '''

        # path attribute for the object
        # print for batch operations
        self.path = input_file

        csv_reader = csv.reader(open(f"{self.path}", "r", encoding="utf8"))

        # csv_reader  is not iterable and won't access the row data
        #         create a list - iterable and easy indexing
        self.lines = list(csv_reader)

        # default dictionary with default value set to []
        self.columns = dd(lambda: [])

        # if the output file path is given, call write_to_file()
        if len(output_file) != 0:
            self.output_file = output_file
            self.write_to_file()

    def count(self) -> dict:
        '''
            Initiate an empty dictionary with default to a list.
            various length of rows (columns) are keys and rows with respective columns
            are appended to the list.
            columns[number of columns ] = [list of rows with that number of columns]
        '''
        count = {}

        for row in self.lines:
            # index + 1 to give actual row number starting from 1
            self.columns[len(row)].append(self.lines.index(row) + 1)

        # give a count of rows with that specific number of columns
        for key, value in self.columns.items():
            count[key] = len(value)

        return count

    def write_to_file(self):
        ''' Initiate an empty dictionary with default to a list.
            various length of rows (columns) are keys and rows with respective columns
            are appended to the list.
            columns[number of columns ] = [list of rows with that number of columns]
            this method is automatically called if output file is mentioned.
            :param self: only passed to use object attributes.
        '''

        l_column = self.columns
        l_count = {}

        with open(f"{self.output_file}", "w") as op:
            for row in self.lines:
                # index + 1 to give actual row number starting from 1
                l_column[len(row)].append(self.lines.index(row) + 1)

            for key, value in self.columns.items():
                l_count[key] = len(value)

            if len(l_count) == 1:
                print(
                    f'CSV contains {[x for x in l_count.keys()][0]} column(s) \n no variation')

                if input('still write json? [y/n]') == 'y':
                    json.dump({'metadata': {'input': f'{self.path}', "format": "columns:rows"},
                               "columnWise": l_column, "counts": l_count}, op)
                else:
                    return
            else:
                json.dump({'metadata': {'input': f'{self.path}', "format": "columns:rows"},
                           "columnWise": l_column, "counts": l_count}, op)

        op.close()

        print(f'output written to {self.output_file}')


# ---------------------------IMPLEMENTATION-----------------------------------

input_filename = r"E:\Atharva\Evolvus\CSV_validator\data_profiling\check_app.csv"
output_json = r"escape_test_result.json"


t0 = time.time()
obj = CsvFieldCounter(input_filename, output_json)
