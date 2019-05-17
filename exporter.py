import csv
import json


def export_to_json(stat, iowrapper):

    stat = json.dumps(stat, sort_keys=True, indent=4)
    iowrapper.write(stat)


def export_to_csv(stat, iowrapper):

    writer = csv.writer(iowrapper)
    for line in stat:
        writer.writerow(line)


def export_to_stdout(stat, iowrapper):

    for line in stat:
        iowrapper.write(str(line))
        iowrapper.write('\n')


def export_to_pdf(statistic):
    pass


def get_exporter(exporter):

    return exporters.get(exporter)


exporters = {
    'stdout': export_to_stdout,
    'json': export_to_json,
    'csv': export_to_csv,
    'pdf': export_to_pdf,
}
