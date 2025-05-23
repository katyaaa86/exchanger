from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Ad(models.Model):
    CONDITION_CHOICES = (
        ('new', 'новый'),
        ('used', 'б/у'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField()
    image_url = models.ImageField(upload_to='uploads/', null=True, blank=True)
    category = models.ManyToManyField(Category)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='NW')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/ads/{self.id}'


class ExchangeProposal(models.Model):
    STATUS_CHOICES = (
        ('pending', 'ожидает'),
        ('accept', 'принята'),
        ('decline', 'отклонена'),
    )
    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='sent_proposals')
    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='received_proposals')
    comment = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
