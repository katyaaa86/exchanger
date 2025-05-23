from django import forms

from ads.models import Ad


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        labels = {
            'title': 'Заголовок',
            'description': 'Описание',
            'image_url': 'Изображение',
            'category': 'Категории',
            'condition': 'Состояние',
        }
        fields = ['title', 'description', 'image_url', 'category', 'condition']
