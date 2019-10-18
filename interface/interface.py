"""
An interface to and abstraction over the WaniKani V2 API.
"""

import requests
from urllib.parse import urljoin

from interface.level import Level
from interface.subjects import Subjects, Radical, Kanji, Vocabulary
from interface.time import wk_to_datetime


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
                 wk_to_datetime(data['data']['unlocked_at']),
                 wk_to_datetime(data['data']['started_at']),
                 wk_to_datetime(data['data']['passed_at']),
                 wk_to_datetime(data['data']['abandoned_at']))

  def get_subjects(self, radicals=True, kanji=True,
                   vocabulary=True, level=0):
    """
    Fetch subjects from WaniKani. By default, all subject types are fetched for
    all levels.

    @p radicals (bool) Indicates whether radicals should be fetched.
    @p kanji (bool) Indicates whether kanji should be fetched.
    @p vocabulary (bool) Indicates whether vocabulary should be fetched.
    @p level (int) [0-60] Inidcates which level to fetch subjects for.
      0 is the default and results in querying for subjects of all levels.
    @return An instance of subjects.Subjects.
    """
    params = {}

    params['types'] = []
    if radicals:
      params['types'].append('radical')
    if kanji:
      params['types'].append('kanji')
    if vocabulary:
      params['types'].append('vocabulary')

    if level > 0:
      if level > 60:
        params['levels'] = '60'
      else:
        params['levels'] = str(level)
    else:
      raise NotImplementedError(
        'Fetching subjects for all levels is currently not supported.')

    subjects = Subjects([], [], [])
    data = self._get('subjects', params=params)

    if data:
      data = data['data']

      for item in data:
        if item['object'] == 'radical':
          subjects.radicals.append(Radical(item))
        if item['object'] == 'kanji':
          subjects.kanji.append(Kanji(item))
        if item['object'] == 'vocabulary':
          subjects.vocabulary.append(Vocabulary(item))

    return subjects

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
