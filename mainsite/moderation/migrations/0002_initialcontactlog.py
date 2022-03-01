# Generated by Django 3.1.2 on 2022-02-14 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InitialContactLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.TextField()),
                ('receiver', models.TextField()),
                ('date_sent', models.DateTimeField(auto_now_add=True)),
                ('message', models.TextField()),
            ],
        ),
    ]