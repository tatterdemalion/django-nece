# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import options

from nece.managers import TranslationManager, TranslationMixin
from nece.exceptions import NonTranslatableFieldError


options.DEFAULT_NAMES += ('translatable_fields',)


class Language(object):
    def __init__(self, **translations):
        for field, translation in translations.items():
            setattr(self, field, translation)


class TranslationModel(models.Model, TranslationMixin):
    translations = JSONField(null=True, blank=True)
    default_language = None
    _translated = None

    objects = TranslationManager()

    def __init__(self, *args, **kwargs):
        self._language_code = self._default_language_code
        return super(TranslationModel, self).__init__(*args, **kwargs)

    def __getattribute__(self, name):
        attr = object.__getattribute__(self, name)
        if name.startswith('__'):
            return attr
        translated = object.__getattribute__(self, '_translated')
        if translated:
            if hasattr(translated, name):
                return getattr(translated, name) or attr
        return attr

    def populate_translations(self, translations):
        for field in self._meta.translatable_fields:
            if field not in translations:
                translations[field] = None
        return translations

    def translate(self, language_code=None, **kwargs):
        if language_code:
            self._language_code = language_code
        if not self.is_default_language(self._language_code):
            self.translations = self.translations or {}
            self.translations[self._language_code] = self.translations.get(
                self._language_code, {}
            )
        for name, value in kwargs.items():
            if name not in self._meta.translatable_fields:
                raise NonTranslatableFieldError(name)
            if self.is_default_language(self._language_code):
                setattr(self, name, value)
            else:
                self.translations.get(self._language_code, {})[name] = value
        if language_code:
            self.language(language_code)

    def reset_language(self):
        self._translated = None
        self._language_code = self._default_language_code

    def language(self, language_code, fallback=True):
        self.reset_language()

        # Default language
        if self.is_default_language(language_code):
            self._language_code = language_code
            return self

        # Not default language
        language_codes = self.get_language_keys(language_code, fallback)
        # Default language field
        fields = self._meta.translatable_fields
        self.default_language = Language(
            **{i: getattr(self, i, None) for i in fields})
        # Translation fields
        if self.translations:
            for code in language_codes:
                translations = self.translations.get(code)
                if translations:
                    self._language_code = code
                    trans = self.populate_translations(translations)
                    self._translated = Language(**trans)
                    break

        return self

    def language_or_none(self, language_code):
        language_code = self.get_language_key(language_code)
        if self.is_default_language(language_code):
            return self.language(language_code)
        if not self.translations or not self.translations.get(language_code):
            return None
        return self.language(language_code)

    def language_as_dict(self, language_code=None, fallback=True):
        if not language_code:
            language_code = self._language_code
        tf = self._meta.translatable_fields
        language_codes = self.get_language_keys(language_code, fallback)
        for code in language_codes:
            # Default language code
            if code == self._default_language_code:
                return {k: v for k, v in self.__dict__.items() if k in tf}
            # Not default language code
            if self.translations:
                translations = self.translations.get(code)
                if translations:
                    return {k: v for k, v in translations.items() if v and k in tf}
        return {}

    def save(self, *args, **kwargs):
        language_code = self._language_code
        self.reset_language()
        if self.translations == '':
            self.translations = None
        super(TranslationModel, self).save(*args, **kwargs)
        self.language(language_code)

    class Meta:
        abstract = True
