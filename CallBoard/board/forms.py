from django import forms
from django.core.exceptions import ValidationError
from .models import Announcement


class AnnouncementForm(forms.ModelForm):

    class Meta:

        model = Announcement
        fields = [
            'title',
            'category',
            'text',
        ]
        widgets = {
            'title': forms.Textarea(attrs={'class': 'form-text', 'cols': 70, 'rows': 3}),
            'text': forms.Textarea(attrs={'class': 'form-text', 'cols': 70, 'rows': 10}),
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")
        category = cleaned_data.get("category")

        if title is None or title == "":
            raise ValidationError({
                "title": "Заголовок не должен быть пустым"
            })

        if text is None or text == "":
            raise ValidationError({
                "text": "Содержание должно быть заполнено"
            })

        if category is None:
            raise ValidationError({
                "category": "Необходимо выбрать категорию"
            })

        return cleaned_data
