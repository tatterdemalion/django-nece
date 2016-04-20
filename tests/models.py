from __future__ import unicode_literals

from django.db import models
from nece.models import TranslationModel


class Fruit(TranslationModel):
    name = models.CharField(max_length=255)
    benefits = models.CharField(max_length=255)
    scientific_name = models.CharField(max_length=255)

    class Meta:
        translatable_fields = ('name', 'benefits', )

    def __str__(self):
        return self.name
