"""
A representation of a user level built from data from the WaniKani V2 API.
"""

from collections import namedtuple


class Level:
  def __init__(self, level, wk_id, unlocked, started, passed, abandoned):
    """
    @p level (int)
    @p wk_id (int) The WaniKani API ID for this level; ex: 49392.
    @p unlocked (datetime) The time this level was unlocked.
    @p started (datetime) The time this level's content was first studied.
    @p passed (datetime) The time this level was passed.
    @p abandoned (datetime) The time this level was abandoned; never == None.
    """
    self.level = level
    self.id = wk_id
    self.unlocked = unlocked
    self.started = started
    self.passed = passed
    self.abandoned = abandoned

  def __str__(self):
    return ('Level: {}; ID: {}; unlocked: {}; started: {}; passed: {}; '
            'abandoned: {}').format(self.level, self.id, self.unlocked,
            self.started, self.passed, self.abandoned)
