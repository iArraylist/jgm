# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.conf import settings
from rom.models import Job


JOB_CHOICES = [[job.pk, job.name] for job in Job.objects.all().order_by('sort')]


class CharacterForm(forms.Form):
    ign = forms.CharField(label='In Game Name', max_length=255, required=True, error_messages={'required': 'Please let us know your name!'},
                          widget=forms.TextInput(attrs={'class': 'form-control'}))
    base_level = forms.IntegerField(label='Base Level', min_value=1, max_value=settings.CHARACTER_MAX_LEVEL, initial=1, required=True,
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))
    contribution = forms.IntegerField(label='Contribution', min_value=0, initial=0, required=True,
                                      widget=forms.NumberInput(attrs={'class': 'form-control'}))
    gold_medal = forms.IntegerField(label='Gold Medal', min_value=0, initial=0, required=True,
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))
    jobs = forms.MultipleChoiceField(label='Jobs', required=True, error_messages={'required': 'Please let us know your job!'},
                                     widget=forms.CheckboxSelectMultiple, choices=JOB_CHOICES)


class CharacterWGForm(CharacterForm):
    woe_job = forms.IntegerField(label='WOE', required=True, error_messages={'invalid': 'Please let us know your WOE job!'},
                                 widget=forms.Select())
    woc_job = forms.IntegerField(label='WOC', required=True, error_messages={'invalid': 'Please let us know your WOC job!'},
                                 widget=forms.Select())
    zone_job = forms.IntegerField(label='ZONE', required=True, error_messages={'invalid': 'Please let us know your ZONE job!'},
                                  widget=forms.Select())
