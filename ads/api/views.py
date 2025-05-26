from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from ads.api.filters import AdAPIFilter
from ads.api.permissions import IsOwnerOrReadOnly, IsReceiverOrReadOnly
from ads.api.serializers import AdSerializer, ProposalSerializer, ProposalStatusUpdateSerializer
from ads.models import Ad, ExchangeProposal


@extend_schema(
    parameters=[
        OpenApiParameter(
            name='is_mine',
            type=bool,
            location=OpenApiParameter.QUERY,
            description='Если true - отображаются объявления текущего пользователя',
        )
    ]
)
class AdViewSet(viewsets.ModelViewSet):
    serializer_class = AdSerializer
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdAPIFilter

    def get_queryset(self):
        return (
            Ad.objects.select_related('user').prefetch_related('category').order_by('-created_at')
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProposalViewSet(viewsets.ModelViewSet):
    serializer_class = ProposalSerializer
    permission_classes = [IsReceiverOrReadOnly, permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return (
            ExchangeProposal.objects.select_related('ad_sender__user', 'ad_receiver__user')
            .filter(Q(ad_sender__user=self.request.user) | Q(ad_receiver__user=self.request.user))
            .order_by('-created_at')
        )

    def update(self, request, *args, **kwargs):
        proposal = self.get_object()
        serializer = ProposalStatusUpdateSerializer(
            proposal, data=request.data, context={'request': request}, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response({'status': proposal.status}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
