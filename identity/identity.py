"""
This module handles interactions with the keyring and is used to store or
retrieve a user API key based on a username.
"""

import keyring

WKTOOLKIT_KEYRING_SERVICE = 'wktoolkit'

def get_api_key(user):
  """
  @p user (str) The user for whom we fetch the token.
  @return An API key if one exists for the user; otherwise, None.
  """
  key = keyring.get_password(WKTOOLKIT_KEYRING_SERVICE, user)
  return None if not key else key


def store_api_key(user, key):
  """
  Update the @p key stored for the @p user.

  @p user (str) The WaniKani/keyring user to update.
  @p key (str) The key to store for @p user.
  """
  keyring.set_password(WKTOOLKIT_KEYRING_SERVICE, user, key)


def handle_identity(user, key):
  """
  This function is higher-level than get_api_key or store_api_key and will call
  one of those two functions depending on the arguments passed here.

  @p user (str) The WaniKani/keyring user.
  @p key (str) The V2 API key associated with the @p user. If None, the key will
    be fetched from the keyring. If specified, the @p key will be stored in the
    keyring.
  @return The API key corresponding to @p user.
  """
  real_key = None
  if not key:
    real_key = get_api_key(user)
    if not real_key:
      print(('User {} has no corresponding token. A token must be manually '
             'specified for this user.').format(user))
      sys.exit(1)
  else:
    store_api_key(user, key)
    real_key = key

  return real_key
