from django.conf import settings
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import FormView
import sendgrid
from sendgrid.helpers.mail import Mail

from .forms import LoginForm, AddUserForm, AddCampaignForm, AddCharacterForm, AddPlayersForm, \
    AddCharacterToCampaignForm, EditCharacterForm, PlanSessionForm
from .mixins import UserCampaignMixin, AddedToCampaignMixin, UserIsOwnerMixin
from .models import Campaign, Character, CampaignUserRole, SessionDate

User = get_user_model()


class CampaignsListView(LoginRequiredMixin, UserCampaignMixin, View):
    def get(self, request, *args, **kwargs):
        campaigns = self.get_campaigns()
        characters = self.get_characters()
        context = {
            "campaigns": campaigns,
            "characters": characters,
        }
        return render(request, "dnd_organizer_app/campaigns_list.html", context)


class CharacterSheetView(LoginRequiredMixin, UserIsOwnerMixin, View):
    def get(self, request, character_id, *args, **kwargs):
        character = get_object_or_404(Character, pk=character_id)
        context = {
            "character": character
        }
        return render(request, "dnd_organizer_app/character_sheet.html", context)


class CampaignView(LoginRequiredMixin, AddedToCampaignMixin, View):
    def get(self, request, campaign_id, *args, **kwargs):
        users = User.objects.filter(
            campaignuserrole__campaign_id=campaign_id,
            campaignuserrole__user_role=2
        )
        characters = Character.objects.filter(campaign_id=campaign_id)
        campaign = get_object_or_404(Campaign, pk=campaign_id)
        upcoming_session = SessionDate.objects.filter(
            campaign=campaign,
            session_date__gte=timezone.now()
        ).first()
        context = {
            "characters": characters,
            "campaign": campaign,
            "users": users,
            "upcoming_session": upcoming_session,
        }
        return render(request, "dnd_organizer_app/campaign.html", context)

    def post(self, request, campaign_id, *args, **kwargs):

        user_id = request.POST.get("user_id")
        campaign = get_object_or_404(Campaign, pk=campaign_id)
        CampaignUserRole.objects.filter(user_id=user_id, campaign=campaign).delete()
        users = User.objects.filter(
            campaignuserrole__campaign_id=campaign_id,
            campaignuserrole__user_role=2)
        characters = Character.objects.filter(campaign_id=campaign_id
                                              )
        upcoming_session = SessionDate.objects.filter(
            campaign=campaign,
            ession_date__gte=timezone.now()
        ).first()

        context = {
            "characters": characters,
            "campaign": campaign,
            "users": users,
            "upcoming_session": upcoming_session,
        }
        return render(request, "dnd_organizer_app/campaign.html", context)


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'dnd_organizer_app/login.html'
    success_url = reverse_lazy('campaigns-list')

    def form_valid(self, form):
        user = form.user
        login(self.request, user)
        return super().form_valid(form)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/')


class AddUserView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'form': AddUserForm()
        }
        return render(request, 'dnd_organizer_app/add_user.html', context)

    def post(self, request, *args, **kwargs):
        form = AddUserForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['login'],
                password=form.cleaned_data['password_1'],
                email=form.cleaned_data['email'],
            )
            return redirect(reverse_lazy('login'))
        else:
            return render(request, 'dnd_organizer_app/add_user.html', context)


class AddCampaignView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'form': AddCampaignForm()
        }
        return render(request, 'dnd_organizer_app/new_campaign.html', context)

    def post(self, request, *args, **kwargs):
        form = AddCampaignForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            campaign = Campaign.objects.create(
                name=form.cleaned_data['name'],
            )
            campaign.players.add(request.user)
            # przypisanie roli Mistrza Gry do tworcy kampanii
            CampaignUserRole.objects.create(
                user=request.user,
                campaign=campaign,
                user_role=1
            )
            return redirect('campaign-detail', campaign_id=campaign.pk)
        else:
            return render(request, 'dnd_organizer_app/new_campaign.html', context)


