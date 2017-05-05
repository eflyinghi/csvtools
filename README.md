# csvtools

CLI tools useful to work with csv files. Below is the documentation for each tool.

### csvpp

usage: `csvpp [-h] [-s SEPARATOR] [-n LINES_NUMBER] [-f] [-o OUTPUT_FILE] [file]`

Print csv file in human-readable format.
Input is taken from STDIN by default.
The first line is header. It contains names of fields.

positional arguments:
  `file`
  > File to read input from. stdin is used by default

optional arguments:
  `-h, --help`
  > show help message and exit

  `-s SEPARATOR, --separator SEPARATOR`
  > Separator to be used

  `-n LINES_NUMBER, --lines_number LINES_NUMBER`
  >  Number of lines used to set column width

  `-f, --format_floats`
  > Format floating-point numbers nicely

  `-o OUTPUT_FILE, --output_file OUTPUT_FILE`
  > Output file. stdout is used by default

examples:
    `cat file.txt | csvpp -f | less -SR`


### csvcut

usage: `csvcut [-h] [-s SEPARATOR] [-o OUTPUT_FILE] [-f FIELDS] [-c] [-u] [file]`

  Select some columns from csv streem.
  Could change order of fields.

positional arguments:
  `file`
  > File to read input from. stdin is used by default

optional arguments:
  `-h, --help`
  > show help message and exit

  `-s SEPARATOR, --separator SEPARATOR`
  > Separator to be used

  `-f FIELDS, --fields FIELDS`
  >  Specify list of fields (comma separated) to cut. Field names or field numbers can be used.
    Dash can be used to specify fields ranges.
    Range 'F1-F2' stands for all fields between F1 and F2.
    Range '-F2' stands for all fields up to F2.
    Range 'F1-' stands for all fields from F1 til the end.


  `-c, --complement`
  >  Instead of leaving only specified columns, leave all except specified.

  `-u,--unique`
  >  Remove duplicates from list of FIELDS

  `-o OUTPUT_FILE, --output_file OUTPUT_FILE`
  > Output file. stdout is used by default

examples:
  `csvcut -f 1,2 stat.txt`
  `csvcut -f st,shows,clicks stat.txt`
  `cat stat.txt | csvcut -f shows,uniq,clicks`
  `cat stat.txt | csvcut -f select_type-clicks`   all fields from `select_type` to `clicks`
  `cat stats.txt | csvcut -f -shows stat.txt`     all fields from the first till `shows`
  `csvcut -f page_id-`                            all fields from `page_id` till the end
  `csvcut -f description --complement`            all fields except for `description`


### csvhead

usage: `csvhead [-h] [-o OUTPUT_FILE] [-n ROWS_COUNT] [file]`

Print header and first lines of input.

positional arguments:
  `file`
  > File to read input from. stdin is used by default

optional arguments:
  `-h, --help`
  > show help message and exit

  `-n ROWS_COUNT, --number_of_lines ROWS_COUNT`
  > Number of first rows to print

  `-o OUTPUT_FILE, --output_file OUTPUT_FILE`
  > Output file. stdout is used by default

examples:
  `cat file.csv | csvhead -n 100`  prints first 100 rows of file.csv


### csvtail

usage: `csvtail [-h] [-o OUTPUT_FILE] [-n ROWS_COUNT] [file]`

Print header and last lines of input.

positional arguments:
  `file`
  > File to read input from. stdin is used by default

optional arguments:
  `-h, --help`
  > show help message and exit

  `-n ROWS_COUNT, --number_of_lines ROWS_COUNT`
  > Number of last rows to print if positive `ROWS_COUNT`. Else skips `ROWS_COUNT` lines and prints till the end of
input.

  `-o OUTPUT_FILE, --output_file OUTPUT_FILE`
  > Output file. stdout is used by default

examples:
  `cat file.csv | csvtail -n -100`  skip first 100 rows and print file.csv till the end.


### csvmap

usage: `csvmap [-h] [-s SEPARATOR] [-o OUTPUT_FILE] [-e EXEC] [expression] [file]`

Transform each row of a csv file with an expression provided.

positional arguments:
  `expression`
  > Python expression to be used to transform a row. Specific columns can be refered as a fields of row object named `r`

  `file`
  > File to read input from. stdin is used by default

optional arguments:
  `-h, --help`
  > show help message and exit

  `-s SEPARATOR, --separator SEPARATOR`
  > Separator to be used

  `-o OUTPUT_FILE, --output_file OUTPUT_FILE`
  > Output file. stdout is used by default

  `-e EXEC, --exec EXEC`
  > Execute python code before starting the transformation. Might be useful for import statements or even for python
functions definition.

examples:
  `cat file.csv | csvmap 'r.ratio = r.a / r.b, r.b *= 1000'` assuming that file.csv contain columns `a` and `b`,
introduces a new column `ratio` containing the `a / b`. Also multiplies column `b` by `1000`.

  `cat file.csv | csvmap 'r.root_a = sqrt(r.a)' --exec 'from numpy import sqrt'` assuming that file.csv contains column
