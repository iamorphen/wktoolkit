"""
This module provides classes and collections for working with subjects. A
subject is the name WaniKani gives to its items: radicals, kanji, and
vocabulary.
"""

from collections import namedtuple

# Radicals, kanji, and vocabulary shall be lists of the following classes.
Subjects = namedtuple('Subjects', ['radicals', 'kanji', 'vocabulary'])


class Subject:
  """
  A base class for WaniKani subjects.
  """

  # Use a tab to separate fields as it's far more likely WaniKani will use
  # commas or semicolons in their content than tabs.
  ANKI_SEPARATOR = '\t'

  def __init__(self, item, store_json):
    """
    @p item (dict) A dictionary of the JSON subject object retrieved through
      the WaniKani V2 API.
    @p store_json (bool) If true, store @p item in this instance.
    """
    # The definition of members is important. We take the order of definition
    # to be the order in which our members are written out in the Anki schema.

    data = item['data']

    self.original_json = item if store_json else None  # Schema-ignored.
    self.id = item['id']
    self.document_url = data['document_url']
    self.level = data['level']
    self.meanings = []
    self.aux_meanings = []
    self.meaning_mnemonic = data['meaning_mnemonic']

    for meaning in data['meanings']:
      self.meanings.append(meaning['meaning'])

    for aux_meaning in data['auxiliary_meanings']:
      self.aux_meanings.append(aux_meaning['meaning'])
    if len(self.aux_meanings) == 0:
      self.aux_meanings.append('None')

  def to_anki(self):
    """
    @return (str) a tab-separated list of our members.
    """
    # Some of our members are lists that will be joined by commas. Anki uses
    # the first (comma, semicolon, tab) it sees as the separator. Therefore,
    # the first member we add to the string should not itself contain any
    # character that can be confused as a separator.
    return str(self.ANKI_SEPARATOR.join((str(self.id), self.document_url,
                                         str(self.level),
                                         ', '.join(self.meanings),
                                         ', '.join(self.aux_meanings),
                                         self.meaning_mnemonic)))

  @staticmethod
  def anki_schema():
    """
    @return (str) Our members in order of appearance in to_anki().
    """
    return "id document_url level meanings aux_meanings meaning_mnemonic"


class Radical(Subject):
  def __init__(self, item, store_json):
    """
    @p item (dict) A dictionary of the JSON radical object retrieved through
      the WaniKani V2 API.
    @p store_json (bool) If true, store @p item in this instance.
    """
    # The definition of members is important. We take the order of definition
    # to be the order in which our members are written out in the Anki schema.

    super().__init__(item, store_json)
    self.characters = ''  # TODO(orphen) Store the radical's vector graphic.

  def to_anki(self):
    """
    @return (str) a tab-separated list of our members.
    """
    anki = super().to_anki()
    return self.ANKI_SEPARATOR.join((anki, 'characters_not_implemented'))

  @staticmethod
  def anki_schema():
    """
    @return (str) Our members in order of appearance in to_anki().
    """
    return ' '.join((Subject.anki_schema(), 'characters'))

  def __str__(self):
    return ('Radical; Meanings: {}; Level: {}; ID: {}'
           ).format(', '.join(self.meanings), self.level, self.id)


class Kanji(Subject):
  class Readings:
    def __init__(self):
      self.onyomi = list()
      self.kunyomi = list()
      self.nanori = list()

    def to_anki(self):
      onyomi = ', '.join(self.onyomi) if len(self.onyomi) else 'None'
      kunyomi = ', '.join(self.kunyomi) if len(self.kunyomi) else 'None'
      nanori = ', '.join(self.nanori) if len(self.nanori) else 'None'
      return Kanji.ANKI_SEPARATOR.join((onyomi, kunyomi, nanori))

    @staticmethod
    def anki_schema():
      return ' '.join(('onyomi', 'kunyomi', 'nanori'))

    def __str__(self):
      return 'O: {}; K: {}; N: {}'.format(', '.join(self.onyomi),
        ', '.join(self.kunyomi), ', '.join(self.nanori))


  def __init__(self, item, store_json):
    """
    @p item (dict) A dictionary of the JSON kanji object retrieved through
      the WaniKani V2 API.
    @p store_json (bool) If true, store @p item in this instance.
    """
    # The definition of members is important. We take the order of definition
    # to be the order in which our members are written out in the Anki schema.

    super().__init__(item, store_json)

    data = item['data']

    self.characters = data['characters']
    self.readings = self.Readings()
    self.reading_mnemonic = data['reading_mnemonic']

    for reading in data['readings']:
      if reading['type'] == 'onyomi':
        self.readings.onyomi.append(reading['reading'])
      if reading['type'] == 'kunyomi':
        self.readings.kunyomi.append(reading['reading'])
      if reading['type'] == 'nanori':
        self.readings.nanori.append(reading['reading'])


  def to_anki(self):
    """
    @return (str) a tab-separated list of our members.
    """
    anki = super().to_anki()
    return self.ANKI_SEPARATOR.join((anki, self.characters,
                                     self.readings.to_anki(),
                                     self.reading_mnemonic))

  @staticmethod
  def anki_schema():
    """
    @return (str) Our members in order of appearance in to_anki().
    """
    return ' '.join((Subject.anki_schema(), 'characters',
                     Kanji.Readings.anki_schema(), 'reading_mnemonic'))

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
    # The definition of members is important. We take the order of definition
    # to be the order in which our members are written out in the Anki schema.

    super().__init__(item, store_json)

    data = item['data']

    self.characters = data['characters']
    self.readings = list()
    self.parts_of_speech = list()
    self.reading_mnemonic = data['reading_mnemonic']
    self.sentences = list()

    for reading in data['readings']:
      self.readings.append(reading['reading'])

    for part in data['parts_of_speech']:
      self.parts_of_speech.append(part)

    for sentence in data['context_sentences']:
      self.sentences.append(self.Sentence(sentence['en'], sentence['ja']))

  def to_anki(self):
    """
    @return (str) a tab-separated list of our members.
    """
    anki = super().to_anki()
    # TODO(orphen)
    return anki

  @staticmethod
  def anki_schema():
    """
    @return (str) Our members in order of appearance in to_anki().
    """
    return ' '.join((Subject.anki_schema(), 'characters', 'readings',
                     'parts_of_speech', 'reading_mnemonic', 'sentences'))

  def __str__(self):
    return ('Vocabulary; Characters: {}; Meanings: {}; Readings: {}; '
            'Level: {}; ID: {}'
           ).format(self.characters, ', '.join(self.meanings),
                    ', '.join(self.readings), self.level, self.id)
