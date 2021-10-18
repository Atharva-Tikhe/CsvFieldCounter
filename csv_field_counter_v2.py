from collections import defaultdict as dd
import re
import json


class csv_processor:

    columns = dd(lambda: [])  # will hold all the values of columns and rows
    escaped = []  # will hold correctly escaped lines

    def __init__(self, settings: dict) -> None:
        self.settings = settings
        self.escape_comma()

    def escape_comma(self):
        file = open(f"{settings['input']}", 'r', encoding='utf-8')
        lines = file.readlines()
        if settings['stop_at'] is not None:
            lines = lines[:settings['stop_at']]
        lines = [line.replace(r'''\"''', "'") for line in lines]

        # regexr.com/67ks0 for explanation
        escape_comma = re.compile(r',(?=(?:(?:[^"]*"){2})*[^"]*$)')

        [csv_processor.escaped.append(escape_comma.split(line))
         for line in lines]

        self.prepare_output(csv_processor.escaped)

    def prepare_output(self, rows: list):
        count = dd(lambda: [])

        for row in rows:
            csv_processor.columns[len(row)].append(rows.index(row) + 1)

        if self.settings['show_first_items']:
            if len(csv_processor.columns.keys()) > 1:
                for column, rows in csv_processor.columns.copy().items():
                    count[column].append(len(rows))
                    count[column].append(csv_processor.escaped[rows[0]][:2])
            else:
                print(
                    f'CSV contains {[x for x in csv_processor.columns.keys()][0]} column(s) \n no variation')
        else:
            for column, rows in csv_processor.columns.copy().items():
                count[column].append(len(rows))

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
                    "columnWise": csv_processor.columns, "counts": count}, out)

# ================================================ SETTINGS ==============================================


settings = {
    'input': 'escape_test.csv',
    'output': 'escaping_test_result.json',
    'show_first_items': True,
    # performs slicing, like [0:stop_at] to get that many files.
    'stop_at': None,
}

# =========================================================================================================

obj = csv_processor(settings=settings)
