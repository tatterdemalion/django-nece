from django.db import models
from django.db.models.query import ModelIterable
from django.conf import settings

TRANSLATIONS_DEFAULT = getattr(settings, 'TRANSLATIONS_DEFAULT', 'en_us')
TRANSLATIONS_MAP = getattr(settings, 'TRANSLATIONS_MAP', {'en': 'en_us'})


class TranslationModelIterable(ModelIterable):
    def __iter__(self):
        for obj in super(TranslationModelIterable, self).__iter__():
            obj.language(self.queryset._language_code)
            yield obj


class TranslationMixin(object):
    _default_language_code = TRANSLATIONS_DEFAULT

    def get_language_key(self, language_code):
        return TRANSLATIONS_MAP.get(
            language_code, language_code)

    def is_default_language(self, language_code):
        language_code = self.get_language_key(language_code)
        return language_code == TRANSLATIONS_DEFAULT


class TranslationQuerySet(models.QuerySet, TranslationMixin):
    _language_code = None

    def __init__(self, model=None, query=None, using=None, hints=None):
        super(TranslationQuerySet, self).__init__(model, query, using, hints)
        self._iterable_class = TranslationModelIterable

    def language(self, language_code):
        self._language_code = language_code
        return self

    def _clone(self, **kwargs):
        query = self.query.clone()
        if self._sticky_filter:
            query.filter_is_sticky = True
        clone = self.__class__(model=self.model, query=query,
                               using=self._db, hints=self._hints)
        clone._for_write = self._for_write
        clone._prefetch_related_lookups = self._prefetch_related_lookups[:]
        clone._known_related_objects = self._known_related_objects
        clone._iterable_class = self._iterable_class
        clone._fields = self._fields
        clone._language_code = self._language_code
        clone.__dict__.update(kwargs)
        return clone


class TranslationManager(models.Manager, TranslationMixin):
    def _make_queryset(self, klass):
        qs = klass(self.model, using=self.db, hints=self._hints)
        return qs

    def language_or_default(self, language_code):
        if self.is_default_language(language_code):
            return self._make_queryset(TranslationQuerySet)
        language_code = self.get_language_key(language_code)
        return self._make_queryset(TranslationQuerySet).language(
            language_code)

    def language(self, language_code):
        return self.language_or_default(language_code).filter(
            translations__has_key=(language_code))
