#!/usr/bin/python3 -B

import argparse
import sys

from identity import identity
from interface.interface import Interface
from session.session import Session, BASE_URL


def main():
  parser = argparse.ArgumentParser(description=(
    'Fetch WaniKani subjects. Specify no subject type to fetch all types.'))
  parser.add_argument('--token', help='store/use this token for transactions')
  parser.add_argument('--radical', help='fetch radicals', action='store_true')
  parser.add_argument('--kanji', help='fetch kanji', action='store_true')
  parser.add_argument('--vocabulary', help='fetch vocabulary',
                      action='store_true')
  parser.add_argument('--level', help=('fetch subjects for this level [1-60]; '
                      'leave unspecified to fetch subjects for all levels'),
                      type=int, default=0)
  parser.add_argument('user', help='the WaniKani username to transact as')
  args = parser.parse_args()

  token = identity.handle_identity(args.user, args.token)

  session = Session(token)
  if not session:
    sys.exit(1)

  interface = Interface(session, BASE_URL)
  subjects = interface.get_subjects(args.radical, args.kanji, args.vocabulary,
                                    args.level)
  for item in subjects.vocabulary:
    print(item)

if __name__ == "__main__":
  main()
