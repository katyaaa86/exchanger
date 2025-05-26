import pytest
from django.urls import reverse

from ads.models import ExchangeProposal


pytestmark = pytest.mark.django_db


@pytest.mark.django_db
def test_create_ad(authenticated_user, proposal_data, ad, second_ad):
    client, user = authenticated_user
    url = reverse('ad_detail', args=[second_ad.id])

    response = client.post(url, proposal_data)

    assert response.status_code == 302
    proposals = ExchangeProposal.objects.filter(ad_sender=ad)
    assert proposals.exists()
    proposal = proposals.first()
    assert proposal.ad_sender == ad
    assert proposal.ad_receiver == second_ad
    assert proposal.comment == proposal_data['comment']
    assert proposal.status == 'pending'


@pytest.mark.django_db
def test_update_proposal_status(authenticated_user, second_user, ad, second_ad, proposal):
    client, user = authenticated_user
    url = reverse('proposal_status_update', args=[proposal.id])

    response = client.post(url, {'status': 'accept'})
    proposal.refresh_from_db()

    assert response.status_code == 302
    assert proposal.status == 'accept'


@pytest.mark.django_db
def test_update_proposal_status_by_another_user(
    authenticated_user, second_user, ad, second_ad, second_proposal
):
    client, user = authenticated_user
    url = reverse('proposal_status_update', args=[second_proposal.id])

    response = client.post(url, {'status': 'accept'})
    second_proposal.refresh_from_db()

    assert response.status_code == 403
    assert second_proposal.status == 'pending'
