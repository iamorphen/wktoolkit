#!/usr/bin/python3 -B

import argparse
import keyring
import sys

from session.session import Session

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
  parser = argparse.ArgumentParser()
  parser.add_argument('user', help='the WaniKani username to transact as')
  parser.add_argument('--token', help='store/use this token for transactions')
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

  if session:
    print(session)


if __name__ == "__main__":
  main()
