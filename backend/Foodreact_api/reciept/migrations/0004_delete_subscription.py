# Generated by Django 3.2.16 on 2023-01-17 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reciept', '0003_favoritereciepes_shoppingcart_subscription'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Subscription',
        ),
    ]