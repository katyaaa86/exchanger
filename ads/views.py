from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View, generic
from django.views.generic.edit import FormMixin
from django_filters.views import FilterView

from ads.filters import AdFilter, ReceivedExchangeProposalFilter, SentExchangeProposalFilter
from ads.forms import AdForm, ExchangeProposalForm
from ads.models import Ad, ExchangeProposal


class AdsListView(FilterView):
    model = Ad
    template_name = 'ads_list.html'
    context_object_name = 'ads'
    paginate_by = 10
    filterset_class = AdFilter

    def _prepare_base_queryset(self):
        return (
            Ad.objects.select_related('user').prefetch_related('category').order_by('-created_at')
        )

    def get_queryset(self):
        queryset = self._prepare_base_queryset()
        if self.request.user.is_authenticated:
            return queryset.filter(~Q(user=self.request.user))
        return queryset


class UserAdsListView(LoginRequiredMixin, AdsListView):

    def get_queryset(self):
        return self._prepare_base_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = True
        return context


class AdDetailView(FormMixin, generic.DetailView):
    model = Ad
    template_name = 'ad_detail.html'
    form_class = ExchangeProposalForm
    success_url = reverse_lazy('sent_proposals_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['form'] = self.get_form()
            context['is_not_author'] = self.request.user != self.object.user
        return context

    def post(self, request, *args, **kwargs):
        ad = self.get_object()
        form = self.get_form()
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.ad_receiver = ad
            proposal.save()
            return self.form_valid(form)
        return self.form_invalid(form)


class AdCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'ad_create.html'
    form_class = AdForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AdUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'ad_create.html'
    form_class = AdForm

    def get_queryset(self):
        return Ad.objects.filter(user=self.request.user)


class AdDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'ad_delete.html'
    success_url = reverse_lazy('user_ads_list')

    def get_queryset(self):
        return Ad.objects.filter(user=self.request.user)


class BaseProposalsListView(LoginRequiredMixin):
    template_name = 'proposals_list.html'
    context_object_name = 'proposals'
    paginate_by = 10

    def _prepare_base_queryset(self):
        return ExchangeProposal.objects.select_related(
            'ad_sender__user', 'ad_receiver__user'
        ).order_by('-created_at')


class SentProposalsListView(BaseProposalsListView, FilterView):
    filterset_class = SentExchangeProposalFilter

    def get_queryset(self):
        queryset = self._prepare_base_queryset()
        return queryset.filter(ad_sender__user=self.request.user)


class ReceivedProposalsListView(BaseProposalsListView, FilterView):
    filterset_class = ReceivedExchangeProposalFilter

    def get_queryset(self):
        queryset = self._prepare_base_queryset()
        return queryset.filter(ad_receiver__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_received'] = True
        return context


class ExchangeProposalStatusUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        proposal = get_object_or_404(ExchangeProposal, pk=pk)

        if proposal.ad_receiver.user != request.user:
            return HttpResponseForbidden("Недостаточно прав")

        new_status = request.POST.get('status')
        if new_status in (s[0] for s in ExchangeProposal.STATUS_CHOICES):
            proposal.status = new_status
            proposal.save()

        return redirect(request.META.get('HTTP_REFERER', '/'))


ERROR_MESSAGES = {
    400: "Неверный запрос. Проверьте введённые данные.",
    403: "Доступ запрещён. У вас нет прав для этого действия.",
    404: "Страница не найдена.",
    500: "Ошибка сервера.",
}


def error_view(request, exception=None, status_code=500):
    error_message = ERROR_MESSAGES.get(status_code, "Неизвестная ошибка.")
    return render(request, "error_page.html", {'error_message': error_message}, status=status_code)
