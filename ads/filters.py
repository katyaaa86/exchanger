import django_filters

from ads.models import Ad, Category


class AdFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок содержит',
    )
    description = django_filters.CharFilter(
        field_name='description',
        lookup_expr='icontains',
        label='Описание содержит',
    )
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        label='Категория',
    )
    condition = django_filters.ChoiceFilter(
        choices=Ad.CONDITION_CHOICES,
        label='Состояние',
    )

    class Meta:
        model = Ad
        fields = ['title', 'description', 'category', 'condition']
