from collections import defaultdict as dd
import pickle
import re
import json


def save_state() -> None:
    import pickle as pkl
    pkl.dump(csv_processor.final_lines, open(
        'file_lines.pkl', 'wb'))
    print('file lines pickled')


class csv_processor:

    columns = dd(lambda: [])  # will hold all the values of columns and rows
    final_lines = []  # will hold correctly escaped lines

    def __init__(self, settings: dict) -> None:
        self.settings = settings
        self.escape_comma()
        save_state()

    def escape_comma(self) -> None:
        file = open(f"{settings['input']}", 'r', encoding='utf-8')
        lines = file.readlines()
        if settings['stop_at'] is not None:
            lines = lines[:settings['stop_at']]
        lines = [line.replace(r'''\"''', "'") for line in lines]

        # regexr.com/67ks0 for explanation
        escape_regex = re.compile(r',(?=(?:(?:[^"]*"){2})*[^"]*$)')

        [csv_processor.final_lines.append(escape_regex.split(line))
         for line in lines]

        self.prepare_output(csv_processor.final_lines)

    def prepare_output(self, rows: list) -> None:
        csv_processor.count = dd(lambda: [])

        for row in rows:
            csv_processor.columns[len(row)].append(rows.index(row) + 1)

        if self.settings['show_first_items']:
            if len(csv_processor.columns.keys()) > 1:
                for column, rows in csv_processor.columns.copy().items():
                    csv_processor.count[column].append(len(rows))
                    csv_processor.count[column].append(
                        csv_processor.final_lines[rows[0]])
            else:
                print(
                    f'CSV contains {[x for x in csv_processor.columns.keys()][0]} column(s) \n no variation')
        else:
            for column, rows in csv_processor.columns.copy().items():
                csv_processor.count[column].append(len(rows))

        if self.settings["output"] is not None:
            with open(f'{self.settings["output"]}', 'w', encoding='utf-8') as out:
                json.dump({'metadata': {'input': f'{settings["input"]}', "format": "columns:rows", "counts": {
                    "columnCount": [
                        "count",
                        [
                            "firstValues"
                        ]
                    ]
                }},
                    "columnWise": csv_processor.columns, "counts": csv_processor.count}, out)

# ================================================ SETTINGS ==============================================


settings = {
    'input': 'escape_test.csv',
    'output': 'escaping_test_result.json',
    'show_first_items': True,
    # performs slicing, like [0:stop_at] to get that many lines.
    'stop_at': None,
}

# =========================================================================================================

# obj = csv_processor(settings=settings)


class match_rows():
    # csv_processor(settings)

    def __init__(self, settings: dict) -> None:
        self.settings = settings
        self.modify_rows()

    def modify_rows(self) -> None:
        # index of this list is line number in file
        lines = list(pickle.load(open('file_lines.pkl', 'rb')))
        actual_col = len(lines[0])

        if settings['output'] != '':
            json_output = json.load(open(settings['output'], 'r'))

        else:
            raise(FileNotFoundError)

        broken_rows = list(json_output['columnWise']['2'])

        print(lines)

        broken_rows.insert(0, broken_rows[0]-1)

        try:
            for index in range(len(broken_rows)):
                lines[broken_rows[index]].extend(lines[broken_rows[index+1]])
                del(lines[broken_rows[index+1]])
        except IndexError:
            print('index error silenced')
            print(lines)

        import pandas as pd

        df = pd.DataFrame(lines)
        print(df)


obj = match_rows(settings=settings)
