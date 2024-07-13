from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from .models import Campaign, Character, CampaignUserRole

User = get_user_model()


class UserCampaignMixin:
    def get_campaigns(self):
        user = self.request.user
        if user.is_authenticated:
            return Campaign.objects.filter(
                campaignuserrole__user=user,
                campaignuserrole__user_role=1
            )
        return Campaign.objects.none()

    def get_characters(self):
        user = self.request.user
        if user.is_authenticated:
            return Character.objects.filter(owner=user)
        return Character.objects.none()


class AddedToCampaignMixin:
    def dispatch(self, request, *args, **kwargs):
        campaign_id = self.kwargs.get('campaign_id')
        campaign = get_object_or_404(Campaign, id=campaign_id)
        user_assigned = CampaignUserRole.objects.filter(campaign=campaign, user=request.user, user_role=1).exists()

        if not user_assigned:
            return redirect('campaigns-list')
        return super().dispatch(request, *args, **kwargs)


class UserIsOwnerMixin:
    def dispatch(self, request, *args, **kwargs):
        character_id = kwargs.get('character_id')
        character = get_object_or_404(Character, id=character_id)

        if character.owner != request.user:
            if character.campaign:
                campaign = get_object_or_404(Campaign, id=character.campaign_id)
                user_role = CampaignUserRole.objects.filter(user=request.user, campaign=campaign).first()
                if not user_role or user_role.user_role != 1:
                    return redirect(reverse('campaigns-list'))
                else:
                    return super().dispatch(request, *args, **kwargs)
            return redirect(reverse('campaigns-list'))
        return super().dispatch(request, *args, **kwargs)
