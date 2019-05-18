# python natural language statistics

Gather natural language statistics from python projects

## usage

    usage: nlstat.py [-h] [-p filepath [filepath ...]]
                 [-c limit files parsing to count] [-o output]
                 [-f {stdout,json,csv,pdf}] [-l {python}] [-g url [url ...]]
                 [-r {top-verbs,top-nouns,top-names-functions,top-names-variables,top-verbs-functions,top-verbs-variables}]
                 [-s top_size]

    Natural language statistics.

    optional arguments:
      -h, --help            show this help message and exit
      -p filepath [filepath ...], --path filepath [filepath ...]
                            one or more paths to project
      -c limit files parsing to count, --count limit files parsing to count
                            one or more paths to project
      -o output, --output output
                            redirect output to a file or stdout, default: stdout
      -f {stdout,json,csv,pdf}, --format {stdout,json,csv,pdf}
                            output data format, default: json
      -l {python}, --lang {python}
                            programming language, default: python
      -g url [url ...], --git-url url [url ...]
                            one or more urls to git project repository
      -r {top-verbs,top-nouns,top-names-functions,top-names-variables,top-verbs-functions,top-verbs-variables}, --report {top-verbs,top-nouns,top-names-functions,top-names-variables,top-verbs-functions,top-verbs-variables}
                            report type, default: top-verbs
      -s top_size, --top-size top_size
                            size of top reports, default: 10

## usage example

    ./nlstat.py -p . -o stat -f json -r top-names-functions -l python -c 10

This command get all python files in current working directory, collect statistics about top functions names, convert it to json format and put in file with name 'stat'