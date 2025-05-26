from django_filters import rest_framework

from ads.models import Ad


class AdAPIFilter(rest_framework.FilterSet):
    is_mine = rest_framework.BooleanFilter(method='filter_is_mine', label='Мои объявления')

    class Meta:
        model = Ad
        fields = ['title', 'description', 'category', 'condition']

    def filter_is_mine(self, queryset, name, is_mine):
        user = self.request.user
        if not user.is_authenticated:
            return queryset
        if is_mine:
            return queryset.filter(user=user)
        return queryset.exclude(user=user)
