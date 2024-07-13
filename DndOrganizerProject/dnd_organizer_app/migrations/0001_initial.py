# Generated by Django 4.2.10 on 2024-07-12 10:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('players', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('main_class', models.IntegerField(choices=[(1, 'Fighter'), (2, 'Ranger'), (3, 'Warlock'), (4, 'Mage'), (5, 'Sorcerer'), (6, 'Cleric'), (7, 'Rogue')])),
                ('subclass', models.IntegerField(choices=[(1, 'Fighter'), (2, 'Ranger'), (3, 'Warlock'), (4, 'Mage'), (5, 'Sorcerer'), (6, 'Cleric'), (7, 'Rogue')], null=True)),
                ('level', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20')])),
                ('subclass_level', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20')], null=True)),
                ('hit_points', models.IntegerField()),
                ('armor_class', models.SmallIntegerField()),
                ('hit_dices_number', models.SmallIntegerField()),
                ('subclass_hit_dices_number', models.SmallIntegerField(null=True)),
                ('hit_dices', models.IntegerField(choices=[(1, 4), (2, 6), (3, 8), (4, 10), (5, 12)])),
                ('subclass_hit_dices', models.IntegerField(choices=[(1, 4), (2, 6), (3, 8), (4, 10), (5, 12)], null=True)),
                ('strength', models.IntegerField(choices=[(3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20')])),
                ('dexterity', models.IntegerField(choices=[(3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20')])),
                ('constitution', models.IntegerField(choices=[(3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20')])),
                ('intelligence', models.IntegerField(choices=[(3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20')])),
                ('wisdom', models.IntegerField(choices=[(3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20')])),
                ('charisma', models.IntegerField(choices=[(3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20')])),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dnd_organizer_app.campaign')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='User2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Weapon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('description', models.TextField(null=True)),
                ('type', models.IntegerField(choices=[(1, 'Strength'), (2, 'Finesse')])),
                ('hit_dice', models.IntegerField(choices=[(1, 4), (2, 6), (3, 8), (4, 10), (5, 12)])),
                ('magic', models.BooleanField()),
                ('bonus', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dnd_organizer_app.character')),
                ('weapons', models.ManyToManyField(to='dnd_organizer_app.weapon')),
            ],
        ),
        migrations.CreateModel(
            name='CampaignUserRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_role', models.IntegerField(choices=[(0, 'None'), (1, 'Game Master'), (2, 'Player')])),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dnd_organizer_app.campaign')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]