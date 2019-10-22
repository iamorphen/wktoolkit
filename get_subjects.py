#!/usr/bin/python3 -B

import argparse
import json
import sys
from itertools import chain

from identity import identity
from interface.interface import Interface
from interface.subjects import Radical, Kanji, Vocabulary
from session.session import Session, BASE_URL


def handle_args():
  """
  @return the object returned by argparse.ArgumentParser.parse_args().
  """
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
  group = parser.add_mutually_exclusive_group()
  group.add_argument('--original_json', help=('print original subject JSON to '
                     'stdout'), action='store_true')
  group.add_argument('--anki', help=('print a tab-separated list of fields '
                     'per subject per line'), action='store_true')
  group.add_argument('--anki_schema', help='print the Anki schema',
                     action='store_true')
  parser.add_argument('user', help='the WaniKani username to transact as')
  return parser.parse_args()


def main():
  args = handle_args()

  if args.anki_schema:
    print('Radicals: {}\nKanji: {}\nVocabulary: {}'.format(
      Radical.anki_schema(), Kanji.anki_schema(), Vocabulary.anki_schema()))
    sys.exit(0)

  token = identity.handle_identity(args.user, args.token)
  session = Session(token)
  if not session:
    sys.exit(1)

  interface = Interface(session, BASE_URL)
  subjects = interface.get_subjects(args.radical, args.kanji, args.vocabulary,
                                    args.level, args.original_json)

  if args.original_json:
    # NOTE(orphen) This could be optimized if creating the single massive JSON
    # object can be avoided.
    jlob = list()
    for item in chain(subjects.radicals, subjects.kanji, subjects.vocabulary):
      jlob.append(item.original_json)
    for chunk in json.JSONEncoder().iterencode(jlob):
      print(chunk)
  elif args.anki:
    for item in chain(subjects.radicals, subjects.kanji, subjects.vocabulary):
      print(item.to_anki())
  else:
    for item in chain(subjects.radicals, subjects.kanji, subjects.vocabulary):
      print(item)


if __name__ == "__main__":
  main()
