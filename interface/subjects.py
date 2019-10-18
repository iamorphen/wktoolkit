"""
This module provides classes and collections for working with subjects. A
subject is the name WaniKani gives to its items: radicals, kanji, and
vocabulary.
"""

from collections import namedtuple

# radicals, kanji, and vocabulary shall be lists of the following classes.
Subjects = namedtuple('Subjects', ['radicals', 'kanji', 'vocabulary'])


class Subject:
  def __init__(self, item, store_json):
    """
    A base class for subjects.

    @p item (dict) A dictionary of the JSON subject object retrieved through
      the WaniKani V2 API.
    @p store_json (bool) If true, store @p item in this instance.
    """
    self.json = item if store_json else None

    data = item['data']

    self.id = item['id']
    self.document_url = data['document_url']
    self.level = data['level']

    self.meanings = []
    for meaning in data['meanings']:
      self.meanings.append(meaning['meaning'])

    self.aux_meanings = []
    for aux_meaning in data['auxiliary_meanings']:
      self.aux_meanings.append(meaning['meaning'])

    self.meaning_mnemonic = data['meaning_mnemonic']


class Radical(Subject):
  def __init__(self, item, store_json):
    """
    @p item (dict) A dictionary of the JSON radical object retrieved through
      the WaniKani V2 API.
    @p store_json (bool) If true, store @p item in this instance.
    """
    super().__init__(item, store_json)

    self.characters = ''  # TODO(orphen) Store the radical's vector graphic.

  def __str__(self):
    return ('Radical; Meanings: {}; Level: {}; ID: {}'
           ).format(', '.join(self.meanings), self.level, self.id)


class Kanji(Subject):
  class Readings:
    def __init__(self):
      self.onyomi = list()
      self.kunyomi = list()
      self.nanori = list()

    def __str__(self):
      return 'O: {}; K: {}; N: {}'.format(', '.join(self.onyomi),
        ', '.join(self.kunyomi), ', '.join(self.nanori))


  def __init__(self, item, store_json):
    """
    @p item (dict) A dictionary of the JSON kanji object retrieved through
      the WaniKani V2 API.
    @p store_json (bool) If true, store @p item in this instance.
    """
    super().__init__(item, store_json)
    data = item['data']

    self.characters = data['characters']
    self.readings = self.Readings()
    for reading in data['readings']:
      if reading['type'] == 'onyomi':
        self.readings.onyomi.append(reading['reading'])
      if reading['type'] == 'kunyomi':
        self.readings.kunyomi.append(reading['reading'])
      if reading['type'] == 'nanori':
        self.readings.nanori.append(reading['reading'])

    self.reading_mnemonic = data['reading_mnemonic']

  def __str__(self):
    return ('Kanji; Character: {}; Meanings: {}; Readings: {}; Level: {}; '
            'ID: {}').format(self.characters, ', '.join(self.meanings),
                             str(self.readings), self.level, self.id)


class Vocabulary(Subject):
  Sentence = namedtuple('Sentence', ['en', 'ja'])


  def __init__(self, item, store_json):
    """
    @p item (dict) A dictionary of the JSON vocabulary object retrieved
      through the WaniKani V2 API.
    @p store_json (bool) If true, store @p item in this instance.
    """
    super().__init__(item, store_json)
    data = item['data']

    self.characters = data['characters']

    self.readings = list()
    for reading in data['readings']:
      self.readings.append(reading['reading'])

    self.parts_of_speech = list()
    for part in data['parts_of_speech']:
      self.parts_of_speech.append(part)

    self.reading_mnemonic = data['reading_mnemonic']

    self.sentences = list()
    for sentence in data['context_sentences']:
      self.sentences.append(self.Sentence(sentence['en'], sentence['ja']))

  def __str__(self):
    return ('Vocabulary; Characters: {}; Meanings: {}; Readings: {}; '
            'Level: {}; ID: {}'
           ).format(self.characters, ', '.join(self.meanings),
                    ', '.join(self.readings), self.level, self.id)
