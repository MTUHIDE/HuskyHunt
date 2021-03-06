# Generated by Django 3.0.5 on 2020-11-10 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_catalogitem_archivedtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogitem',
            name='archivedType',
            field=models.CharField(choices=[('VI', 'Visible'), ('HD', 'Hidden'), ('RE', 'Removed'), ('AR', 'Archived')], default='VI', max_length=2),
        ),
    ]
