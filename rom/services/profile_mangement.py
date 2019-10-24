# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rom.models import Profile
from rom.form_profile import ProfileForm


class ProfileManagement(object):
    def __init__(self, user):
        self.user = user
        try:
            self.profile = self.user.profile
        except Profile.DoesNotExist:
            self.profile = Profile(member=self.user)
            self.profile.save()

    def update(self, form_json):
        line_contact = form_json['line_contact']
        self.profile.line_contact = line_contact
        self.profile.save()

    def get(self):
        profile = dict()
        profile['line_contact'] = self.profile.line_contact
        return profile

    def get_form(self):
        return self.__generate_form()

    def __generate_form(self):
        initial = dict()
        initial['line_contact'] = self.profile.line_contact
        form = ProfileForm(initial=initial)
        return form
