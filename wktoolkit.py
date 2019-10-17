#!/usr/bin/python3 -B

import argparse
import keyring
import sys

from interface.interface import Interface
from session.session import Session, BASE_URL

WKTOOLKIT_KEYRING_SERVICE = 'wktoolkit'

def get_token(user):
  """
  @p user The user for whom we fetch the token.
  @return A token if one exists for the user; otherwise, None.
  """
  token = keyring.get_password(WKTOOLKIT_KEYRING_SERVICE, user)
  return None if not token else token


def store_token(user, token):
  """
  Update the @p token stored for the @p user.

  @p user The WaniKani/keyring user to update.
  @p token The token to store for @p user.
  """
  keyring.set_password(WKTOOLKIT_KEYRING_SERVICE, user, token)


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

  token = None
  if not args.token:
    token = get_token(args.user)
    if not token:
      print(('User {} has no corresponding token. Invoke this script with '
             '--token to specify and store a token for this user.').format(
             args.user))
      sys.exit(1)
  else:
    store_token(args.user, args.token)
    token = args.token

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
