import pytest
from django.contrib.auth.models import User
from django.test import Client

from dnd_organizer_app.models import Campaign, CampaignUserRole, Character


@pytest.fixture
def create_login_user(client):
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='123'
    )
    client.login(username='testuser', password='123')
    return user


@pytest.fixture
def create_player(client):
    return User.objects.create_user(
        username='testnewplayer',
        email='test@example.com',
        password='123'
    )


@pytest.fixture
def create_campaign(client, create_login_user):
    campaign = Campaign.objects.create(name='Test Campaign')
    CampaignUserRole.objects.create(
        user_role=1,
        user=create_login_user,
        campaign=campaign
    )
    return campaign

@pytest.fixture
def create_character(client, create_login_user):
    return Character.objects.create(
        name='New Character',
        main_class=1,
        level=1,
        hit_points=10,
        armor_class=15,
        hit_dices_number=2,
        hit_dices=6,
        strength=10,
        dexterity=10,
        constitution=10,
        intelligence=10,
        wisdom=10,
        charisma=10,
        owner=create_login_user
    )