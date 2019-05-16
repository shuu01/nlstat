import csv
import json
import logging


def get_handler(stat=None, filename='stat', out_type='stdout'):

    if not stat:
        logging.error('')
        return False

    handlers = {
        'stdout': out_to_stdout,
        'json': out_to_json,
        'csv': out_to_csv,
        'ods': out_to_ods,
        'pdf': out_to_pdf,
    }

    handler = handlers.get(out_type)

    if handler:
        return handler(stat)
    else:
        logging.error(
            f"handler {out_type} doesn't supported"
        )
        return False


def out_to_json(stat, filename):

    stat = json.dumps(stat, sort_keys=True, indent=4)

    try:
        with open(filename, 'w') as json_file:
            json_file.write(stat)
            return True
    except Exception as e:
        logging.error(e)


def out_to_csv(stat, filename):
    try:
        with open(filename, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([stat['word_type'], 'occurence'])
            for word, occurence in statistic['words_top']:
                statistic_writer.writerow([word, occurence])
    except IOError as e:
        logging.error('words_code_stat.csv I/O error({0}): {1}'.format(
            e.errno, e.strerror
        ))


def output_to_stdout(statistic):

    print('statistic type: {0}'.format(statistic['parse_code_type']))
    print_statistics_words_top(statistic['words_top'],
                               words_type=statistic['word_type'])


def output_to_pdf(statistic):
    pass
