# Generated by Django 4.2.1 on 2023-06-16 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_alter_tag_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='text',
            field=models.TextField(default='', verbose_name='описание рецепта'),
            preserve_default=False,
        ),
    ]