`a`, introduces a new column `root_a` containing `sqrt(a)`. Prior to running the row transformation, imports sqrt
function from numpy.

### csvreduce

usage: `csvreduce [-h] [-s SEPARATOR] [-o OUTPUT_FILE] [-k KEYS] [-i INTEGRATION_STEP] [-a AGGREGATORS] [--no-sort] [file]`

Reduces csv file using the KEYS provided. Reducing is a process of aggregating rows with the same keys by applying
AGGREGATORS to them. In other words, the rows will be grouped by the KEYS duting the aggregation process.

positional arguments:
  `file`
  > File to read input from. stdin is used by default

optional arguments:
  `-h, --help`
  > show help message and exit

  `-s SEPARATOR, --separator SEPARATOR`
  > Separator to be used

  `-o OUTPUT_FILE, --output_file OUTPUT_FILE`
  > Output file. stdout is used by default

  `-k KEYS, --keys KEYS`
  > Comma-separated list of columns to be used as reduce keys. Column names or column numbers can be used here

  `-i INTEGRATION_STEP, --integration_step INTEGRATION_STEP`
  > Divide each aggregation group into smaller groups each containing `INTEGRATION_STEP` rows.

  `-a AGGREGATORS, --agregators AGGREGATORS`
  > Comma-separated list of value-aggregators. Each aggregator might be one of the following: `first`, `last`, `sum`,
`mean`, `min`, `max`, `std` (standard deviation), count. Each aggragator (except count) is a function expecting 2
arguments: column name or number and the resulting field name. The resulting field name has a default value of
`$AGGREGATOR_NAME_$FIRST_ARGUMENT'` (e.g. for `sum('a')` it will have a default value of `sum_a`). Please see the
examples for more details.

  `--no-sort`
  > If provided, the input will not be sorted prior to reduce operation. Be careful, that might lead to an incorrect
reduce result. If your input is already sorted by the KEYS, this option will significantly speed up the reduce.

examples:
    `cat table.txt | tabreduce -r sum('price', 'overall_price'),count` assuming that `table.txt` has a column named
`price`, the result will be a table containing just a single row with columns named `overall_price` and `count`.

    `cat flat_prices.csv | tabreduce -k type,district -r max('price'),min('price'),mean('price'),avg('square')` assuming
that `flat_prices.csv` has columns name `price` and `district`, the result will be a table containing the maximum,
minimum and average price and average square of a flat for each district and commercial type.

### csvsort

usage: `csvsort [-h] [-s SEPARATOR] [-o OUTPUT_FILE] [-k KEYS] [-m MAX_ROWS] [--descending] [--numeric] [file]`

  Sort the rows of csv stream ascending.

positional arguments:
  `file`
  > File to read input from. stdin is used by default

optional arguments:
  `-h, --help`
  > show help message and exit

  `-s SEPARATOR, --separator SEPARATOR`
  > Separator to be used

  `-k KEYS, --keys KEYS`
  >  Specify the list of keys (comma separated) to sort on. Field names or field numbers can be used.
    Dash can be used to specify fields ranges.
    Range 'F1-F2' stands for all fields between F1 and F2.
    Range '-F2' stands for all fields up to F2.
    Range 'F1-' stands for all fields from F1 til the end.

  `--descending`
  >  If provided, perform descending sort instead of ascending

  `--numeric`
  >  If provided, keys will be interpreted as numbers. Otherwise - as strings.

  `-m MAX_ROWS, --max-rows MAX_ROWS`
  >  Don't load to memory more than `MAX_ROWS` rows at a time. This option is crucial if you have to deal with huge
  csv files. Default value is 0 that meanse that this will sort file in memory.

  `-o OUTPUT_FILE, --output_file OUTPUT_FILE`
  > Output file. stdout is used by default

examples:
  `cat stat.csv | csvsort -k shows`

### csvplot

usage: `csvplot [-h] [-s SEPARATOR] [-o OUTPUT_FILE] [-x KEY] [-y KEYS] [--xlabel LABEL] [-ylabels LABELS] [file]`

  Plot the data based on csv file contents.

positional arguments:
  `file`
  > File to read input from. stdin is used by default

optional arguments:
  `-h, --help`
  > show help message and exit

  `-s SEPARATOR, --separator SEPARATOR`
  > Separator to be used

  `-x KEY`
  >  Specify the key to iterate over x-axes. If not provided, use row number instead.

  `--xlabel LABEL`
  >  Label to be used for X axis.

  `-y KEYS`
  >  Specify columns to be plotted. One line graph will be plotted per each column. The plots will have different
colors.

  `--ylabel LABELS`
  >  Labeles to be used for Y axis.

  `-o OUTPUT_FILE, --output_file OUTPUT_FILE`
  > Output file. stdout is used by default

examples:
  `cat stat.csv | csvsort -k shows`
