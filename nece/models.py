from __future__ import unicode_literals
from collections import namedtuple

from django.db import models
from django.contrib.postgres.fields import JSONField
from nece.managers import TranslationManager, TranslationMixin


class TranslationModel(models.Model, TranslationMixin):
    translations = JSONField(null=True)
    default_language = None
    _translated = None

    objects = TranslationManager()

    def __init__(self, *args, **kwargs):
        self.language_class = namedtuple('Language', self.translatable_fields)
        self._language_code = self._default_language_code
        return super(TranslationModel, self).__init__(*args, **kwargs)

    def __getattribute__(self, name):
        if name.startswith('__'):
            return object.__getattribute__(self, name)
        translated = object.__getattribute__(self, '_translated')
        if translated:
            if hasattr(translated, name):
                return getattr(translated, name)
        return object.__getattribute__(self, name)

    def translate(self, language_code=None, **kwargs):
        if language_code:
            self.translations = self.translations or {}
            self.translations[language_code] = {}
            self._language_code = language_code
        for name, value in kwargs.items():
            if self.is_default_language(self._language_code):
                setattr(self, name, value)
            else:
                self.translations.get(self._language_code, {})[name] = value
        if language_code:
            self.language(language_code)

    def reset_language(self):
        self._translated = None
        self._language_code = self._default_language_code

    def language(self, language_code):
        self.reset_language()
        fields = self.translatable_fields
        self.default_language = self.language_class(
            **{i: getattr(self, i, None) for i in fields})
        self._language_code = self.get_language_key(language_code)
        if self.is_default_language(language_code):
            return self
        translations = self.translations or {}
        if translations:
            translations = translations.get(self._language_code, {})
            if translations:
                self._translated = self.language_class(**translations)
        return self

    def language_or_none(self, language_code):
        if self.is_default_language(language_code):
            return self.language(language_code)
        language_code = self.get_language_key(language_code)
        if not self.translations or self.translations.get(language_code):
            return None
        return self.language(language_code)

    def save(self, *args, **kwargs):
        language_code = self._language_code
        self.reset_language()
        super(TranslationModel, self).save(*args, **kwargs)
        self.language(language_code)

    class Meta:
        abstract = True
