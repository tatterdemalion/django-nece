from django.contrib import admin
from nece.admin import TranslationAdmin
from nece_test.models import Fruit

admin.site.register(Fruit, TranslationAdmin)
