from django.conf import settings
from django.contrib.admin import ModelAdmin
from django_admin_json_editor import JSONEditorWidget


def generate_translatable_schema(model):
    """
    Generates JSON schema for JSON admin editor
    :param model: model class
    :return: JSON admin schema
    """
    # noinspection PyProtectedMember
    translatable_fields = model._meta.translatable_fields
    return {
        'type': 'object',
        'properties': {
            language: {
                'type': 'object',
                'properties': {
                    field: {
                        'type': 'string'
                    } for field in translatable_fields
                },
            } for language in settings.TRANSLATIONS_MAP
        }
    }


class TranslatableModelAdmin(ModelAdmin):
    """
    Overrides `translations` field
    """

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'translations':
            kwargs['widget'] = JSONEditorWidget(generate_translatable_schema(self.model), False)
        return super(TranslatableModelAdmin, self).formfield_for_dbfield(db_field, **kwargs)
