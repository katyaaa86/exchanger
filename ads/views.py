from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic

from ads.filters import AdFilter
from ads.forms import AdForm
from ads.models import Ad


class AdsList(generic.ListView):
    model = Ad
    template_name = 'ads_list.html'
    context_object_name = 'ads'
    paginate_by = 10

    def _prepare_base_queryset(self):
        return (
            Ad.objects.select_related('user').prefetch_related('category').order_by('-created_at')
        )

    def get_queryset(self):
        queryset = self._prepare_base_queryset()
        if self.request.user.is_authenticated:
            return queryset.filter(~Q(user=self.request.user))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = AdFilter(self.request.GET, queryset=self.get_queryset())
        return context


class UserAdsList(LoginRequiredMixin, AdsList):

    def get_queryset(self):
        return self._prepare_base_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = True
        return context


class AdDetail(generic.DetailView):
    model = Ad
    template_name = 'ad_detail.html'


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
