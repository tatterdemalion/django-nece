from django.contrib import admin
from nece.forms import TranslationForm


class TranslationAdmin(admin.ModelAdmin):
    form = TranslationForm
