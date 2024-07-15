from django import forms
from django.forms import widgets
from django.core.validators import BaseValidator
from django.core.exceptions import ValidationError

from webapp.models import Type
from webapp.models import Status

def validate_summary(value):
    if "bad_word" in value.lower():
        raise ValidationError("Заголовок содержит бранные слова")

class NoSpecificCharactersValidator(BaseValidator):
    message = "Заголовок не должен содержать определенные символы"
    code = "no_specific_characters"

    def compare(self, value, initial):
        forbidden_characters = ['@', '#', '$', '^']
        return not any(char in forbidden_characters for char in str(value))

def at_least_5_summary(value):
    if len(value) < 5:
        raise ValidationError('Заголовок должен содержать не менее 5 символов')

class IssueForm(forms.Form):
    summary = forms.CharField(max_length=50, required=True, label="Заголовок",
                              validators=[validate_summary, at_least_5_summary])
    description = forms.CharField(max_length=2000, required=False, label="Описание",
                                  widget=widgets.Textarea(attrs={"cols": 30, "rows": 5, "class": "test"}),)
    types = forms.ModelMultipleChoiceField(queryset=Type.objects.all(), label="Типы")
    status = forms.ModelChoiceField(queryset=Status.objects.all(), label="Статусы")


class TypeForm(forms.Form):
    title = forms.CharField(max_length=50, required=True, label="Название")

class StatusForm(forms.Form):
    title = forms.CharField(max_length=50, required=True, label="Название")