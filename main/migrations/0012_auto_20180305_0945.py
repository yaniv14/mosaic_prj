# Generated by Django 2.0.2 on 2018-03-05 07:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20180302_1106'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mosaicitem',
            options={'ordering': ['misp_rashut']},
        ),
        migrations.AlterModelOptions(
            name='mosaicpicture',
            options={'ordering': ['mosaic__misp_rashut']},
        ),
    ]
