"""
A simple representation of a WaniKani user.
"""

from collections import namedtuple

User = namedtuple('User', ['name',        # The username (str).
                           'active',      # (bool)
                           'level',       # The user's current level (int).
                           'max_level'])  # The user's maximum allowed level (int).
