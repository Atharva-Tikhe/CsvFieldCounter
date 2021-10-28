import re

class line_matching:

    settings: dict = {}

    def __init__(self, settings: dict) -> None:
        self.settings = settings

        self.file = open(f"{settings['input']}", 'r', encoding='utf-8')
        final_lines = self.escape_comma()
        final_lines_modified = self.correct_rows(final_lines)
        self.compare_dfs(row_modified=final_lines_modified,
                         row_unmodified=final_lines)

    def escape_comma(self) -> None:
        final_lines = []
        lines = self.file.readlines()
        if self.settings['stop_at'] is not None:
            lines = lines[:settings['stop_at']]

        lines = [line.replace(r'''\"''', "'") for line in lines]

        escape_regex = re.compile(r',(?=(?:(?:[^"]*"){2})*[^"]*$)')

        [final_lines.append(escape_regex.split(line))
            for line in lines]

        print(len(final_lines))

        return final_lines

    def correct_rows(self, lines: list):
        actual_cols = len(lines[0])
        for line in lines:
            if len(line) < actual_cols:
                lines[lines.index(line)].extend(
                    lines[lines.index(line)+1])
                del(lines[lines.index(
                    line)+1])

        print(len(lines))
        print(lines)

        return lines

    def compare_dfs(self, row_modified: list, row_unmodified: list):
        import pandas as pd
        test_df = pd.DataFrame(row_modified)

        untouched_df = pd.DataFrame(row_unmodified)

        if self.settings['print_both_df']:
            print('Displaying line by line modified df:')
            print(test_df)
            print('='*(len(test_df[0])*10))

            print('Displaying df read by pandas:')
            print(untouched_df)

        df_all = test_df.merge(untouched_df.drop_duplicates(), on=[0],
                               how='left', indicator=True)  # test_df is left, untouched_df is right

        df_all.to_csv(f"{settings['output'].split('.')[0]}_comparison.csv")
        print('comparison csv generated')


settings = {
    'input': 'escape_test.csv',
    'output': 'escaping_test_result',
    'show_first_items': True,
    # performs slicing, like [0:stop_at] to get that many files.
    'stop_at': None,
    'print_both_df': True
}

# escape_comma(settings=settings)
line_matching(settings)