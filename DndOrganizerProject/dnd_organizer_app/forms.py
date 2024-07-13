from django.utils import timezone

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from dnd_organizer_app.models import Campaign, Character, SessionDate


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cd = super().clean()
        username = cd.get('username')
        password = cd.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError("Podaj poprawny login lub haslo")
        else:
            self.user = user


class AddUserForm(forms.Form):
    login = forms.CharField(max_length=150)
    password_1 = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    def clean(self):
        cd = super().clean()
        pass1 = cd.get('password_1')
        pass2 = cd.get('password_2')
        username = cd.get('login')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Nazwa uzytkownika jest zajeta.")
        if pass1 != pass2:
            raise ValidationError('Podaj poprawnie obydwa hasła.')


class AddCampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name']


class AddCharacterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.notrequired:
            self.fields[field].required = False

    class Meta:
        model = Character
        fields = [
            'name',
            'main_class',
            'subclass',
            'level',
            'subclass_level',
            'hit_points',
            'armor_class',
            'hit_dices_number',
            'subclass_hit_dices_number',
            'hit_dices',
            'subclass_hit_dices',
            'strength',
            'dexterity',
            'constitution',
            'intelligence',
            'wisdom',
            'charisma',
        ]
        notrequired = [
            'subclass',
            'subclass_level',
            'subclass_hit_dices_number',
            'subclass_hit_dices_number',
            'subclass_hit_dices',
        ]


class AddPlayersForm(forms.Form):
    players = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Campaign
        fields = ['players']

    def __init__(self, campaign_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['players'].queryset = User.objects.exclude(
            campaignuserrole__campaign_id=campaign_id
        )


class AddCharacterToCampaignForm(forms.Form):
    campaigns = forms.ModelChoiceField(
        queryset=None,
        label='Wybierz kampanie'
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['campaigns'].queryset = Campaign.objects.filter(players=user)

    class Meta:
        # model = Campaign
        fields = ['campaigns']


class EditCharacterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.notrequired:
            self.fields[field].required = False

    class Meta:
        model = Character
        fields = [
            'name',
            'main_class',
            'subclass',
            'level',
            'subclass_level',
            'hit_points',
            'armor_class',
            'hit_dices_number',
            'subclass_hit_dices_number',
            'hit_dices',
            'subclass_hit_dices',
            'strength',
            'dexterity',
            'constitution',
            'intelligence',
            'wisdom',
            'charisma',
        ]
        notrequired = [
            'subclass',
            'subclass_level',
            'subclass_hit_dices_number',
            'subclass_hit_dices_number',
            'subclass_hit_dices',
        ]

    def clean_hit_points(self):
        hit_points = self.cleaned_data.get('hit_points')
        if hit_points < 0:
            raise forms.ValidationError("Punkty zycia nie moga byc ujemne.")
        return hit_points

    def clean_armor_class(self):
        armor_class = self.cleaned_data.get('armor_class')
        if armor_class < 0:
            raise forms.ValidationError("Klasa pancerza nie moze byc ujemna.")
        return armor_class

    def clean_level(self):
        level = self.cleaned_data.get('level')
        if level is None or level < 0:
            raise ValidationError("Poziom nie moze byc ujemny.")
        return level

    def clean_subclass_level(self):
        subclass_level = self.cleaned_data.get('subclass_level')
        if subclass_level is not None and subclass_level < 0:
            raise ValidationError("Poziom nie moze byc ujemny.")
        return subclass_level

    def clean_hit_dices_number(self):
        hit_dices_number = self.cleaned_data.get('hit_dices_number')
        if hit_dices_number is None or hit_dices_number < 0:
            raise ValidationError("Liczba kosci nie moze byc ujemna.")
        return hit_dices_number

    def clean_subclass_hit_dices_number(self):
        subclass_hit_dices_number = self.cleaned_data.get('subclass_hit_dices_number')
        if subclass_hit_dices_number is not None and subclass_hit_dices_number < 0:
            raise ValidationError("Liczba kosci nie moze byc ujemmmmmmna")
        return subclass_hit_dices_number


class PlanSessionForm(forms.ModelForm):
    class Meta:
        model = SessionDate
        fields = ['session_date']
        widgets = {
            'session_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_session_date(self):
        print(self.cleaned_data)
        session_date = self.cleaned_data['session_date']
        if session_date < timezone.now().date():
            raise ValidationError(
                "Wybierz date z przyszlosci albo dzisiejsza date!"
            )
        return session_date
