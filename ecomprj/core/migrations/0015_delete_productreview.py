# Generated by Django 4.2.2 on 2024-04-05 21:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_cartorderproducts_remove_productreview_date_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductReview',
        ),
    ]