from django import forms
from django_filters import FilterSet, BooleanFilter

from .models import Respond, Announcement


class RespondFilter(FilterSet):

    confirmed = BooleanFilter(
        field_name='confirmed',
        label='Принят',
        widget=forms.CheckboxInput,
        lookup_expr='exact'
    )

    def __init__(self, *args, **kwargs):

        super(RespondFilter, self).__init__(*args, **kwargs)
        self.filters['announcement'].queryset = Announcement.objects.filter(user_id=kwargs['request'])

    class Meta:

        model = Respond
        fields = ['announcement', 'confirmed',]
