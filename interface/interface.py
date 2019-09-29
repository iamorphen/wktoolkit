"""
An interface to and abstraction over the WaniKani V2 API.
"""

import requests
from datetime import datetime
from urllib.parse import urljoin

from interface.level import Level

# Used to parse dates such as: 2019-09-24T01:58:43.171547Z
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

def wk_time(time):
  """
  Convert from the WaniKani time representation in the V2 API to a datetime.

  @p time A timestamp string as presented in a WaniKani V2 API result.
  @return A datetime equivalent or None if time is None.
  """
  return datetime.strptime(time, TIME_FORMAT) if time else None

class Interface():
  def __init__(self, session, base_url):
    """
    @p session A Session instance. This instance is assumed to be valid.
    @p base_url The base URL to the WaniKani V2 API.
    """
    self._session = session
    self._headers = {'Authorization': 'Bearer {}'.format(session.token())}
    self._base_url = base_url

  def get_current_level(self):
    """
    @return A Level representing the user's current level or None on error.
    """
    data = self._get('level_progressions')
    if not data:
      return None

    data = data['data'][-1]
    return Level(int(data['data']['level']),
                 int(data['id']),
                 wk_time(data['data']['unlocked_at']),
                 wk_time(data['data']['started_at']),
                 wk_time(data['data']['passed_at']),
                 wk_time(data['data']['abandoned_at']))

  def _get(self, resource, params=None, hdrs=None):
    """
    @p resource (str) The REST resource to GET, appended to the base URL.
    @p params (dict of str) Parameterss to add to the request.
    @p hdrs (dict of str) Headers to add to the request. Authorization is added
      by default.
    @return A requests.Response.json() object or None on error.
    """
    url = urljoin(self._base_url, resource)
    headers = {**(self._headers), **hdrs} if hdrs else self._headers
    data = requests.get(url, params=params, headers=headers)

    if not data.ok:
      print('Request for resource {} failed; reason: {}'.format(resource,
        data.reason))
      return None

    return data.json()
