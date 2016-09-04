from django.db import models
from django.conf import settings
from django.db.models.query import ModelIterable


class TranslationMixin(object):
    TRANSLATIONS_DEFAULT = getattr(settings, 'TRANSLATIONS_DEFAULT', 'en_us')
    TRANSLATIONS_MAP = getattr(settings, 'TRANSLATIONS_MAP', {'en': 'en_us'})
    _default_language_code = TRANSLATIONS_DEFAULT

    def get_language_key(self, language_code):
        return (self.TRANSLATIONS_MAP.get(language_code, language_code) or
                self._default_language_code)

    def is_default_language(self, language_code):
        language_code = self.get_language_key(language_code)
        return language_code == self.TRANSLATIONS_DEFAULT


class TranslationModelIterable(ModelIterable):
    def __iter__(self):
        for obj in super(TranslationModelIterable, self).__iter__():
            if self.queryset._language_code:
                obj.language(self.queryset._language_code)
            yield obj


class TranslationQuerySet(models.QuerySet, TranslationMixin):
    _language_code = None

    def __init__(self, model=None, query=None, using=None, hints=None):
        super(TranslationQuerySet, self).__init__(model, query, using, hints)
        self._iterable_class = TranslationModelIterable

    def language_or_default(self, language_code):
        language_code = self.get_language_key(language_code)
        self._language_code = language_code
        return self

    def language(self, language_code):
        language_code = self.get_language_key(language_code)
        self._language_code = language_code
        results = self.language_or_default(language_code)
        if self.is_default_language(language_code):
            return results
        return results.filter(translations__has_key=(language_code))

    def _clone(self, *args, **kwargs):
        clone = super(TranslationQuerySet, self)._clone(*args, **kwargs)
        clone._language_code = self._language_code
        return clone

    def filter(self, *args, **kwargs):
        if not self.is_default_language(self._language_code):
            for key, value in kwargs.items():
                if key.split('__')[0] in self.model._meta.translatable_fields:
                    del kwargs[key]
                    key = 'translations__{}__{}'.format(
                        self._language_code, key)
                    kwargs[key] = value
        return super(TranslationQuerySet, self).filter(*args, **kwargs)


class TranslationManager(models.Manager, TranslationMixin):
    _queryset_class = TranslationQuerySet

    def get_queryset(self, language_code=None):
        qs = self._queryset_class(self.model, using=self.db, hints=self._hints)
        language_code = self.get_language_key(language_code)
        qs.language(language_code)
        return qs

    def language_or_default(self, language_code):
        language_code = self.get_language_key(language_code)
        return self.get_queryset(language_code).language_or_default(
            language_code)

    def language(self, language_code):
        language_code = self.get_language_key(language_code)
        return self.get_queryset(language_code).language(language_code)
