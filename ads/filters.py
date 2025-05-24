import django_filters

from ads.models import Ad, Category, ExchangeProposal


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


def extract_ad_receivers(request):
    if request is None or not request.user.is_authenticated:
        return Ad.objects.none()
    receivers_id = (
        ExchangeProposal.objects.filter(ad_sender__user=request.user)
        .values_list('ad_receiver_id', flat=True)
        .distinct()
    )
    return Ad.objects.filter(id__in=receivers_id)


def extract_ad_senders(request):
    if request is None or not request.user.is_authenticated:
        return Ad.objects.none()
    senders_id = (
        ExchangeProposal.objects.filter(ad_receiver__user=request.user)
        .values_list('ad_sender_id', flat=True)
        .distinct()
    )
    return Ad.objects.filter(id__in=senders_id)


class SentExchangeProposalFilter(django_filters.FilterSet):
    ad_receiver = django_filters.ModelChoiceFilter(
        queryset=extract_ad_receivers,
        label='Получатель',
    )
    status = django_filters.ChoiceFilter(
        choices=ExchangeProposal.STATUS_CHOICES,
        label='Статус',
    )

    class Meta:
        model = ExchangeProposal
        fields = ['ad_receiver', 'status']


class ReceivedExchangeProposalFilter(django_filters.FilterSet):
    ad_sender = django_filters.ModelChoiceFilter(
        queryset=extract_ad_senders,
        label='Отправитель',
    )
    status = django_filters.ChoiceFilter(
        choices=ExchangeProposal.STATUS_CHOICES,
        label='Статус',
    )

    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'status']
