from django import forms
from django_filters import FilterSet, ChoiceFilter

from .models import Respond


class RespondFilter(FilterSet):

    announcement = ChoiceFilter(
        field_name='announcement',
        label='Объявление',
        lookup_expr='iexact'
    )

    class Meta:

        model = Respond
        fields = ['announcement']
