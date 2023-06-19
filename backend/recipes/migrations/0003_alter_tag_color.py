# Generated by Django 4.2.1 on 2023-06-15 15:23

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=18, samples=[('#FF0000', 'red'), ('#FFFF00', 'yellow'), ('#00FF00', 'lime'), ('#0000FF', 'blue')]),
        ),
    ]
