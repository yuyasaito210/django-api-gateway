# Generated by Django 2.2.6 on 2020-02-20 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0006_auto_20200220_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentalrequest',
            name='status',
            field=models.CharField(choices=[('REQUIRED_RENT', 'RequiredRent'), ('RENTED', 'Rented'), ('RENTED', 'RequiredReturn'), ('REQUIRED_RETURN', 'Returned')], default='REQUIRED_RENT', max_length=20),
        ),
    ]
