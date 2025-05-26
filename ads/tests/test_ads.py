import pytest
from django.urls import reverse

from ads.models import Ad


pytestmark = pytest.mark.django_db


@pytest.mark.django_db
def test_create_ad(authenticated_user, ad_data, category):
    client, user = authenticated_user
    url = reverse('ad_create')
    ad_data['category'] = [category.id]
    response = client.post(url, ad_data)
    assert response.status_code == 302

    ads = Ad.objects.filter(title='Example title')
    assert ads.exists()
    ad = ads.first()
    assert ad.title == ad_data['title']
    assert ad.description == ad_data['description']
    assert ad.category.first().id == category.id
    assert ad.user == user


@pytest.mark.django_db
def test_list_ads_without_login(client, ad):
    url = reverse('ads_list')
    response = client.get(url)

    content = response.content.decode()
    assert response.status_code == 200
    assert ad.title in content
    assert ad.description in content
    assert ad.category.all().first().name in content
    assert ad.condition in content


@pytest.mark.django_db
def test_my_list_ads(authenticated_user, ad):
    client, user = authenticated_user
    url = reverse('user_ads_list')
    response = client.get(url)

    content = response.content.decode()
    assert response.status_code == 200
    assert ad.title in content
    assert ad.description in content
    assert ad.category.all().first().name in content
    assert ad.condition in content
    assert ad.user.username in content


@pytest.mark.django_db
def test_other_list_ads(authenticated_user, second_ad, ad):
    client, user = authenticated_user
    url = reverse('ads_list')
    response = client.get(url)

    content = response.content.decode()
    assert response.status_code == 200
    assert second_ad.title in content
    assert second_ad.description in content
    assert second_ad.category.all().first().name in content
    assert second_ad.condition in content
    assert second_ad.user.username in content


@pytest.mark.django_db
def test_update_ad(authenticated_user, ad, category):
    client, user = authenticated_user
    url = reverse('ad_update', args=[ad.id])
    updated_data = {
        'title': 'new title',
        'description': 'new description',
        'condition': 'used',
        'category': [category.id],
    }

    response = client.post(url, updated_data)
    ad.refresh_from_db()

    assert response.status_code == 302
    assert ad.title == updated_data['title']
    assert ad.description == updated_data['description']
    assert ad.condition == updated_data['condition']


@pytest.mark.django_db
def test_update_ad_without_login(client, ad, ad_data, category):
    url = reverse('ad_update', args=[ad.id])
    updated_data = {
        'title': 'new title',
        'description': 'new description',
        'condition': 'used',
        'category': [category.id],
    }

    response = client.post(url, updated_data)
    ad.refresh_from_db()

    assert response.status_code == 302
    assert ad.title == ad_data['title']
    assert ad.description == ad_data['description']
    assert ad.condition == ad_data['condition']


@pytest.mark.django_db
def test_delete_ad(authenticated_user, ad):
    ad_id = ad.id
    client, user = authenticated_user
    url = reverse('ad_delete', args=[ad.id])

    response = client.delete(url)

    assert response.status_code == 302
    assert not Ad.objects.filter(id=ad_id).first()


@pytest.mark.django_db
def test_search_title_list_ads(client, ad, second_ad):
    url = reverse('ads_list')

    response = client.get(url, {'title': second_ad.title})
    content = response.content.decode()

    assert response.status_code == 200
    assert second_ad.title in content


@pytest.mark.django_db
def test_search_desc_list_ads(client, ad, second_ad):
    url = reverse('ads_list')

    response = client.get(url, {'description': second_ad.description})
    content = response.content.decode()

    assert response.status_code == 200
    assert second_ad.description in content


@pytest.mark.django_db
def test_search_condition_list_ads(client, ad, second_ad):
    url = reverse('ads_list')

    response = client.get(url, {'condition': second_ad.condition})
    content = response.content.decode()

    assert response.status_code == 200
    assert second_ad.condition in content
