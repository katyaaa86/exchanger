from django.contrib import admin

from ads.models import Ad, Category, ExchangeProposal


admin.site.register(Ad)
admin.site.register(ExchangeProposal)
admin.site.register(Category)
