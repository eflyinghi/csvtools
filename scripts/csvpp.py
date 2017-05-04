from argparse import ArgumentParser
import sys


DESCRIPTION = 'csvpp - prints cvs file in human-readable format'
EXAMPLES = 'example: cat file.txt | csvpp -f | less -SR'


def print_row(row, column_widths, output_stream):
    output_line = '|'
    for i, column in enumerate(row):
        output_line += ' ' + column + ' ' * (column_widths[i] - len(column) + 1) + '|'
    output_line += '\n'
    output_stream.write(output_line)


def main():
    args = parse_args()
    input_stream = open(args.file, 'r') if args.file else sys.stdin
    output_stream = open(args.output_file, 'r') if args.output_file else sys.stdout

    columns = input_stream.readline().strip().split(args.separator)
    first_rows = [columns]
    for i in range(args.lines_number):
        first_rows.append(input_stream.readline().strip().split(args.separator))
    column_widths = [max([len(column) for column in [row[i] for row in first_rows]]) for i in range(len(columns))]

    for row in first_rows:
        print_row(row, column_widths, output_stream)
    for row in input_stream:
        print_row(row.strip().split(args.separator), column_widths, output_stream)

    if input_stream != sys.stdin:
        input_stream.close()
    if output_stream != sys.stdout:
        output_stream.close()


def parse_args():
    parser = ArgumentParser(description=DESCRIPTION, epilog=EXAMPLES)
    parser.add_argument('-s', '--separator', type=str, help='Separator to be used', default=',')
    parser.add_argument('-n', '--lines_number', type=int, help='Number of lines used to set column width', default=100)
    parser.add_argument('-f', '--format_floats', help='Format floating-point numbers nicely', action='store_true')
    parser.add_argument('-o', '--output_file', type=str, help='Output file. stdout is used by default')

    parser.add_argument('file', nargs='?', help='File to read input from. stdin is used by default')

    args = parser.parse_args()

    return args

main()
