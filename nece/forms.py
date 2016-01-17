from django import forms
from nece.widgets import TranslationWidget


class TranslationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TranslationForm, self).__init__(*args, **kwargs)
        self.fields['translations'].widget = TranslationWidget(
            instance=self.instance)