class AddCharacterView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'form': AddCharacterForm()
        }
        return render(request, 'dnd_organizer_app/new_character.html', context)

    def post(self, request, *args, **kwargs):
        form = AddCharacterForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            character = Character.objects.create(
                name=form.cleaned_data['name'],
                main_class=form.cleaned_data['main_class'],
                subclass=form.cleaned_data['subclass'],
                level=form.cleaned_data['level'],
                subclass_level=form.cleaned_data['subclass_level'],
                hit_points=form.cleaned_data['hit_points'],
                armor_class=form.cleaned_data['armor_class'],
                hit_dices_number=form.cleaned_data['hit_dices_number'],
                subclass_hit_dices_number=form.cleaned_data['subclass_hit_dices_number'],
                hit_dices=form.cleaned_data['hit_dices'],
                subclass_hit_dices=form.cleaned_data['subclass_hit_dices'],
                strength=form.cleaned_data['strength'],
                dexterity=form.cleaned_data['dexterity'],
                constitution=form.cleaned_data['constitution'],
                intelligence=form.cleaned_data['intelligence'],
                wisdom=form.cleaned_data['wisdom'],
                charisma=form.cleaned_data['charisma'],
                owner=request.user
            )
            return redirect('character-sheet', character_id=character.pk)
        else:
            return render(request, 'dnd_organizer_app/new_character.html', context)


class AddPlayersView(LoginRequiredMixin, View):
    def get(self, request, campaign_id, *args, **kwargs):
        campaign = get_object_or_404(Campaign, id=campaign_id)
        form = AddPlayersForm(campaign_id)
        context = {
            'campaign': campaign,
            'form': form,
        }
        return render(request, 'dnd_organizer_app/add_players.html', context)

    def post(self, request, campaign_id, *args, **kwargs):
        campaign = get_object_or_404(Campaign, id=campaign_id)
        form = AddPlayersForm(campaign_id, request.POST)
        if form.is_valid():
            players = form.cleaned_data['players']
            for player in players:
                campaign.players.add(player)
                CampaignUserRole.objects.create(
                    user=player,
                    campaign=campaign,
                    user_role=2
                )
            return redirect('campaign-detail', campaign_id=campaign.id)
        context = {
            'campaign': campaign,
            'form': form,
        }
        return render(request, 'dnd_organizer_app/add_players.html', context)


class AddCharacterToCampaign(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        # campaigns = Campaign.objects.filter(players=user)
        form = AddCharacterToCampaignForm(user)
        context = {
            'form': form
        }
        # context = {'campaigns': campaigns}
        return render(request, 'dnd_organizer_app/add_character_to_campaign.html', context)

    def post(self, request, *args, **kwargs):
        form = AddCharacterToCampaignForm(request.user, request.POST)
        if form.is_valid():
            campaign_id = form.cleaned_data['campaigns'].id
            character_id = kwargs['character_id']
            character = get_object_or_404(Character, id=character_id)

            character.campaign = Campaign.objects.get(id=campaign_id)
            character.save()

            return redirect('character-sheet', character_id=character_id)
        else:
            context = {'form': form}
            return render(request, 'dnd_organizer_app/add_character_to_campaign.html', context)


class EditCharacterView(LoginRequiredMixin, UserIsOwnerMixin, View):
    def get(self, request, character_id, *args, **kwargs):
        character = get_object_or_404(Character, id=character_id)
        form = EditCharacterForm(instance=character)
        context = {
            'form': form,
            'character': character
        }
        return render(request, 'dnd_organizer_app/edit_character.html', context)

    def post(self, request, character_id, *args, **kwargs):
        character = get_object_or_404(Character, id=character_id)
        form = EditCharacterForm(request.POST, instance=character)
        if form.is_valid():
            form.save()
            return redirect('character-sheet', character_id=character_id)
        else:
            context = {
                'form': form,
                'character': character
            }
            return render(request, 'dnd_organizer_app/edit_character.html', context)


class PlanSessionView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'form': PlanSessionForm()
        }
        return render(request, 'dnd_organizer_app/plan_session.html', context)

    def post(self, request, campaign_id, *args, **kwargs):
        campaign = get_object_or_404(Campaign, pk=campaign_id)
        form = PlanSessionForm(request.POST)
        if form.is_valid():

            session = SessionDate.objects.create(
                session_date=form.cleaned_data['session_date'],
                campaign=campaign
            )
            # Wysylanie emaiiili przy pomoc sendgrid Twillio
            users = User.objects.filter(campaignuserrole__campaign=campaign)
            emails = [user.email for user in users]
            sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
            for email in emails:
                message = Mail(
                    from_email=settings.EMAIL_HOST_USER,
                    to_emails=email,
                    subject='Kolejna sesja',
                    html_content=f'<p>Sesja "{campaign.name}" została zaplanowana na {session.session_date}.</p>'
                )
                try:
                    sg.send(message)
                except Exception as e:
                    print(f"An error occurred while sending email to {email}: {e}")

            return redirect('campaign-detail', campaign_id=campaign.id)
        context = {'form': form}
        return render(request, 'dnd_organizer_app/plan_session.html', context)
