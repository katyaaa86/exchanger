from django.views import generic

from ads.models import Ad


class AdsList(generic.ListView):
    model = Ad
    template_name = 'ads_list.html'
    context_object_name = 'ads'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        return Ad.objects.select_related('user').prefetch_related('category')
