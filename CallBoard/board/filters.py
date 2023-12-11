from django import forms
from django_filters import FilterSet, ChoiceFilter, BooleanFilter

from .models import Respond


class RespondFilter(FilterSet):

    announcement = ChoiceFilter(
        field_name='announcement',
        label='Объявление',
        lookup_expr='in'
    )

    confirmed = BooleanFilter(
        field_name='confirmed',
        label='Принят',
        widget=forms.CheckboxInput,
        lookup_expr='exact'
    )

    class Meta:

        model = Respond
        fields = ['announcement', 'confirmed',]
