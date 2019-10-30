"""
This module provides time conversion utilities for working with timestamps from
WaniKani.
"""

from datetime import datetime

# Used to parse dates such as: 2019-09-24T01:58:43.171547Z
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

def wk_to_datetime(time):
  """
  Convert from the WaniKani time representation in the V2 API to a datetime.

  @p time A timestamp string as presented in a WaniKani V2 API result.
  @return A datetime equivalent or None if time is None.
  """
  return datetime.strptime(time, TIME_FORMAT) if time else None

