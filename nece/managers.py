from django.db import models
from django.db.models.query import (BaseIterable,
                                    get_related_populators,
                                    deferred_class_factory)
from django.conf import settings

TRANSLATIONS_DEFAULT = getattr(settings, 'TRANSLATIONS_DEFAULT', 'en_us')
TRANSLATIONS_MAP = getattr(settings, 'TRANSLATIONS_MAP', {'en': 'en_us'})


class TranslationModelIterable(BaseIterable):
    """
    Exact copy of django.db.models.query.ModelIterable with a minor difference
    TODO: find a way to extend generators
    """

    def __iter__(self):
        queryset = self.queryset
        db = queryset.db
        compiler = queryset.query.get_compiler(using=db)
        # Execute the query. This will also fill compiler.select, klass_info,
        # and annotations.
        results = compiler.execute_sql()
        select, klass_info, annotation_col_map = (
            compiler.select, compiler.klass_info, compiler.annotation_col_map)
        if klass_info is None:
            return
        model_cls = klass_info['model']
        select_fields = klass_info['select_fields']
        model_fields_start, model_fields_end = (select_fields[0],
                                                select_fields[-1] + 1)
        init_list = [f[0].target.attname
                     for f in select[model_fields_start:model_fields_end]]
        if len(init_list) != len(model_cls._meta.concrete_fields):
            init_set = set(init_list)
            skip = [f.attname for f in model_cls._meta.concrete_fields
                    if f.attname not in init_set]
            model_cls = deferred_class_factory(model_cls, skip)
        related_populators = get_related_populators(klass_info, select, db)
        for row in compiler.results_iter(results):
            obj = model_cls.from_db(db, init_list,
                                    row[model_fields_start:model_fields_end])
            if related_populators:
                for rel_populator in related_populators:
                    rel_populator.populate(row, obj)
            if annotation_col_map:
                for attr_name, col_pos in annotation_col_map.items():
                    setattr(obj, attr_name, row[col_pos])

            # Add the known related objects to the model, if there are any
            if queryset._known_related_objects:
                for field, rel_objs in queryset._known_related_objects.items():
                    # Avoid overwriting objects loaded e.g. by select_related
                    if hasattr(obj, field.get_cache_name()):
                        continue
                    pk = getattr(obj, field.get_attname())
                    try:
                        rel_obj = rel_objs[pk]
                    except KeyError:
                        pass  # may happen in qs1 | qs2 scenarios
                    else:
                        setattr(obj, field.name, rel_obj)
            obj.language(queryset._language_code)
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

    def language(self, language_code):
        if self.is_default_language(language_code):
            return self._make_queryset(TranslationQuerySet)
        language_code = self.get_language_key(language_code)
        return self._make_queryset(TranslationQuerySet).language(
            language_code).filter(translations__has_key=(language_code))

    def language_or_default(self, language_code):
        raise NotImplementedError()
