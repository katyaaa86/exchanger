from django import forms

from ads.models import Ad, ExchangeProposal


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


class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        labels = {
            'ad_sender': 'Объявление для обмена',
            'comment': 'Комментарий',
        }
        fields = ['ad_sender', 'comment']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['ad_sender'].queryset = Ad.objects.filter(user=user)
