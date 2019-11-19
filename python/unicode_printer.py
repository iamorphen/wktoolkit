#!/usr/bin/python3 -B
"""
Prints characters in Unicode ranges. By default, prints kanji from CJK ranges.
"""

import argparse
from collections import namedtuple

CodeRange = namedtuple('CodeRange', ['begin', 'end', 'name'])

DefaultRanges = [CodeRange(0x3400, 0x4db5, 'CJK unified ideographs Extension A - Rare Kanji'),
                 CodeRange(0x4e00, 0x9faf, 'CJK unified ideographs - Common and Uncommon Kanji')]

def prepare_ranges(ranges):
    """
    Builds a list of CodeRange instances from ranges specified on the command line.
    @p ranges (list of strings) Code ranges formatted as 'begin_hex;end_hex;name'.
    """
    if not ranges:
        return DefaultRanges

    code_ranges = list()
    for code_range in ranges:
        pieces = code_range.split(';')
        code_ranges.append(CodeRange(int(pieces[0], base=16), int(pieces[1], base=16), pieces[2]))

    return code_ranges

def print_ranges(glyphs_per_line, verbose, ranges):
    """
    @p glyphs_per_line (int)
    @p verbose         (bool) If True, print range titles and line-leading glyph codes.
    @p ranges          (list of CodeRange instances)
    """
    for code_range in ranges:
        if verbose:
            print('{} ({} - {})'.format(code_range.name, hex(code_range.begin), hex(code_range.end)))

        code = code_range.begin
        count = 0
        while code <= code_range.end:
            if not count % glyphs_per_line and verbose:
                print('{} '.format(hex(code)), end='')

            print(chr(code), end='')
            count += 1

            if count % glyphs_per_line:
                print(' ', end='')
            elif code != code_range.end:
                print()

            code += 1

        print()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--glyphs_per_line', help='The number of glyphs per printed line',
                        type=int, default=16)
    parser.add_argument('--verbose', help='Print code range titles and line-leading codes',
                        action='store_true')
    parser.add_argument('--range', help='Specify a range as "hex_begin;hex_end;name"',
                        action='append')
    args = parser.parse_args()

    print_ranges(args.glyphs_per_line, args.verbose, prepare_ranges(args.range))


if __name__ == '__main__':
    main()
