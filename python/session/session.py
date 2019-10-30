"""
A WaniKani session holds information about a particular user. This class also
holds information such as the user's private API key, required in REST
transactions. This session is designed for the V2 API.
"""

import requests
from urllib.parse import urljoin

from session.user import User

BASE_URL = 'https://api.wanikani.com/v2/'

class Session:
  def __init__(self, token, verbose=False):
    """
    Create a user session. This session uses the @p token to fetch user
    information via a REST transaction. If we can't determine user information
    based on the token, our self.user member will be None.

    @p token A secret API token to use for this session.
    @p verbose If True, enable verbose logging.
    """
    self._token = token
    self._verbose = verbose
    self.user = None

    self._fetch_user()

  def token(self):
    return self._token

  def _fetch_user(self):
    # TODO(orphen) Add explicit versioning when the V2 API graduates from beta.
    # https://docs.api.wanikani.com/20170710/?shell#revisions-aka-versioning
    headers = {'Authorization': 'Bearer {}'.format(self._token)}
    user_data = requests.get(urljoin(BASE_URL, 'user'), headers=headers)

    if user_data.ok:
      json = user_data.json()
      self.user = User(
        name=json['data']['username'],
        active=bool(json['data']['subscription']['active']),
        level=int(json['data']['level']),
        max_level=int(json['data']['subscription']['max_level_granted']))
    else:
      if self._verbose:
        print('Error fetching user data; reason: {}'.format(user_data.reason))
      self.user = None

  def __bool__(self):
    return self.user is not None

  def __str__(self):
    return 'User: {}; Subscription active: {}; Level {}/{}'.format(
      self.user.name, self.user.active, self.user.level, self.user.max_level)


