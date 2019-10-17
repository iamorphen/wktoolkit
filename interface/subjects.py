"""
This module provides classes and collections for working with subjects. A
subject is the name WaniKani gives to its items: radicals, kanji, and
vocabulary.
"""

from collections import namedtuple

# radicals, kanji, and vocabulary shall be lists of the following classes.
Subjects = namedtuple('Subjects', ['radicals', 'kanji', 'vocabulary'])

class Radical:
  def __init__(self):
    pass


class Kanji:
  def __init__(self):
    pass


class Vocabulary:
  def __init__(self, item):
    """
    @p item A dictionary derived from a JSON vocabulary object retrieved
      through the WaniKani V2 API.
    """
    data = item['data']

    self.id = item['id']
    self.document_url = data['document_url']
    self.level = data['level']
    self.characters = data['characters']
    self.meanings = []  # TODO(orphen)
    self.aux_meanings = []  # TODO(orphen)
    self.readings = []  # TODO(orphen)
    self.parts_of_speech = []  # TODO(orphen)
    self.meaning_mneumonic = data['meaning_mnemonic']
    self.reading_mneumonic = data['reading_mnemonic']
    self.sentences = []  # TODO(orphen)

  def __str__(self):
    return ('Characters: {}; Level: {}; ID: {}'
           ).format(self.characters, self.level, self.id)
