# Generated by Django 4.2.2 on 2024-04-30 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userauths", "0004_alter_contactus_options_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="address",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="country",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
