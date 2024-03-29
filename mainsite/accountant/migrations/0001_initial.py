# Generated by Django 3.1.2 on 2021-04-02 22:50

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
            name='user_profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preferred_name', models.CharField(blank=True, max_length=50, null=True)),
                ('home_city', models.CharField(blank=True, max_length=50, null=True)),
                ('home_state', models.CharField(blank=True, max_length=50, null=True)),
                ('zipcode', models.IntegerField(blank=True, null=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='account/profilepics/')),
                ('last_email', models.DateTimeField(null=True)),
                ('emails_today', models.IntegerField(default=0)),
                ('last_flag', models.DateTimeField(null=True)),
                ('flags_today', models.IntegerField(default=0)),
                ('points', models.IntegerField(default=0)),
                ('banned_until', models.DateTimeField(null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
