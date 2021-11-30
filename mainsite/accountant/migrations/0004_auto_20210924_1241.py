# Generated by Django 3.1.2 on 2021-09-24 16:41

import accountant.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountant', '0003_auto_20210924_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_profile',
            name='zipcode',
            field=models.CharField(blank=True, max_length=5, null=True, validators=[accountant.models.validate_zip, django.core.validators.MinLengthValidator(5)]),
        ),
    ]