import io
import unittest

from csvtools.csvtools.csvpp import print_row


class TestPrintRow(unittest.TestCase):
    def setUp(self):
        self.stream = io.StringIO()

    def test_simple_print(self):
        print_row(
            row=['a', 'b', 'c'],
            column_widths=[5, 3, 6],
            output_stream=self.stream,
            careful=True,
            quiet=False
        )
        print_row(
            row=['aaa', 'bbbbbbbb', ''],
            column_widths=[5, 3, 6],
            output_stream=self.stream,
            careful=True,
            quiet=False
        )
        first_row, second_row, _ = self.stream.getvalue().split('\n')
        self.assertEquals(first_row, '| a     | b   | c      |')
        self.assertEquals(second_row, '| aaa   | bbbbbbbb |        |')
