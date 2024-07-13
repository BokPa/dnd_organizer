from django.test import TestCase

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client


from .models import Campaign, CampaignUserRole, Character


@pytest.mark.django_db
def test_user_registration(client):
    register_url = reverse('registration')
    user_data = {
        'login': 'testuser',
        'email': 'test@example.com',
        'password_1': '123',
        'password_2': '123',
    }

    response = client.post(register_url, user_data)
# 302 sprawdza przekierowanie
    assert response.status_code == 302
    assert User.objects.filter(username='testuser').exists()

@pytest.mark.django_db
def test_registration_with_existing_username(client):
    User.objects.create_user(username='testuser', email='existing@example.com', password='12222222222222223')
    register_url = reverse('registration')
    user_data = {
        'login': 'testuser',
        'email': 'test2@example.com',
        'password_1': '123',
        'password_2': '123',
    }

    response = client.post(register_url, user_data)

    assert response.status_code == 200
    assert '__all__' in response.context['form'].errors
    assert User.objects.filter(email='test2@example.com').count() == 0

@pytest.mark.django_db
def test_registration_with_empty_email(client):
    register_url = reverse('registration')
    user_data = {
        'login': 'testuser',
        'email': '',
        'password_1': '123',
        'password_2': '123',
    }

    response = client.post(register_url, user_data)

    assert 'email' in response.context['form'].errors
    assert User.objects.filter(username='testuser').count() == 0

@pytest.mark.django_db
def test_registration_with_non_matching_passwords(client):
    register_url = reverse('registration')
    user_data = {
        'login': 'testuser',
        'email': 'test@example.com',
        'password_1': '123',
        'password_2': '1234',
    }

    response = client.post(register_url, user_data)

    assert '__all__' in response.context['form'].errors
    assert User.objects.filter(username='testuser').count() == 0


@pytest.mark.django_db
def test_create_campaign(client, create_login_user):
    create_campaign_url = reverse('add-campaign')
    campaign_data = {
        'name': 'Test Campaign',
    }

    response = client.post(create_campaign_url, campaign_data)

    assert response.status_code == 302
    assert Campaign.objects.filter(name='Test Campaign').exists()
    campaign = Campaign.objects.get(name='Test Campaign')
    assert CampaignUserRole.objects.filter(user=create_login_user, campaign=campaign, user_role=1).exists()



@pytest.mark.django_db
def test_add_player_to_campaign(client, create_login_user, create_player, create_campaign):
    add_player_url = reverse('add-players', kwargs={'campaign_id': create_campaign.id})
    player_data = {
        'players': [create_player.id],
    }

    response = client.post(add_player_url, player_data)

    assert response.status_code == 302
    assert create_campaign.players.filter(username='testnewplayer').exists()
    assert CampaignUserRole.objects.filter(user=create_player, campaign=create_campaign, user_role=2).exists()


@pytest.mark.django_db
def test_display_campaigns_for_user(client, create_login_user, create_campaign):
    campaign_non_admin = Campaign.objects.create(name='Non-Admin Campaign')
    campaigns_list_url = reverse('campaigns-list')

    response = client.get(campaigns_list_url)

    assert create_campaign.name in response.content.decode()
    assert campaign_non_admin.name not in response.content.decode()


@pytest.mark.django_db
def test_display_characters_for_user(client, create_login_user, create_character, create_player):
    character_not_owned = Character.objects.create(
        name='Non-Admin Character',
        main_class=2,
        level=1,
        hit_points=10,
        armor_class=15,
        hit_dices_number=1,
        hit_dices=6,
        strength=10,
        dexterity=10,
        constitution=10,
        intelligence=10,
        wisdom=10,
        charisma=10,
        owner=create_player,
    )
    characters_list_url = reverse('campaigns-list')
    response = client.get(characters_list_url)
    assert create_character.name in response.content.decode()
    assert character_not_owned.name not in response.content.decode()


@pytest.mark.django_db
def test_add_character(client, create_login_user):
    add_character_url = reverse('add-character')

    character_data = {
        'name': 'New Character',
        'main_class': 1,
        'level': 1,
        'hit_points': 10,
        'armor_class': 15,
        'hit_dices_number': 1,
        'hit_dices': 3,
        'strength': 10,
        'dexterity': 10,
        'constitution': 10,
        'intelligence': 10,
        'wisdom': 10,
        'charisma': 10,
        'owner': create_login_user,
    }


    response = client.post(add_character_url, character_data)

    assert response.status_code == 302
    assert Character.objects.filter(name='New Character').exists()