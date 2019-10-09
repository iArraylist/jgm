# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rom.models import CharacterBase, CharacterJob, Job


class CharacterManagement(object):
    def __init__(self, user):
        self.user = user
