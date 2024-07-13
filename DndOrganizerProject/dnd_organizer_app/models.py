from django.conf import settings
from django.db import models

ROLES = (
    (0, "None"),
    (1, "Game Master"),
    (2, "Player")
)

CLASSES = (
    (1, "Fighter"),
    (2, "Ranger"),
    (3, "Warlock"),
    (4, "Mage"),
    (5, "Sorcerer"),
    (6, "Cleric"),
    (7, "Rogue")
)

LEVEL_CHOICES = [(i, str(i)) for i in range(1, 21)]

MODIFIER_CHOICES = [(i, str(i)) for i in range(3, 21)]

HIT_DICES = (
    (1, 4),
    (2, 6),
    (3, 8),
    (4, 10),
    (5, 12)
)


class User2(models.Model):
    username = models.CharField(max_length=64)

    # role = models.IntegerField(choices=ROLES)
    def __str__(self):
        return self.username


class Campaign(models.Model):
    name = models.CharField(max_length=128)
    players = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name


class CampaignUserRole(models.Model):
    user_role = models.IntegerField(choices=ROLES)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    campaign = models.ForeignKey("Campaign", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Character(models.Model):
    name = models.CharField(max_length=32)
    main_class = models.IntegerField(choices=CLASSES)
    subclass = models.IntegerField(choices=CLASSES, null=True)
    level = models.IntegerField(choices=LEVEL_CHOICES)
    subclass_level = models.IntegerField(choices=LEVEL_CHOICES, null=True)
    hit_points = models.IntegerField()
    armor_class = models.SmallIntegerField()
    hit_dices_number = models.SmallIntegerField()
    subclass_hit_dices_number = models.SmallIntegerField(null=True)
    hit_dices = models.IntegerField(choices=HIT_DICES)
    subclass_hit_dices = models.IntegerField(choices=HIT_DICES, null=True)
    strength = models.IntegerField(choices=MODIFIER_CHOICES)
    dexterity = models.IntegerField(choices=MODIFIER_CHOICES)
    constitution = models.IntegerField(choices=MODIFIER_CHOICES)
    intelligence = models.IntegerField(choices=MODIFIER_CHOICES)
    wisdom = models.IntegerField(choices=MODIFIER_CHOICES)
    charisma = models.IntegerField(choices=MODIFIER_CHOICES)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True)

    # equipment =
    # spells =
    def __str__(self):
        return self.name

    def get_main_class_name(self):
        for index, class_name in CLASSES:
            if index == self.main_class:
                return class_name
        return None

    def get_subbclass_name(self):
        for index, class_name in CLASSES:
            if index == self.subclass:
                return class_name
        return None

    def get_main_hit_dice_type(self):
        for index, hit_dice_type in HIT_DICES:
            if index == self.hit_dices:
                return hit_dice_type
        return None

    def get_subclass_hit_dice_type(self):
        for index, hit_dice_type in HIT_DICES:
            if index == self.subclass_hit_dices:
                return hit_dice_type
        return None

class Weapon(models.Model):
    WEAPON_TYPES = (
        (1, "Strength"),
        (2, "Finesse")
    )
    name = models.CharField(max_length=32)
    description = models.TextField(null=True)
    type = models.IntegerField(choices=WEAPON_TYPES)
    hit_dice = models.IntegerField(choices=HIT_DICES)
    magic = models.BooleanField()
    bonus = models.IntegerField()


class Equipment(models.Model):
    character = models.OneToOneField(Character, on_delete=models.CASCADE)
    weapons = models.ManyToManyField(Weapon)


#     items =


class SessionDate(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    session_date = models.DateField()
