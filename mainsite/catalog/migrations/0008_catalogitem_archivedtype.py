# Generated by Django 3.0.5 on 2020-11-09 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_merge_20200918_1113'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalogitem',
            name='archivedType',
            field=models.CharField(choices=[('VI', 'Visible'), ('HD', 'Hidden'), ('RE', 'Removed')], default='VI', max_length=2),
        ),
    ]
