# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms


class GuildCreateForm(forms.Form):
    character = forms.CharField(label='Character', max_length=255, required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}))
    name = forms.CharField(label='Guild Name', max_length=255, required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    discord_link = forms.CharField(label='Discord', max_length=255, required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
