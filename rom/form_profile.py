# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms


class ProfileForm(forms.Form):
    line_contact = forms.CharField(label='Line', max_length=255, required=True,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
