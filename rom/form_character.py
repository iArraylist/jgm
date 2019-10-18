# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.conf import settings
from rom.models import Job


job_choices = [[job.pk, job.name] for job in Job.objects.all().order_by('sort')]


class CharacterForm(forms.Form):
    ign = forms.CharField(label='In Game Name', max_length=255, required=True,
                          widget=forms.TextInput(attrs={'class': 'form-control'}))
    base_level = forms.IntegerField(label='Base Level', min_value=1, max_value=settings.CHARACTER_MAX_LEVEL, initial=1,
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))
    contribution = forms.IntegerField(label='Contribution', min_value=0, initial=0,
                                      widget=forms.NumberInput(attrs={'class': 'form-control'}))
    gold_medal = forms.IntegerField(label='Gold Medal', min_value=0, initial=0,
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))
    jobs = forms.MultipleChoiceField(label='Jobs', required=True, widget=forms.CheckboxSelectMultiple, choices=job_choices)
