import datetime

import pytest
from django.contrib.auth.models import User
from django.test import Client

from ads.models import Ad, Category, ExchangeProposal


@pytest.fixture
def user():
    return User.objects.create_user(username='user', password='password123')


@pytest.fixture
def second_user():
    return User.objects.create_user(username='user2', password='password123')


@pytest.fixture
def authenticated_user(db, user):
    client = Client()
    client.login(username=user.username, password='password123')
    return client, user


@pytest.fixture
def category():
    return Category.objects.create(name='category')


@pytest.fixture
def ad_data():
    return {
        'title': 'Example title',
        'description': 'Example description',
        'condition': 'new',
    }


@pytest.fixture
def second_ad_data():
    return {
        'title': 'Example title2',
        'description': 'Example description2',
        'condition': 'used',
    }


@pytest.fixture
def ad(ad_data, user, category):
    ad = Ad(user=user, created_at=datetime.date.fromisoformat('2025-05-26'), **ad_data)
    ad.save()
    ad.category.add(category)
    return ad


@pytest.fixture
def second_ad(second_ad_data, second_user, category):
    ad = Ad(
        user=second_user, created_at=datetime.date.fromisoformat('2025-05-26'), **second_ad_data
    )
    ad.save()
    ad.category.add(category)
    return ad


@pytest.fixture
def proposal_data(ad, second_ad):
    return {
        'ad_sender': ad.id,
        'ad_receiver': second_ad.id,
        'comment': 'comment',
    }


@pytest.fixture
def proposal(ad, second_ad):
    return ExchangeProposal.objects.create(
        ad_sender=second_ad,
        ad_receiver=ad,
        created_at=datetime.date.fromisoformat('2025-05-26'),
        status='pending',
        comment='comment',
    )


@pytest.fixture
def second_proposal(ad, second_ad):
    return ExchangeProposal.objects.create(
        ad_sender=ad,
        ad_receiver=second_ad,
        created_at=datetime.date.fromisoformat('2025-05-26'),
        status='pending',
        comment='comment',
    )
