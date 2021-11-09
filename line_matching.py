import re
import logging
import pandas as pd


class line_matching:

    settings: dict = {}

    def __init__(self, settings: dict) -> None:
        self.settings = settings
        self.file = open(f"{settings['input']}", 'r', encoding='utf-8')

        logging.basicConfig(filename='line_matching.log', format="%(asctime)s %(message)s",
                            datefmt="%m/%d/%Y %I:%M:%S, %p:", level=logging.INFO)

        logging.info('New run ' + '='*10)
        logging.info('Processing started')

        final_lines = self.escape_comma()
        self.correct_rows_and_match(final_lines)

        logging.info('Processing finished')

    def escape_comma(self) -> None:
        final_lines = []

        if self.settings['stop_at'] is not None:
            lines = self.file.readlines()[:settings['stop_at']]
        else:
            lines = self.file.readlines()

        lines = [line.replace(r'''\"''', "'") for line in lines]

        escape_regex = re.compile(r',(?=(?:(?:[^"]*"){2})*[^"]*$)')

        [final_lines.append(escape_regex.split(line))
            for line in lines]

        return final_lines

    def correct_rows_and_match(self, lines: list):
        df_untouched = pd.DataFrame(lines)

        actual_cols = len(lines[0])
        for line in lines:
            if len(line) < actual_cols:
                lines[lines.index(line)].append(
                    lines[lines.index(line)+1])
                '''
                    Use of extend was dropped as it was creating new element in the list (which gave wrong column numbers)
                    append will cause nesting but column number will be preserved.
                '''
                # lines[lines.index(line)].extend(lines[lines.index(line)+1])

                del(lines[lines.index(line)+1])
                if len(line) != actual_cols:
                    logging.warning(
                        f"Line doesn't have correct amount of rows: {line}")

        row_corrected_df = pd.DataFrame([row for row in lines])

        final_df = pd.DataFrame(
            columns=['linewise processing', 'autoload in pandas', 'match'])

        for index in row_corrected_df.index:
            if row_corrected_df.iloc[[index]].to_string(header=False, index=False) != df_untouched.iloc[[index]].to_string(header=False, index=False):

                final_df.at[f'{index}', 'linewise processing'] = row_corrected_df.iloc[[
                    index]].to_string(header=False, index=False)

                final_df.at[f'{index}', 'autoload in pandas'] = df_untouched.iloc[[
                    index]].to_string(header=False, index=False)
                final_df.at[f'{index}', 'match'] = False
                logging.warning(
                    f"rows don't match at index {index} : {df_untouched.iloc[[index]].to_string(header=False, index=False)}")
            else:
                continue
                final_df.at[f'{index}', 'linewise processing'] = row_corrected_df.iloc[[
                    index]].to_string(header=False, index=False)

                final_df.at[f'{index}', 'autoload in pandas'] = df_untouched.iloc[[
                    index]].to_string(header=False, index=False)
                final_df.at[f'{index}', 'match'] = False
            final_df.to_csv(
                f"{self.settings['output']}_comparison.csv", index_label='index')

        if self.settings['print_output'] == True:
            print(final_df)


settings = {
    'input': 'escape_test.csv',
    'output': 'escaping_test_result',
    'show_first_items': True,
    # performs slicing, like [0:stop_at] to get that many files.
    'stop_at': None,
    'print_both_df': False,
    'print_output': False
}

line_matching(settings)
