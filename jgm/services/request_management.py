# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class RequestManagement(object):
    def __init__(self, request):
        self.request = request

    def is_authenticated(self):
        return self.request.user.is_authenticated()

    def is_anonymous(self):
        return self.request.user.is_anonymous()

    def is_method_post(self):
        if self.request.method == 'POST':
            return True
        return False

    def is_method_get(self):
        if self.request.method == 'GET':
            return True
        return False

    def get_user(self):
        return self.request.user
